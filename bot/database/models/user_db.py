from peewee import IntegerField, CharField, ForeignKeyField, DateField
from .base import BaseModel


class UserDB(BaseModel):
    telegram_id = IntegerField(unique=True)
    username = CharField(45)

    class Meta:
        db_table = 'users'
