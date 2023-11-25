from pydantic import BaseModel
from typing import Union

class MemberBase(BaseModel):
    name: str
    age: int
    email: str
    plan_id: int
    status: bool

class Member(MemberBase):
    member_id: Union[int, None] = None

    class Config:
        orm_mode = True

class MemberCreate(MemberBase):
    pass

class MemberUpdate(BaseModel):
    name: str = None
    age: int = None
    email: str = None
    plan_id: int = None
    status: bool = None

class MemberUpdateData(MemberUpdate):
    pass

class MemberUpdateResponse(MemberBase):
    pass

#-----------------PLAN-----------------#

class PlanBase(BaseModel):
    plan_name: str
    price: float
    status: bool

class Plan(PlanBase):
    plan_id: Union[int, None] = None

    class Config:
        orm_mode = True

class PlanCreate(PlanBase):
    pass

class PlanUpdate(BaseModel):
    plan_name: str = None
    price: int = None
    status: bool = None

class PlanUpdateData(PlanUpdate):
    pass

class PlanUpdateResponse(PlanBase):
    pass

#---------------MEMBER-PLAN-----------------#

class MemberofPlan(BaseModel):
    plan_id: int

    class Config:
        orm_mode = True

