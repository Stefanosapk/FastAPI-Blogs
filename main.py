from typing import Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q }

@app.put("/items/{item_id}")
def update_item(item_id: int, random: Item):
    return {"item_name": random.name, "item_id": item_id, "item_price": random.price}


@app.get("/test/validation")
async def read_items(q: Optional[str] = Query(None, min_length=3, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.post("/post/the/{item_id}")
def get_the_item(item_id: int, item: Item):
    return item