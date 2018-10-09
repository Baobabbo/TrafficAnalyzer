class Car:
    def __init__(self):
        self.carID = None
        self.numFrames = 0
        self.calcSpeed = None
        self.arrayImmagini = []
        self.carDispColor = None
        self.position = [None, None]
        self.in_area = None

    def setCarID(self, ID):
        self.carID = ID

    def setNumFrames(self, number):
        self.numFrames = number

    def addImage(self, immagine):
        self.arrayImmagini.append(immagine)

    def setCarColor(self, color):
        self.carDispColor = color

    def incNumFrames(self):
        self.numFrames = self.numFrames + 1

    def set_in_area(self):
        self.in_area = 1

    def clear_in_area(self):
        self.in_area = 0

    def set_position(self, x, y):
        self.position[0] = x
        self.position[1] = y