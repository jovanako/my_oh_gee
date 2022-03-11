from sqlalchemy import Column, String, Integer
from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(60, nullable=False))
