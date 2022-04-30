from tortoise import fields
from tortoise.models import Model


class UserORM(Model):
    id = fields.IntField(pk=True, generated=True)
    first_name = fields.CharField(max_length=64)
    last_name = fields.CharField(max_length=64)
    mobile_number = fields.TextField()
    country_code = fields.SmallIntField()
    verified = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "Users"


class OTPORM(Model):
    user = fields.ForeignKeyField(
        model_name="app.UserORM", on_delete="CASCADE")
    code = fields.IntField()
    expiry = fields.DatetimeField()

    class Meta:
        table = "Users_OTP"


class BankORM(Model):
    id = fields.IntField(pk=True, generated=True)
    user = fields.ForeignKeyField("app.UserORM", on_delete="CASCADE")
    first_name = fields.CharField(max_length=128)
    last_name = fields.CharField(max_length=128)
    father_name = fields.CharField(max_length=128)
    date_of_birth = fields.DateField()
    permanent_address = fields.TextField()
    current_address = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "Users_banks"
