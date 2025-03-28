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

@app.post("/cart")
def calculate_cart(cart: Cart):
    total_price = sum(item.price for item in cart.items)
    if total_price > 500:
        total_price *= 0.9  # Apply 10% discount
    return {
        "user": cart.user,
        "items": cart.items,
        "total_price": round(total_price, 2)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)