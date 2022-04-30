from fastapi import Body, FastAPI
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError
from tortoise import Tortoise
import datetime
from models import BankDetails, UserBase, UserPublic, VerifyUser
from db import *
from helpers import *


app = FastAPI()


@app.on_event("shutdown")
async def close_orm():
    await Tortoise.close_connections()

register_tortoise(
    app,
    db_url="sqlite://data.sqlite3",
    modules={"app": ["db"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


def sendOTP(mobile):
    otp = generateOTP()
    print("OTP", otp, "is sent to", mobile)
    return otp


@app.post("/user", response_model=UserPublic)
async def signup(user: UserBase = Body(...)):
    user_db = await UserORM.create(**user.dict())
    otp = sendOTP(f"+{user_db.country_code}{user_db.mobile_number}")
    # Set expiry to 10 mins from now!
    expiry = datetime.datetime.now(
        datetime.timezone.utc) + datetime.timedelta(minutes=10)
    await OTPORM.create(user=user_db, code=otp, expiry=expiry)
    await user_db.save()
    return user_db


@app.post("/user/verify")
async def verify(user_otp: VerifyUser) -> dict:
    otp_db = await OTPORM.get_or_none(user=user_otp.user)
    user_db = await otp_db.user.all()
    # Do not proceed if user has already verified
    if user_db.verified:
        return HTTPNotFoundError(detail="User already verified!")
    # User id is not yet registered
    if otp_db is None:
        return HTTPNotFoundError(detail="User id Not found")
    if user_otp.code != otp_db.code:
        return HTTPNotFoundError(detail="Incorrect OTP entered!")

    if datetime.datetime.now(datetime.timezone.utc) > otp_db.expiry:
        return HTTPNotFoundError(detail="OTP is expired")
    # Verified Successfully
    user_db.verified = True
    await user_db.save()
    return {
        "success": True,
        "form": BankDetails.get_fields()
    }


@app.post("/user/banks")
async def addBank(bank: BankDetails = Body(...)):
    user_db = await UserORM.all().get(id=bank.user)
    bank_db = await BankORM.create(**bank.dict(exclude={"user"}), user=user_db)
    return bank_db
