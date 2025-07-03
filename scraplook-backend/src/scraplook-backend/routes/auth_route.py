from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.user import Token, UserOutput
from passlib.context import CryptContext
from typing import Annotated
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from prisma import Prisma, errors
from config.prisma_client import get_prisma_instance
from services.user_services import get_user_by_name

# === Configuration JWT ===
SECRET_KEY = "57699903d1ebdf47ba210a5be9ea4178a5588ba8e7b3cefd70cc3b9e888cc67d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# === Initialisation du router ===
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# === OAuth2 ===
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# === Password hashing ===
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# === Fonctions auxiliaires ===
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def authenticate_user(prisma: Prisma, username: str, password: str):
    try:
        user = await get_user_by_name(prisma, username)
    except errors.RecordNotFoundError:
        return None
    if not verify_password(password, user.password):
        return None
    return user


# === Route de login (POST /auth/token) ===
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    prisma: Prisma = Depends(get_prisma_instance),
):
    user = await authenticate_user(prisma, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


# === Récupération de l'utilisateur courant (via le token) ===
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    prisma: Prisma = Depends(get_prisma_instance)
) -> UserOutput:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les identifiants",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
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
    return current_user
