"""
Route module to manage user authentification
"""

from typing import Annotated, Optional
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models.user import Token, UserOutput
from prisma import Prisma, errors
from prisma.models import User
from services.user_services import get_user_by_name
from utils.hash import pwd_context
from config.app_config import get_app_config
from config.prisma_client import get_prisma_instance

# === Configuration JWT ===
ALGORITHM = "HS256"

# === Initialisation du router ===
router = APIRouter(prefix="/auth", tags=["auth"])

# === OAuth2 ===
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Impossible de valider les identifiants",
    headers={"WWW-Authenticate": "Bearer"},
)

APP_CONFIG = get_app_config()


# === Fonctions auxiliaires ===
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Check password is equivalent to a hashed password.

    Args:
        plain_password: Password to check.
        hashed_password: Password hashed, base of comparison.

    Returns:
        bool: Indicates if password is equivalent to hashed password.
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError as error:
        APP_CONFIG.logger.warning(
            "Incorrect hashed password format: %s, error: %s", hashed_password, error
        )
        return False


def create_token(data: dict, expires_delta: timedelta) -> str:
    """
    Create JWT access or refresh token.

    Args:
        data: Data to encode.
        expires_delta: Expiration date of the token.

    Returns:
        str: JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, APP_CONFIG.env_data.encryption_key, algorithm=ALGORITHM
    )


async def authenticate_user(
    prisma: Prisma, username: str, password: str
) -> Optional[User]:
    """
    Authenticate user by checking credentials are correct and matches a user in DB.

    Args:
        prisma:  DB connection.
        username: Username of user to authenticate.
        password: User's password to authenticate.

    Returns:
        Optional[User]: User object if authentication was successful, otherwise None.
    """
    try:
        user = await get_user_by_name(prisma, username)
    except errors.RecordNotFoundError:
        return None
    if not verify_password(password, user.password):
        return None
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    prisma: Prisma = Depends(get_prisma_instance),
):
    """
    Endpoint to authenticate user using JWT token.

    Args:
        form_data: User's credentials.
        prisma: DB connection.

    Returns:
        Token: JWT token associated with user.
    """
    user = await authenticate_user(prisma, form_data.username, form_data.password)
    if not user:
        APP_CONFIG.logger.warning(
            "Authentication failed for user: %s", form_data.username
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=APP_CONFIG.env_data.access_token_duration_minutes
    )
    refresh_token_expires = timedelta(
        hours=APP_CONFIG.env_data.refresh_token_duration_hours
    )
    access_token = create_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    refresh_token = create_token(
        data={"sub": user.name}, expires_delta=refresh_token_expires
    )

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    prisma: Prisma = Depends(get_prisma_instance),
) -> UserOutput:
    """
    Helper method to retrieve current user from DB, and check access token is valid.

    Args:
        token: User's access token.
        prisma: DB connection.

    Returns:
        UserOutput: User object with current access token.
    """
    try:
        payload = jwt.decode(
            token, APP_CONFIG.env_data.encryption_key, algorithms=[ALGORITHM]
        )
        username = payload.get("sub")
    except JWTError as error:
        APP_CONFIG.logger.warning(
            "Failed to decode jwt access token '%s': %s", token, error
        )
        raise credentials_exception from error

    if payload.get("sub") is None:
        raise credentials_exception

    user_in_db = await get_user_by_name(prisma, username)
    user_in_db.password = ""
    if user_in_db is None:
        raise credentials_exception

    return UserOutput(
        **user_in_db.model_dump(),
        token=Token(access_token=token, token_type="bearer"),
    )


@router.get("/check_refresh_access_token", response_model=bool)
async def check_refresh_access_token(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> bool:
    """
    Route to check if access token must be refreshed.

    The access token must be refreshed if today date
    and access token timeout exceed access token expiration.

    Args:
        token: Access token to check.

    Returns: True if access token must be refreshed, otherwise False.
    """
    try:
        payload = jwt.decode(
            token, APP_CONFIG.env_data.encryption_key, algorithms=[ALGORITHM]
        )
    except JWTError as error:
        APP_CONFIG.logger.warning(
            "Failed to decode jwt access token to check '%s': %s", token, error
        )
        raise credentials_exception from error

    # check if access token is invalid in xx
    access_token_timeout = timedelta(
        minutes=APP_CONFIG.env_data.access_token_invalid_timeout_minutes
    )

    if (
        payload.get("exp") is not None
        and datetime.now().astimezone() + access_token_timeout
        >= datetime.fromtimestamp(payload.get("exp")).astimezone()
    ):
        APP_CONFIG.logger.info(
            "Access token has to be refreshed for user with name '%s'",
            payload.get("sub"),
        )
        return True

    return False


@router.post("/refresh_access_token", response_model=Token)
async def refresh_access_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    prisma: Prisma = Depends(get_prisma_instance),
) -> Token:
    """
    Refresh current access token by generating new access token.

    Check if refresh token passed as a parameter is valid.

    Args:
        token: Refresh token used to generate new access token for a user.
        prisma: DB connection.

    Returns: Refresh access token.
    """
    try:
        payload = jwt.decode(
            token, APP_CONFIG.env_data.encryption_key, algorithms=[ALGORITHM]
        )
        username = payload.get("sub")
    except JWTError as error:
        APP_CONFIG.logger.warning(
            "Failed to decode jwt refresh token '%s': %s", token, error
        )
        raise credentials_exception from error

    if payload.get("sub") is None:
        raise credentials_exception

    user_in_db = await get_user_by_name(prisma, username)
    user_in_db.password = ""
    if user_in_db is None:
        raise credentials_exception

    # create a new access token
    access_token_expires = timedelta(
        minutes=APP_CONFIG.env_data.access_token_duration_minutes
    )
    new_access_token = create_token(
        data={"sub": user_in_db.name}, expires_delta=access_token_expires
    )

    return Token(access_token=new_access_token, token_type="bearer")


@router.get("/me", response_model=UserOutput)
async def read_users_me(user: Annotated[UserOutput, Depends(get_current_user)]):
    """
    Endpoint to retrieve user information based on an access token.

    Args:
        user: User information.

    Returns:
        UserOutput: User information.
    """
    return user
