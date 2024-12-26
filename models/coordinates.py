class Coordinates:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __iter__(self):
        iters = dict((x, y) for x, y in Coordinates.__dict__.items() if x[:2] != '__')
        iters.update(self.__dict__)

        for x, y in iters.items():
            yield x, y
