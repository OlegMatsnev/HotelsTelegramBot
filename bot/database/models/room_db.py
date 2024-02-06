from peewee import IntegerField, ForeignKeyField
from .base import BaseModel
from .user_db import UserDB


class RoomDB(BaseModel):
    adults = IntegerField()
    children = IntegerField()
    user_telegram_id = ForeignKeyField(UserDB, to_field="telegram_id", backref="hotels")

    class Meta:
        db_table = 'rooms'
