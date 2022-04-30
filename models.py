from datetime import datetime
from xmlrpc.client import Boolean
from pydantic import BaseModel


class AdaptedModel(BaseModel):
    @classmethod
    def get_fields(cls, alias=False):
        fields = cls.schema(alias).get("properties")
        req_fields = cls.schema(alias).get("required")
        field_details = {}
        for idx, (field, value) in enumerate(fields.items()):
            field_details[idx] = {
                "name": field,
                "title": value.get("title"),
                "type": value.get("type"),
                "required": True if field in req_fields else False
            }
        return field_details


class UserBase(BaseModel):
    first_name: str
    last_name: str
    mobile_number: int
    country_code: int


class UserDB(UserBase):
    id: int = 1
    verified: Boolean
    created_at: datetime


class UserPublic(BaseModel):
    id: int
    first_name: str


class VerifyUser(BaseModel):
    uid: int
    code: int


class VerifyDB(VerifyUser):
    expiry: datetime



class BankDetails(AdaptedModel):
    first_name: str
    last_name: str
    father_name: str
    date_of_birth: str
    permanent_address: str
    current_address: str


class BankDetailsDB(BankDetails):
    id: int
    created_at: datetime
