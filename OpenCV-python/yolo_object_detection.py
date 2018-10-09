# import necessary packages
# import cvlib as cv
# from cvlib.object_detection import draw_bbox
import obj_det as cv
from obj_det import draw_bbox
import cv2


def vehicle_detection(video_path):
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
            exit()

        # apply object detection
        bbox, label, conf = cv.detect_common_objects(frame, vehicle)

        print(bbox, label, conf)

        # draw bounding box over detected objects
        out = draw_bbox(frame, bbox, label, conf)

        # display output
        cv2.imshow("Real-time object detection", frame)

        # press "Q" to stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # release resources
    videoCap.release()
    cv2.destroyAllWindows()
    return
