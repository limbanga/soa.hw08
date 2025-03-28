from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, conlist, validator
from typing import List

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return v

    @validator('name')
    def name_must_be_longer_than_2(cls, v):
        if len(v) < 3:
            raise ValueError('Name must be at least 3 characters long')
        return v

class User(BaseModel):
    username: str
    email: EmailStr

    @validator('username')
    def username_must_be_longer_than_2(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return v

class Cart(BaseModel):
    user: User
    items: List[Item]

    @validator('items')
    def items_must_contain_at_least_one_item(cls, v):
        if len(v) < 1:
            raise ValueError('Cart must contain at least one item')
        return v

@app.post("/cart", response_model=Cart)
async def create_cart(cart: Cart):
    return cart

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)