from peewee import ForeignKeyField, CharField, DateField
from .base import BaseModel
from .user_db import UserDB


class UserInputDB(BaseModel):
    user_telegram_id = ForeignKeyField(UserDB, to_field="telegram_id", backref="hotels")
    city = CharField(45)
    check_in_date = DateField()
    check_out_date = DateField()

    class Meta:
        db_table = 'user_inputs'
