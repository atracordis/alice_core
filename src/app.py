from typing import List

from fastapi import FastAPI, Query
import random

from .infrastructure.auth.auth_utils import *
from .infrastructure.resources.reader import *
from .infrastructure.resources.const import *
from .domain.predict import *

app = FastAPI(title="Question acquiring API", description="Log in. Get sentiment. Don't worry. Be happy.", version="1.0",
              openapi_tags=[{'name': 'auth', 'description': 'Authentication functions'},
                            {'name': 'core', 'description': 'Core functions'}])


@app.post("/token", response_model=Token, tags=["auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Logs user in
    :param form_data: contains username and password
    :return: access token
    """
    user = authenticate_user(credentials, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User, tags=["auth"])
async def check_if_logged_in(current_user: User = Depends(get_current_active_user)):
    """
    Checks if logged in
    :param current_user: gets current user, raises exception if not logged in
    :return: current username
    """
    return current_user


@app.get('/test', tags=["core"])
def check_if_up():
    """
    Checks if app is up
    :return: set to say all is ok
    """
    return {'Diagnostics complete. All systems nominal'}


@app.get("/sentiment/", tags=["core"])
async def check_if_logged_in(sentence : str,
                             branch : str = Query("agnostic_model", enum=["agnostic_model", "Disneyland_HongKong", "Disneyland_California", "Disneyland_Paris"]),
                             current_user: User = Depends(get_current_active_user)):
    """
    Checks if logged in
    :param current_user: gets current user, raises exception if not logged in
    :return: current username
    """

    return {"status":"great success",
            "sentiment":predict(sentence, processor, branch)}



@app.get("/get_score/", tags=["core"])
async def check_if_logged_in(branch : str = Query("agnostic_model", enum=valid_branches),
                             current_user: User = Depends(get_current_active_user)):
    """
    Checks if logged in
    :param current_user: gets current user, raises exception if not logged in
    :return: current username
    """

    return {"status":"great success",
            "score": str(processor[branch]["score"])}
