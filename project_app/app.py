from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from typing import List, Dict, Optional

from schema import UserGet, PostGet, FeedGet
# from models import User, Post, Feed
from table_user import User
from table_post import Post
from table_feed import Feed

from database import Base, SessionLocal

from loguru import logger

app = FastAPI()


async def get_db():
    with SessionLocal() as db:
        return db


@app.get('/user/{id}', response_model=UserGet)
async def get_user_id(id: int, db: Session = Depends(get_db)):
    result = db.query(User).filter(User.id == id).all()
    if not len(result):
        raise HTTPException(404, 'User not found')
    else:
        return result[0]


@app.get('/post/{id}', response_model=PostGet)
async def get_post_id(id: int, db: Session = Depends(get_db)):
    result = db.query(Post).filter(Post.id == id).all()
    if not len(result):
        raise HTTPException(404, 'Post not found')
    else:
        return result[0]


@app.get('/user/{id}/feed', response_model=List[FeedGet])
async def get_feed_by_user_id(id: int, limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(Feed).filter(Feed.user_id == id).order_by(Feed.time.desc()).limit(limit).all()
    return result


@app.get('/post/{id}/feed', response_model=List[FeedGet])
async def get_feed_by_post_id(id: int, limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(Feed).filter(Feed.post_id == id).order_by(Feed.time.desc()).limit(limit).all()
    return result


@app.get('/post/recommendations/', response_model=List[PostGet])
async def get_top_likes(id: Optional[int] = None, limit: int = 10, db: Session = Depends(get_db)):
    result = db.query(Post).join(Feed) \
        .filter(Feed.action == 'like') \
        .group_by(Post.id) \
        .order_by(func.count(Post.id).desc()).limit(limit).all()
    return result

