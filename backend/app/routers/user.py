from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from app import schemas
from app.utils import auth
from app.db import models
from app.db.database import get_db
from app.auth import oauth2

router = APIRouter(
    tags=['Users'],
    prefix="/users",
)

@router.get("/", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db), current_user : int =  Depends(oauth2.get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You don't have enough permissions")
    print("Getting all users")
    users = db.query(models.User).all()
    return users

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = auth.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), ):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user

@router.put('/{id}', response_model=schemas.UserOut)
def update_user(id: int, user: schemas.UserUpdate, current_user : int = Depends(oauth2.get_current_user) , db: Session = Depends(get_db)):
    if current_user.id != id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You don't have enough permissions")
    user_obj = db.query(models.User).filter(models.User.id == id).first()
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    user_obj.fullname = user.fullname
    user_obj.username = user.username

    db.commit()
    db.refresh(user_obj)

    return user_obj

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user : int =  Depends(oauth2.get_current_user)):
    if current_user.id != id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You don't have enough permissions")
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    db.delete(user)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)