from peewee import Model, SqliteDatabase
from bot.database import db


class BaseModel(Model):
    class Meta:
        database = db
        order_by = 'id'
