# import the necessary packages
from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tk
import threading
import datetime
import imutils
import cv2
import os
import time
import numpy as np
class video_util_frame (tk.Frame):
    # dove vs è il video stream
    # il metodo init inizializza la classe nel momento in cui viene chiamata
    # self è sempre il primo parametro
    def __init__(self,parent,vs, controller):
        tk.Frame.__init__(self,parent)
        self.vs=vs
        self.frame=None
        self.ret=None
        self.thread=None
        self.stopEvent=None
        self.parent=parent
        self.fps = None
        self.controller = controller
        self.panel=None
        print("Sto venendo inizializzato")
        # start a thread that constantly pools the video sensor for
        # the most recently read frame

        self.stopEvent = threading.Event()
        print(self.stopEvent)
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

    # codice per vedere dove ho cliccato sull'area del video aperto
    def callback(self,event):
        print ("clicked at", event.x, event.y)

    def videoLoop(self):
        print("ho chiamato video loop")
        self.fps = self.vs.get(cv2.CAP_PROP_FPS)
        print(self.fps)
        # DISCLAIMER:
        # I'm not a GUI developer, nor do I even pretend to be. This
        # try/except statement is a pretty ugly hack to get around
        # a RunTime error that Tkinter throws due to threading
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # self.pausaRiproduzione()    #si mette subito in pausa da solo
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                self.ret, self.frame = self.vs.read()
                #self.frame = imutils.resize(self.frame, width=500)

                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format

                rgbImg = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                rgbImg = cv2.resize(rgbImg,(906,509),interpolation=cv2.INTER_AREA)
                rgbImg = Image.fromarray(rgbImg)
                rgbImg = ImageTk.PhotoImage(rgbImg)

                # if the panel is not None, we need to initialize it
                if self.panel is None:
                    self.panel = tk.Label(self.parent,image=rgbImg)
                    self.panel.image = rgbImg

                    self.panel.bind("<Button-1>", self.callback)
                    self.panel.pack(side="left", padx=10, pady=10)
                    time.sleep(1/self.fps)
                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=rgbImg)
                    self.panel.image = rgbImg
                    time.sleep(1 / self.fps)
        except RuntimeError:
            print("caught a RunTime Error")

    def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation = inter)

        # return the resized image
        return resized
