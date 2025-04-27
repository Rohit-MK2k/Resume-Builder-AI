import logging
import os
from typing import Dict, Any, List, Annotated
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate

from sqlalchemy.orm import Session

from Schema.resume_Schema import Resume
from resumeGenerator import ResumeGenerator

from database import get_db
from api.auth.route import router as auth_router

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


app = FastAPI()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get('/')
def root():
    return {"Hello": "World!"}

app.include_router(auth_router)

# @app.post('/user/signup/')
# def registerUser(newUser: dict, db: db_dependency):
#     print(newUser)
#     return {"message": "Received user data", "data": newUser}