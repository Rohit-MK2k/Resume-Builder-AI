from typing import Dict, Any, List, Annotated
from pydantic import BaseModel 

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from database import get_db
from database import User

router = APIRouter(
    prefix="",
    tags=["user authentication"]
)

db_dependency = Annotated[Session, Depends(get_db)]

class userCreate(BaseModel):
    username: str
    email: str
    password: str

class userExist(BaseModel):
    email: str
    password: str

# @desc   Register new user
# @route  POST / api / auth
# @access Public
@router.post("/signup")
def registerUser(newUser: userCreate, db: db_dependency):
    # Check if user with this email already exists in the database
    user_exists = db.query(User).filter(User.email == newUser.email).first()
    
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    
    # If user doesn't exist, we can proceed with registration
    new_user = User(
        name = newUser.username,
        email = newUser.email,
        password = newUser.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User Created Sucessfully",  "status": "success"}

@router.post('/login')
def authUser(user: userExist, db: db_dependency):
    print(user)