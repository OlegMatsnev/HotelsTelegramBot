class Room:
    def __init__(self, adults: int, children: int):
        self._adults = adults
        self._children = children

    @property
    def adults(self):
        return self._adults

    @adults.setter
    def adults(self, value):
        self._adults = value

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = value

    def to_dict(self):
        return {'adults': str(self.adults), 'children': str(self.children)}

    def __str__(self):
        return f"adults: {self.adults}, children: {self.children}"