from fastapi import Body, FastAPI
from models import *

app = FastAPI()

print(BankDetails.get_fields())

@app.post("/user")
async def signup(user: UserBase = Body(...)):
    return "signup"


@app.post("/user/verify")
async def verify() -> dict:
    return "Verify user"


@app.post("/user/banks")
async def addBank():
    return "Add bank"