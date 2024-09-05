class Schedules:
    def __init__(self):
        self.monday = [[] for i in range(15)]
        self.tuesday = [[] for i in range(15)]
        self.wednesday = [[] for i in range(15)]
        self.thursday = [[] for i in range(15)]
        self.friday = [[] for i in range(15)]
        self.saturday = [[] for i in range(4)]
        self.length = 79

    def get_schedule(self):
        return [
            {"monday": self.monday},
            {"tuesday": self.tuesday},
            {"wednesday": self.wednesday},
            {"thursday": self.thursday},
            {"friday": self.friday},
            {"saturday": self.saturday},
        ]
