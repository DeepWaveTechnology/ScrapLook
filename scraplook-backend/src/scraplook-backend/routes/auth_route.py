from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Annotated
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from prisma import Prisma
from config.prisma_client import get_prisma_instance

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


# === Schémas Pydantic ===
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    disabled: bool | None = False


class UserInDB(User):
    hashed_password: str


# === Fonctions auxiliaires ===
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_user_from_db(prisma: Prisma, username: str) -> UserInDB | None:
    user = await prisma.user.find_unique(where={"name": username})
    if user:
        return UserInDB(username=user.name, hashed_password=user.password)
    return None


async def authenticate_user(prisma: Prisma, username: str, password: str):
    user = await get_user_from_db(prisma, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
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
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


# === Récupération de l'utilisateur courant (via le token) ===
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    prisma: Prisma = Depends(get_prisma_instance)
) -> User:
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

    user_in_db = await get_user_from_db(prisma, username)
    if user_in_db is None:
        raise credentials_exception
    return User(username=user_in_db.username)


# === Exemple de route protégée ===
@router.get("/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


# === Pour test simple ===
@router.get("/", status_code=status.HTTP_200_OK)
async def read_new_feature():
    return {"message": "This is a new feature route!"}
