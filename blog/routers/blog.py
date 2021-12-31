from fastapi import  Depends, APIRouter,status, Response, HTTPException
from .. import schemas, models
from ..database import  get_db
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    prefix="/blog",
    tags=["blogs"],
)



@router.post('/', response_model = schemas.ShowBlog)
def createBlog(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/', response_model=List[schemas.ShowBlog])
def allBlogs(db: Session = Depends(get_db)):
    blogs =db.query(models.Blog).all()
    return blogs


@router.get('/{blog_id}', response_model = schemas.ShowBlog)
def blog(blog_id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message' : 'Blog was not found.'}
    return blog

@router.delete('/{blog_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    db_blog_to_delete = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not db_blog_to_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog was not Found.")
    db_blog_to_delete.delete(synchronize_session=False)
    db.commit()
    return {'message' : 'The blog has been deleted.'}


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def updateBlog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):  
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog was not Found.")
    blog.update(request.dict())
    db.commit()
    return 'updated'