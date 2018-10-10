# import necessary packages
# import cvlib as cv
# from cvlib.object_detection import draw_bbox
import obj_det as cv
from obj_det import draw_bbox
from centroidTracker import CentroidTracker
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2

def vehicle_detection(video_path):
    # inizializzazione globale del tracker
    global ct
    ct = CentroidTracker()
    # open videoCap
    videoCap = cv2.VideoCapture(video_path)
    vehicle = []
    if not videoCap.isOpened():
        print("Could not open videoCap")
        exit()

    # loop through frames
    while videoCap.isOpened():

        # read frame from videoCap
        status, frame = videoCap.read()

        if not status:
            print("Could not read frame")
            break
            #exit()

        # apply object detection
        bbox, label, conf, aux = cv.detect_common_objects(frame, vehicle)
        vehicle = aux
        print(bbox, label, conf)
        # print("Veicolo in coordinate ",vehicle)
        # draw bounding box over detected objects
        out = draw_bbox(frame, bbox, label, conf)
        performTracking(bbox,label)
        # display output
        cv2.imshow("Real-time object detection", frame)

        # press "Q" to stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # release resources
    videoCap.release()
    cv2.destroyAllWindows()
    return

def performTracking(bbox, label):
    for z, b in enumerate(bbox):
        print(label[z])
        if label[z] == "car":

            print("[TRACKING] Chiamo l'update su ct con i label ", label[z])
            print(bbox[z])
            aux = [bbox[z]]
            objects = ct.update(aux)

            # loop over the tracked objects
            for (objectID, centroid) in objects.items():
                print("[TRACKING] gli oggetti aggiornati hanno: ", objectID, centroid)