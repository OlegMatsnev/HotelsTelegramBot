from bot.hotels_site_API.utils.hotel import Hotel
from .user_input import UserInput
from .user_room import Room


class User:
    def __init__(self, name: (str, None) = None, telegram_id: int = None,
                 rooms: list[Room] = [], input_data: UserInput = None, hotels: list[Hotel] = []):
        self._name = name
        self._telegram_id = telegram_id
        self._rooms = rooms
        self._input_data = input_data
        self._hotels = hotels

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def telegram_id(self):
        return self._telegram_id

    @telegram_id.setter
    def telegram_id(self, value):
        self._telegram_id = value

    @property
    def rooms(self):
        return self._rooms

    @rooms.setter
    def rooms(self, value):
        self._rooms = value

    @property
    def input_data(self):
        return self._input_data

    @input_data.setter
    def input_data(self, value):
        self._input_data = value

    @property
    def hotels(self):
        return self._hotels

    @hotels.setter
    def hotels(self, value):
        self._hotels = value

    def add_room(self, room: Room):
        """Add a room to the list of rooms."""
        self._rooms.append(room)

    def update_room(self, index: int, room: Room):
        """Update a room in the list based on its index."""
        if 0 <= index < len(self._rooms):
            self._rooms[index] = room
        else:
            raise IndexError("Index out of range")

    def get_rooms_list(self):
        return [room.to_dict() for room in self._rooms]

    # convert user data for db methods
    def convert_to_dicts_list(self):
        # user_data ->
        # [
        #   {'checkInDate': {'year': 2024, 'month': 5, 'day': 14}},
        #   {'checkOutDate': {'year': 2024, 'month': 9, 'day': 20}},
        #   {'city': 'Ottawa'},
        #   {'rooms': [{'adults': '2', 'children': '2'}, {'adults': '2', 'children': '1'}, {}]}
        # ]
        user_data = [self._input_data.to_dict(), self.get_rooms_list()]
        return user_data

