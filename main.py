from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy import Column,String,Integer
from sqlalchemy.orm import declarative_base,Session
from database import engine,get_session
app=FastAPI()

Base=declarative_base()

class NewUser(Base):
    __tablename__="newuser"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(100))
    age=Column(Integer)
    phone=Column(String(100))
    email=Column(String(150))
Base.metadata.create_all(engine)
class CreateNew(BaseModel):
    name:str
    age:int
    phone:str
    email:str
   
@app.post("/user")
def new_user(user:CreateNew,db:Session =Depends(get_session)):
    new=NewUser(name=user.name,
                age=user.age,
                phone=user.phone,
                email=user.email)
    db.add(new)
    db.commit()
    db.refresh(new)
    return {"new user":new}

@app.get("/users")
def get_all(db:Session =Depends(get_session)):
    all=db.query(NewUser).all()
    return all

@app.get("/users/{user_id}")
def get_one(user_id:int,db:Session =Depends(get_session)):
    user=db.query(NewUser).filter(NewUser.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404,
                            detail="user not found")
    return user
    
@app.put("/user/{user_id}")
def update(user_id:int,update:CreateNew,db:Session =Depends(get_session)):
    one=db.query(NewUser).filter(NewUser.id==user_id).first()
    if not one:
        raise HTTPException(status_code=404,
                            detail="user not found")
    one.name=update.name
    one.age=update.age
    one.phone=update.phone
    one.email=update.email
    
    db.commit()
    return {"successfully updated"}

@app.delete("/user/{user_id}")
def dalete(user_id:int,db:Session =Depends(get_session)):
    result=db.query(NewUser).filter(NewUser.id==user_id).first()
    if not result:
        raise HTTPException(status_code=404,
                            detail="user not found")
    db.delete(result)
    db.commit()
    return {"deleted"}