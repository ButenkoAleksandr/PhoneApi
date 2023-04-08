from fastapi import FastAPI
from pydantic import BaseModel
from redis import Redis


app: FastAPI = FastAPI()
redis: Redis = Redis()


class Data(BaseModel):
    phone: str
    address: str


@app.get("/check_data")
async def check_data(phone: str) -> dict:
    address = redis.get(phone)
    return {"phone": phone, "address": address}


@app.post("/write_data")
async def write_data(data: Data) -> dict[str, str]:
    redis.set(data.phone, data.address)
    return {"message": "Data written successfully"}


@app.put("/update_data")
async def update_data(data: Data) -> dict[str, str]:
    redis.set(data.phone, data.address)
    return {"message": "Data updated successfully"}
