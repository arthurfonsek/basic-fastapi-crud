from fastapi import Depends, FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TremboFit API",
    description="TremboFit é uma empresa de academia que oferece planos de assinatura para seus membros.",
    summary="API para o sistema de gerenciamento de membros da TremboFit",
    version="0.0.1",
    terms_of_service="https://shorturl.at/orW18",
    contact={
        "name": "Arthur Boschini da Fonseca, Pedro Paulo Moreno Camargo",
        "email": "arthurbf3@al.insper.edu.br, ppmcamargo@gmail.com"
    },
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"}
)

def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        for _, method_item in app.openapi_schema.get('paths').items():
            for _, param in method_item.items():
                responses = param.get('responses')
                # remove 422 response, also can remove other status code
                if '422' in responses:
                    del responses['422']
    return app.openapi_schema

app.openapi = custom_openapi

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#------------------MEMBERS------------------#

#GET MEMBER
@app.get("/members/{member_id}",
         response_model=schemas.Member,
         responses={
            404: {"content": {"String": {"example": "Member not found"}}},
            200: {"description": "Success", "content": {"application/json": {"example": {"name": "Jonas", "age": 30, "email": "jonas@insper.com", "plan": "Basic", "status": True}}}}    
            }
         )
def get_member(member_id: int, db: Session = Depends(get_db)):
    db_member = crud.get_member(db, member_id=member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member

#GET ALL MEMBERS
@app.get("/members", 
         response_model=list[schemas.Member],
         responses={
            200: {"description": "Success", "content": {"application/json": {"example": {
  "1": {
    "name": "Name1",
    "age": 30,
    "email": "name1@insper.com",
    "plan": "Basic",
    "status": True
  },
  "2": {
    "name": "Name2",
    "age": 25,
    "email": "name2@insper.com",
    "plan": "Premium",
    "status": True
  },
  "3": {
    "name": "Name3",
    "age": 35,
    "email": "name3@insper.com",
    "plan": "Gold",
    "status": True
  },
  "4": {
    "name": "Name4",
    "age": 40,
    "email": "name4@insper.com",
    "plan": "Basic",
    "status": False
  }}}}}}
         )
def get_all_members(db: Session = Depends(get_db)):
    db_members = crud.get_all_members(db)
    if db_members is None:
        raise HTTPException(status_code=404, detail="No members found")
    return db_members

#CREATE MEMBER
@app.post("/members", 
          response_model=schemas.Member,
          responses={
            400: {"content": {"String": {"example": "Member already exists"}}},
            200: {"description": "Success", "content": {"application/json": {"example": {"name": "name1", "age": 20, "email": "name1@insper.com", "plan": "Basic", "status": True}}}},
            404: {"content": {"String": {"example": "Plan not found"}}}
        })
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    db_member = crud.create_member(db, member=member)
    return db_member

#UPDATE MEMBER
@app.put("/members/{member_id}", 
         response_model=schemas.Member, 
         responses={
            404: {"content": {"application/json": {"example": {"detail": "Member not found"}}}},
            400: {"content": {"application/json": {"example": {"detail": "Plan not found"}}}},
            200: {"description": "Success", "content": {"application/json": {"example": {"name": "Rafael", "age": 20, "email": "rafael@insper.com", "plan": "Gold", "status": False}}}}   
            })
def update_member(member_id: int, member: schemas.MemberUpdate, db: Session = Depends(get_db)):
    db_member = crud.update_member(db, member_id=member_id, member=member)
    return db_member

#DELETE MEMBER
@app.delete("/members/{member_id}", 
            response_model=schemas.Member, 
            responses={
            404: {"content": {"String": {"example": "Member not found"}}},
            200: {"description": "Success", "content": {"application/json": {"example": {"message": "Member deleted"}}}}   
            })
def delete_member(member_id: int, db: Session = Depends(get_db)):
    db_member = crud.delete_member(db, member_id=member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member

#------------------PLANS------------------#

#GET PLAN
@app.get("/plans/{plan_id}", 
         response_model=schemas.Plan,
         responses={
            404: {"content": {"String": {"example": "Plan not found"}}},
            200: {"description": "Success", "content": {"application/json": {"example": {3: {
        "plan_name": "Gold",
        "price": 300,
        "status": True}}}}}    
            })
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    db_plan = crud.get_plan(db, plan_id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return db_plan

#GET ALL PLANS
@app.get("/plans", 
         response_model=list[schemas.Plan],
         responses={
            200: {"description": "Success", "content": {"application/json": {"example": {
    1: {
        "plan_name": "Basic",
        "price": 100,
        "status": True},
    2: {
        "plan_name": "Premium",
        "price": 200,
        "status": True},
    3: {
        "plan_name": "Gold",
        "price": 300,
        "status": True}
        }}}}})
def get_all_plans(db: Session = Depends(get_db)):
    db_plans = crud.get_all_plans(db)
    if db_plans is None:
        raise HTTPException(status_code=404, detail="No plans found")
    return db_plans

#CREATE PLAN
@app.post("/plans", 
          response_model=schemas.Plan,
          responses={
            500: {"content": {"String": {"example": "Plan already exists"}}},
            200: {"description": "Success", "content": {"application/json": {"example": {"name": "Black", "price": 150, "status":True}}}},
            })
def create_plan(plan: schemas.PlanCreate, db: Session = Depends(get_db)):
    db_plan = crud.create_plan(db, plan=plan)
    if db_plan.plan_name in crud.get_all_plans(db):
        raise HTTPException(status_code=400, detail="Plan already exists")
    return db_plan

#UPDATE PLAN
@app.put("/plans/{plan_id}", 
         response_model=schemas.Plan,
         responses={
            404: {"content": {"String": {"example": "Plan does not exists"}}},
            200: {"description": "Success", "content": {"application/json": {"example": {"name": "Signature", "price": 1000, "status":False}}}}    
            })
def update_plan(plan_id: int, plan: schemas.PlanUpdate, db: Session = Depends(get_db)):
    db_plan = crud.update_plan(db, plan_id=plan_id, plan=plan)
    return db_plan

#DELETE PLAN
@app.delete("/plans/{plan_id}", 
            response_model=schemas.Plan,
            responses={
            404: {"content": {"String": {"example": "Plan not found"}}},
            200: {"description": "Success", "content": {"application/json": {"example": {"message": "Plan deleted"}}}} 
            })
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    db_plan = crud.delete_plan(db, plan_id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return db_plan

#------------------MEMBER-PLAN------------------#

#GET MEMBERS OF A PLAN
@app.get("/plans/{plan_id}/members", 
         response_model=list[schemas.Member],
         responses={
             400: {"content": {"String": {"example": "Plan does not exists"}}},
             404: {"content": {"String": {"example": "No members found"}}},
             200: {"description": "Success", "content": {"application/json": {"example": {
                    "1": {
                        "name": "Name1",
                        "age": 30,
                        "email": "name1@insper.com",
                        "plan": "Basic",
                        "status": True
                    },
                    "2": {
                        "name": "Name2",
                        "age": 25,
                        "email": "name2@insper.com",
                        "plan": "Premium",
                        "status": True
                    },
                    "3": {
                        "name": "Name3",
                        "age": 35,
                        "email": "name3@insper.com",
                        "plan": "Gold",
                        "status": True
                    },
                    "4": {
                        "name": "Name4",
                        "age": 40,
                        "email": "name4@insper.com",
                        "plan": "Basic",
                        "status": False
                    }}}}}}
                )
def get_members_of_plan(plan_id: int, db: Session = Depends(get_db)):
    db_members = crud.get_members_of_plan(db, plan_id=plan_id)
    if len(db_members) == 0:
        raise HTTPException(status_code=404, detail="No members found")
    return db_members