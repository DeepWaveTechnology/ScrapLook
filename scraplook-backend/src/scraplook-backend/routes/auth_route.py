"""
Route module to manage user authentification
"""

from typing import Annotated, Optional
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError
from prisma import Prisma, errors
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models.user import Token, UserOutput
from prisma.models import User
from services.user_services import get_user_by_name
from config.app_config import get_app_config
from config.prisma_client import get_prisma_instance

# === Configuration JWT ===
ALGORITHM = "HS256"

# === Initialisation du router ===
router = APIRouter(prefix="/auth", tags=["auth"])

# === OAuth2 ===
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# === Password hashing ===
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

APP_CONFIG = get_app_config()


# === Fonctions auxiliaires ===
def verify_password(plain_password, hashed_password) -> bool:
    """
    Check password is equivalent to a hashed password.

    Args:
        plain_password: Password to check.
        hashed_password: Password hashed, base of comparison.

    Returns:
        bool: Indicates if password is equivalent to hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    """
    Create JWT access token.

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
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


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
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les identifiants",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, APP_CONFIG.env_data.encryption_key, algorithms=[ALGORITHM]
        )
        username = payload.get("sub")
    except JWTError as error:
        APP_CONFIG.logger.warning("Failed to decode jwt token '%s': %s", token, error)
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


@router.get("/me", response_model=UserOutput)
async def read_users_me(current_user: Annotated[UserOutput, Depends(get_current_user)]):
    """
    Endpoint to retrieve user information based on an access token.

    Args:
        current_user: User information.

    Returns:
        UserOutput: User information.
    """
    return current_user
