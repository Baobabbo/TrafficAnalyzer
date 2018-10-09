# tutti gli imports necessari
from tkinter import *
from tkinter.filedialog import askopenfilename

import cv2 as cv

import programStatus
import videoUtil
import yolo_object_detection
# da spostare in program status
filename=""
status=programStatus.currentStatus()
fileFormat=[".avi", ".mp4", ".mov", ".mkv", ".vid"]
def apriFileVideo():
    print("Selezione del file video in corso")
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    print(filename)
    for f in fileFormat:
        if f in filename:
            # TODO: fare una funzione che uccide il vecchio filmato se la path è stata cambiata
            status.setCurrFilename(filename)
            status.set_file_is_set(1)
            avvioFrameVideo(filename)
            return
    print("Errore: il file specificato non è un file video supportato")
def controllaFile():
    print(status.get_file_is_set())
    if status.get_file_is_set() == 1:
        refreshedStatus = yolo_object_detection.vehicle_detection(video_path= status.currFilename)
        print("eseguito")

def avvioFrameVideo(filename):
    print("Ho ricevuto ")
    print(filename)
    if filename != "":
        # se la stringa filename non è vuota allora display thumbnail e apri
        # una dialog box con la guida per quello che deve essere fatto (selezionare)
        # (il percorso da analizzare della macchina e fornire una distanza...FPS???)
        print("Apro il video")
        cap = cv.VideoCapture(filename)
        subFrame = videoUtil.video_util_frame(parent=video_frame, vs=cap, controller=status)
        subFrame.pack()
    else:
        print("Il nome del file video non era valido")
def toggleVideoPlayback():
    print("Avvio/Pausa video")
    if status.get_file_is_set() == 1:
        if status.video_state == 0:    # se è in pausa play
            status.set_video_state(1)
        else:
            status.set_video_state(0) # metto in pausa


# impostazioni base della finastra principale
master = Tk()
master.title("Traffic Analyzer")
master.minsize(width=1360, height=760) # HD 1366x768
# frame contenente i pulsanti del menù
menu_frame=Frame(master)
button_OpenFile = Button(menu_frame, text="Prova di un pulsante", command=apriFileVideo)
openIcon=PhotoImage(file="apri.png")
button_OpenFile.pack(padx=10,pady=10,side=LEFT)
button_OpenFile.config(image=openIcon)
button_SaveVideo=Button(menu_frame, text="Salva Video")# funzione da implementare
button_SaveVideo.pack(padx=10,pady=10,side=LEFT)
button_SaveGraph=Button(menu_frame,text="Salva Grafico") # funzione ancora da implementare
button_SaveGraph.pack(padx=10,pady=10,side=LEFT)
menu_frame.pack(fill=X) # così da riempire la finestra per tutto l'asse X

video_frame=Frame(master)
#debug=Label(video_frame,text="Questo è il frame dove deve essere riprodotto il video")
#debug.pack()

# creo un sub-frame dove metto i pulsanti per l'interazione con il video
vid_menu_frame=Frame(video_frame)
button_play_pause=Button(vid_menu_frame,text="Play Video", command=toggleVideoPlayback)
button_frameSkip=Button(vid_menu_frame,text="Next Frame")
button_prevFrame=Button(vid_menu_frame,text="Previous Frame")
playIcon=PhotoImage(file="playButton.png")
pauseIcon=PhotoImage(file="pauseButton.png")
skipIcon=PhotoImage(file="frameSkip.png")
button_play_pause.config(image=playIcon)
button_frameSkip.config(image=skipIcon)
button_play_pause.pack(padx=10,pady=10,side=LEFT)
button_frameSkip.pack(padx=10,pady=10,side=LEFT)
button_prevFrame.pack(padx=10,pady=10,side=LEFT)
button_compute= Button(vid_menu_frame, text="Computa Video", command=controllaFile)
button_compute.pack(padx=10, pady=10, side=LEFT)

vid_menu_frame.pack(side=BOTTOM)
#video_frame.configure(background="#404040")

video_frame.pack()
video_frame.pack(fill=BOTH,side=LEFT)

# bisogna inserire un frame per lo scorrimento del video in fondo
# sulla destra invece deve essere inserito un frame con il grafico delle velocità


mainloop()
