class bounding_box:
    def __init__(self, west=0, south=0, east=0, north=0):
        self.west = west
        self.south = south
        self.east = east
        self.north = north

    def __repr__(self):
        return (
                    f'bounding_box(west = {self.west}, '
                    f'south = {self.south}, '
                    f'east = {self.east}, '
                    f'north = {self.north})'
                )
    @property
    def west(self):
        return self.__west

    @west.setter
    def west(self, west):
        if west < -180:
            self.__west = -180
        elif west > 180:
            self.__west = 180
        else:
            self.__west = west

    @property
    def east(self):
        return self.__east

    @east.setter
    def east(self, east):
        if east < -180:
            self.__east = -180
        elif east > 180:
            self.__east = 180
        else:
            self.__east = east
    
    @property
    def south(self):
        return self.__south

    @south.setter
    def south(self, south):
        if south < -90:
            self.__south = -90
        elif south > 90:
            self.__south = 90
        else:
            self.__south = south

    @property
    def north(self):
        return self.__north

    @north.setter
    def north(self, north):
        if north < -90:
            self.__north = -90
        elif north > 90:
            self.__north = 90
        else:
            self.__north = north

    @staticmethod
    def novi_small():
        return bounding_box(west=-83.468632963415, south=42.4712742373734, east=-83.41732101680651, north=42.49869234613597)

    @staticmethod
    def novi_large():
        return bounding_box(west=-83.5532633226741, south=42.43302319281859, east=-83.34810089153233, north=42.51656225087703)

    @staticmethod
    def paf():
        return bounding_box(west=11.477553225690132, south=48.521238923077085, east=11.485313186246147, north=48.52532145934347)
