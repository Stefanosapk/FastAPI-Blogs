from fastapi import  Depends, APIRouter,status, HTTPException
from .. import schemas, models
from ..database import  get_db
from sqlalchemy.orm import Session
from ..hashing import Hash
router = APIRouter(
    prefix="/user",
    tags=["users"],
)

@router.post('/', response_model = schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name = request.name, email = request.email, password = Hash.get_password_hash(request.password))
    # 2os tropos pio concise
    # new_user = models.User(**request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model = schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not Found.")
    return user