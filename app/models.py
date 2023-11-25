from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Member(Base):
    __tablename__ = "member"
    member_id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    name = Column(String(50), index=True)
    age = Column(Integer, index=True)
    email = Column(String(80), index=True)
    plan_id = Column(Integer, ForeignKey("plan.plan_id"), index=True)
    status = Column(Boolean, index=True, default=True)


class Plan(Base):
    __tablename__ = "plan"
    plan_id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    plan_name = Column(String(50), index=True, unique=True)
    price = Column(Integer, index=True)
    status = Column(Boolean, index=True, default=True)