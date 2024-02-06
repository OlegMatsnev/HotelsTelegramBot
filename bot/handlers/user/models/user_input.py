class UserInput:
    def __init__(self, arrival_year: int = 0, arrival_month: int = 0, arrival_day: int = 0,
                 dep_year: int = 0, dep_month: int = 0, dep_day: int = 0, city: str = ''):
        self._arrival_year = arrival_year
        self._arrival_month = arrival_month
        self._arrival_day = arrival_day
        self._dep_year = dep_year
        self._dep_month = dep_month
        self._dep_day = dep_day
        self._city = city

    @property
    def arrival_year(self):
        return self._arrival_year

    @arrival_year.setter
    def arrival_year(self, value):
        self._arrival_year = value

    @property
    def arrival_month(self):
        return self._arrival_month

    @arrival_month.setter
    def arrival_month(self, value):
        self._arrival_month = value

    @property
    def arrival_day(self):
        return self._arrival_day

    @arrival_day.setter
    def arrival_day(self, value):
        self._arrival_day = value

    @property
    def dep_year(self):
        return self._dep_year

    @dep_year.setter
    def dep_year(self, value):
        self._dep_year = value

    @property
    def dep_month(self):
        return self._dep_month

    @dep_month.setter
    def dep_month(self, value):
        self._dep_month = value

    @property
    def dep_day(self):
        return self._dep_day

    @dep_day.setter
    def dep_day(self, value):
        self._dep_day = value

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        self._city = value

    def to_dict(self):
        return {
            'checkInDate': {
                'year': self._arrival_year,
                'month': self._arrival_month,
                'day': self._arrival_day,
            },
            'checkOutDate': {
                'year': self._dep_year,
                'month': self._dep_month,
                'day': self._dep_day,
            },
            'city': self._city,
        }
