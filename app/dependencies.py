from fastapi import Depends, Request, HTTPException
from jose import jwt

from typing import Annotated

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.utils import *


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dep = Annotated[Session, Depends(get_db)]



def get_current_user(
    request: Request,
    db: db_dep
):
    auth_header = request.headers.get("Authorization")
    is_bearer = auth_header.startswith("Bearer ") if auth_header else False
    token = auth_header.split(" ")[1] if auth_header else ""

    if not auth_header and is_bearer:
        raise HTTPException(
            status_code=401,
            detail="You are not authenticated."
        )


    try:
        decoded_jwt = jwt.decode(
            token,
            SECRET_KEY,
            ALGORITHM
        )
        print(decoded_jwt)
        username = decoded_jwt.get("username")
        password = decoded_jwt.get("password")
        role = decoded_jwt.get("role")

        db_user = db.query(User).filter(User.username == username).first()

    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid token."
        )

    return db_user

# ===============================================================
# before it was like this:
# ================================================================
# def get_admin_user(
#     user: User = Depends(get_current_user)
# ):
#     if user.role != "admin":
#         raise HTTPException(
#             status_code=403,
#             detail="You do not have admin privileges."
#         )

#     return user
# ================================================================



def get_admin_user(
    user: User = Depends(get_current_user)
):
    if not (user.is_staff and user.is_superuser):
        raise HTTPException(
            status_code=403,
            detail="You do not have admin privileges."
        )

    return user

current_user_dep = Annotated[User, Depends(get_current_user)]
admin_user_dep = Annotated[User, Depends(get_admin_user)]
