from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import os
import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://test:test@db:5432/testdb"
)

engine = sqlalchemy.create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class ItemModel(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, default="")

Base.metadata.create_all(bind=engine)

class Item(BaseModel):
    id: int
    name: str
    description: str = ""

app = FastAPI()

@app.post("/items/", response_model=Item, status_code=201)
def create_item(item: Item):
    db = SessionLocal()
    if db.query(ItemModel).filter(ItemModel.id == item.id).first():
        db.close()
        raise HTTPException(400, "Item already exists")
    db_item = ItemModel(**item.dict())
    db.add(db_item); db.commit(); db.refresh(db_item)
    db.close()
    return db_item

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    db = SessionLocal()
    db_item = db.query(ItemModel).get(item_id)
    db.close()
    if not db_item:
        raise HTTPException(404, "Item not found")
    return db_item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated: Item):
    db = SessionLocal()
    db_item = db.query(ItemModel).get(item_id)
    if not db_item:
        db.close()
        raise HTTPException(404, "Item not found")
    for k, v in updated.dict().items():
        setattr(db_item, k, v)
    db.commit(); db.refresh(db_item); db.close()
    return db_item

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    db = SessionLocal()
    db_item = db.query(ItemModel).get(item_id)
    if not db_item:
        db.close()
        raise HTTPException(404, "Item not found")
    db.delete(db_item); db.commit(); db.close()
