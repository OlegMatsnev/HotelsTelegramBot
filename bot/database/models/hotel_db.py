from peewee import IntegerField, CharField, FloatField, ForeignKeyField
from .base import BaseModel
from .user_db import UserDB


class HotelDB(BaseModel):
    hotel_id = IntegerField()
    name = CharField()
    picture_url = CharField()
    price_per_night = FloatField()
    total_price = FloatField()
    reviews_count = IntegerField()
    reviews_score = FloatField()
    destination_info = FloatField()
    user_telegram_id = ForeignKeyField(UserDB, to_field="telegram_id", backref="hotels")

    class Meta:
        db_table = 'hotels'

    def __str__(self):

        """
        Возвращает строковое представление отеля с основной информацией.

        Returns:
            str: Строка с данными об отеле.
        """

        return (
            'Название отеля: {name}\n'
            'Свободен: Незвестно;\t Минимальное количество комнат: Незвестно\n'
            'Ссылка на картинку: {picture}\n'
            'Цена за ночь: {price_per_night}\n'
            'Общая цена (including taxes & fees) {total_price}\n'
            'Отзывов: {reviews}\n'
            'Оценка: {score}\n'
            'Дистанция от центра города: {distanceMes} миль\n'
            'Hotel ID: {id}'
        ).format(
            name=self.name,
            picture=self.picture_url,
            price_per_night=round(self.price_per_night, 1),
            total_price=self.total_price,
            reviews=self.reviews_count,
            score=self.reviews_score,
            distanceMes=self.destination_info,
            id=self.hotel_id
        )
