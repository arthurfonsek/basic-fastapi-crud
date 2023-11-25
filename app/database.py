from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

#READ KEY.ENV FILE
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
load_dotenv(Path("env/key.env"))
#SENHA
password = os.getenv("KEY")
user = os.getenv("USER")
database = os.getenv("DATABASE")
host = os.getenv("HOST")

SQLALCHEMY_DATABASE_URL = ("mysql://{}:{}@{}:3306/{}".format(user, password, host, database))

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
