class currentStatus:
    def __init__(self):
        self.currFilename=None   # path del videofile da caricare ed analizzare
        self.tempFilename=None   # path del videofile da salvare/immagini elaborate
        self.currWindowSize=[None,None]   # array contenente la dimensione corrente della finestra
                                     # del programma principale
        self.puntiRetta=[point(),point()] # lista dei punti che sono stati impostati

        self.file_is_set = 0    # default a non settato
        self.video_state = 0    # default a pausa
        self.veichles_array = []

    def setCurrFilename(self,stringa):
        self.currFilename = stringa

    def setTempFilename(self,stringa):
        self.tempFilename = stringa

    def getCurrWindowSize(self):
        return self.currentStatus

    def setCurrWindowSize(self, height, width):

        self.currWindowSize[0] = height
        self.currWindowSize[1] = width

    def set_file_is_set(self,value):
        self.file_is_set=value

    def get_file_is_set(self):
        return self.file_is_set

    def set_video_state(self, value):
        self.video_state = value

class point:
    def __init__(self):
        self.x=None
        self.y=None
    def setPoint(self,x,y):
        self.x=x
        self.y=y
    def checkEmptyPoint(self):
        if self.x is None and self.y is None:
            print("Il punto è nullo")
            return 1
        else:
            return 0
