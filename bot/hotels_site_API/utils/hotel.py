class Hotel:

    # TODO: add attribute address

    """
    Класс для представления данных об отеле.

    Атрибуты:
    - name (str): Название отеля.
    - is_available (bool): Свободен ли отель.
    - min_rooms_left (int): Минимальное количество комнат, оставшихся в отеле.
    - picture_url (str): Ссылка на картинку отеля.
    - price_per_night (float): Цена за ночь в отеле.
    - total_price (float): Общая цена (включая налоги и сборы).
    - reviews_count (int): Количество отзывов об отеле.
    - reviews_score (float): Оценка отелю, если есть отзывы.
    - destination_info (str): Информация о расстоянии от центра города.
    - id (int): Уникальный идентификатор отеля.

    Методы:
    - __str__(): Возвращает строковое представление отеля с основной информацией.

    Пример использования:
    hotel = Hotel(
        name="Отель ABC",
        is_available=True,
        min_rooms_left=5,
        picture_url="https://example.com/hotel.jpg",
        price_per_night=150.0,
        total_price=200.0,
        reviews_count=50,
        reviews_score=4.5,
        destination_info="3 мили от центра",
        id=12345
    )

    print(hotel)  # Выводит информацию об отеле в читаемом формате.
    """

    def __init__(self, name: str, is_available: bool, min_rooms_left: int, picture_url: str, price_per_night: float,
                 total_price: float, reviews_count: int, reviews_score: float, destination_info: str, id: int):
        self._name = name
        self._is_available = is_available
        self._min_rooms_left = min_rooms_left
        self._picture_url = picture_url
        self._price_per_night = price_per_night
        self._total_price = total_price
        self._reviews_count = reviews_count
        self._reviews_score = reviews_score
        self._destination_info = destination_info
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def is_available(self):
        return self._is_available

    @is_available.setter
    def is_available(self, value):
        self._is_available = value

    @property
    def min_rooms_left(self):
        return self._min_rooms_left

    @min_rooms_left.setter
    def min_rooms_left(self, value):
        self._min_rooms_left = value

    @property
    def picture_url(self):
        return self._picture_url

    @picture_url.setter
    def picture_url(self, value):
        self._picture_url = value

    @property
    def price_per_night(self):
        return self._price_per_night

    @price_per_night.setter
    def price_per_night(self, value):
        self._price_per_night = value

    @property
    def total_price(self):
        return self._total_price

    @total_price.setter
    def total_price(self, value):
        self._total_price = value

    @property
    def reviews_count(self):
        return self._reviews_count

    @reviews_count.setter
    def reviews_count(self, value):
        self._reviews_count = value

    @property
    def reviews_score(self):
        return self._reviews_score

    @reviews_score.setter
    def reviews_score(self, value):
        self._reviews_score = value

    @property
    def destination_info(self):
        return self._destination_info

    @destination_info.setter
    def destination_info(self, value):
        self._destination_info = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def __getitem__(self, index):
        attributes = [
            self._name, self._is_available, self._min_rooms_left,
            self._picture_url, self._price_per_night, self._total_price,
            self._reviews_count, self._reviews_score, self._destination_info,
            self._id
        ]
        return attributes[index]

    def __str__(self):

        """
        Возвращает строковое представление отеля с основной информацией.

        Returns:
            str: Строка с данными об отеле.
        """

        return (
            'Название отеля: {name}\n'
            'Свободен: {available};\t Минимальное количество комнат: {minRoom}\n'
            'Ссылка на картинку: {picture}\n'
            'Цена за ночь: {price_per_night}\n'
            'Общая цена (including taxes & fees) {total_price}\n'
            'Отзывов: {reviews}\n'
            'Оценка: {score}\n'
            'Дистанция от центра города: {distanceMes} миль\n'
            'Hotel ID: {id}'
        ).format(
            name=self.name,
            available=self.is_available, minRoom=self.min_rooms_left,
            picture=self.picture_url,
            price_per_night=round(self.price_per_night, 1),
            total_price=self.total_price,
            reviews=self.reviews_count,
            score=self.reviews_score,
            distanceMes=self.destination_info,
            id=self.id
        )


