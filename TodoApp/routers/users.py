from typing import Annotated
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Todos, Users
from starlette import status
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from .auth import get_current_user
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

templates = Jinja2Templates(directory="TodoApp/templates")

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

@router.get('/search-user-page')
async def render_search_user_page(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@router.get('/', status_code=status.HTTP_200_OK)
async def read_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)  
    db.commit()

@router.put('/phonenumber/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()

@router.get("/search/", status_code=status.HTTP_200_OK)
async def search_user(user: user_dependency, user_id: int, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    result = (
        db.query(Users)
        .filter(Users.id >= user_id)
        .order_by(Users.id)
        .limit(1)
        .first()
    )
    
    if result:
        return {"id": result.id, "name": result.username, 'first_name': result.first_name, 'last_name': result.last_name, "email": result.email, "role": result.role}
    
    raise HTTPException(status_code=404, detail="Todo not found.")