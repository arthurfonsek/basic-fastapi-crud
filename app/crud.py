from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

#------------------MEMBERS------------------#
#CRUD

#GET MEMBER
def get_member(db: Session, member_id: int):
    return db.query(models.Member).filter(models.Member.member_id == member_id).first()

#get all members
def get_all_members(db: Session):
    return db.query(models.Member).all()

#CREATE MEMBER
def create_member(db: Session, member: schemas.MemberCreate):
    db_member = models.Member(name=member.name, age=member.age, email=member.email, plan_id=member.plan_id, status=member.status)
    planIdExists = db.query(models.Plan).filter(models.Plan.plan_id == member.plan_id).first()
    if planIdExists is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

#UPDATE MEMBER
def update_member(db: Session, member_id: int, member: schemas.MemberUpdate):
    db_member = db.query(models.Member).filter(models.Member.member_id == member_id).first()
    planIdExists = db.query(models.Plan).filter(models.Plan.plan_id == member.plan_id).first()
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    if planIdExists is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    for var, value in vars(member).items():
        if value is not None:
            setattr(db_member, var, value)
    db.commit()
    db.refresh(db_member)
    return db_member
    
#DELETE MEMBER
def delete_member(db: Session, member_id: int):
    db_member = db.query(models.Member).filter(models.Member.member_id == member_id).first()
    db.delete(db_member)
    db.commit()
    return db_member

#------------------PLANS------------------#
#CRUD

#GET PLAN
def get_plan(db: Session, plan_id: int):
    return db.query(models.Plan).filter(models.Plan.plan_id == plan_id).first()

#GET ALL PLANS
def get_all_plans(db: Session):
    return db.query(models.Plan).all()

#CREATE PLAN
def create_plan(db: Session, plan: schemas.PlanCreate):
    db_plan = models.Plan(plan_name=plan.plan_name, price=plan.price, status=plan.status)
    if plan.plan_name in db.query(models.Plan.plan_name):
        raise HTTPException(status_code=400, detail="Plan already exists")
    elif plan.plan_name not in db.query(models.Plan.plan_name):
        db.add(db_plan)
        db.commit()
        db.refresh(db_plan)
        return db_plan
    
#UPDATE PLAN
def update_plan(db: Session, plan_id: int, plan: schemas.PlanUpdate):
    db_plan = db.query(models.Plan).filter(models.Plan.plan_id == plan_id).first()
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    for var, value in vars(plan).items():
        if value is not None:
            setattr(db_plan, var, value)
    db.commit()
    db.refresh(db_plan)
    return db_plan

#DELETE PLAN
def delete_plan(db: Session, plan_id: int):
    db_plan = db.query(models.Plan).filter(models.Plan.plan_id == plan_id).first()
    db.delete(db_plan)
    db.commit()
    return db_plan

#------------------MEMBER-PLAN------------------#

#GET MEMBERS OF A PLAN
def get_members_of_plan(db: Session, plan_id: int):
    planIdExists = db.query(models.Plan).filter(models.Plan.plan_id == plan_id).first()
    if planIdExists is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return db.query(models.Member).filter(models.Member.plan_id == plan_id).all()