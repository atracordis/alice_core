from ..model.Auth import *
from ..resources.credentials import *


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# to get a string like this run:
# openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password):
    """
    Verifies if password is same as hashed password
    :param plain_password: plain user password (from interface)
    :param hashed_password: hashed user password (from db)
    :return: True if ok, False if not
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Hash user password
    used to hash passwords in db
    :param password: plain user password
    :return: Hashed user password
    """
    return pwd_context.hash(password)


def get_user(credentials, username: str):
    """
    Gets user from user database
    :param db: user database
    :param username: user to get
    :return: None if user not found, UserInDB object if user found
    """
    if username in credentials:
        hashed_password = credentials[username]
        return UserInDB(username=username,hashed_password=hashed_password)


def authenticate_user(credentials, username: str, password: str):
    """
    authenticates user. First tries to get user.
    If user found, checks if user password is ok
    returns user if both checks are good
    :param credentials: user db
    :param username:
    :param password:
    :return: user if user found and password is ok, False otherwise
    """
    user = get_user(credentials, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    creates access token. Expires after expires_delta
    :param data: username
    :param expires_delta: expiration time
    :return: access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    '''
    Gets currently authenticated user
    raises exception if not authenticated
    :param token: access token
    :return: user if all is ok.
    '''
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(credentials, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Returns active user. Async wrapper around get_current_user
    :param current_user:
    :return: current user
    """
    return current_user
