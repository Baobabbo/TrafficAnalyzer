import numpy as np
import cv2


yolo_config_file = "./object-detection-opencv/yolov3.cfg"
yolo_weights = "./object-detection-opencv/yolov3.weights"
yolo_classes = "./object-detection-opencv/yolov3.txt"

def get_output_layers(net):
    print("[INFO] ottengo i nomi dei layers")
    layer_names = net.getLayerNames()
    print(layer_names)
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers

def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# def postprocess(self,frame, outs, confThreshold, nmsThreshold, classes, net):
#     frameHeight = frame.shape[0]
#     frameWidth = frame.shape[1]
#
#     def drawPred(classId, conf, left, top, right, bottom):
#         # Draw a bounding box.
#         cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0))
#
#         label = '%.2f' % conf
#
#         # Print a label of class.
#         if classes:
#             assert(classId < len(classes))
#             label = '%s: %s' % (classes[classId], label)
#
#         labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
#         top = max(top, labelSize[1])
#         cv2.rectangle(frame, (left, top - labelSize[1]), (left + labelSize[0], top + baseLine), (255, 255, 255), cv.FILLED)
#         cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
#
#     layerNames = net.getLayerNames()
#     lastLayerId = net.getLayerId(layerNames[-1])
#     lastLayer = net.getLayer(lastLayerId)
#
#     classIds = []
#     confidences = []
#     boxes = []
#     if net.getLayer(0).outputNameToIndex('im_info') != -1:  # Faster-RCNN or R-FCN
#         # Network produces output blob with a shape 1x1xNx7 where N is a number of
#         # detections and an every detection is a vector of values
#         # [batchId, classId, confidence, left, top, right, bottom]
#         for out in outs:
#             for detection in out[0, 0]:
#                 confidence = detection[2]
#                 if confidence > confThreshold:
#                     left = int(detection[3])
#                     top = int(detection[4])
#                     right = int(detection[5])
#                     bottom = int(detection[6])
#                     width = right - left + 1
#                     height = bottom - top + 1
#                     classIds.append(int(detection[1]) - 1)  # Skip background label
#                     confidences.append(float(confidence))
#                     boxes.append([left, top, width, height])
#     elif lastLayer.type == 'DetectionOutput':
#         # Network produces output blob with a shape 1x1xNx7 where N is a number of
#         # detections and an every detection is a vector of values
#         # [batchId, classId, confidence, left, top, right, bottom]
#         for out in outs:
#             for detection in out[0, 0]:
#                 confidence = detection[2]
#                 if confidence > confThreshold:
#                     left = int(detection[3] * frameWidth)
#                     top = int(detection[4] * frameHeight)
#                     right = int(detection[5] * frameWidth)
#                     bottom = int(detection[6] * frameHeight)
#                     width = right - left + 1
#                     height = bottom - top + 1
#                     classIds.append(int(detection[1]) - 1)  # Skip background label
#                     confidences.append(float(confidence))
#                     boxes.append([left, top, width, height])
#     elif lastLayer.type == 'Region':
#         # Network produces output blob with a shape NxC where N is a number of
#         # detected objects and C is a number of classes + 4 where the first 4
#         # numbers are [center_x, center_y, width, height]
#         classIds = []
#         confidences = []
#         boxes = []
#         for out in outs:
#             for detection in out:
#                 scores = detection[5:]
#                 classId = np.argmax(scores)
#                 confidence = scores[classId]
#                 if confidence > confThreshold:
#                     center_x = int(detection[0] * frameWidth)
#                     center_y = int(detection[1] * frameHeight)
#                     width = int(detection[2] * frameWidth)
#                     height = int(detection[3] * frameHeight)
#                     left = int(center_x - width / 2)
#                     top = int(center_y - height / 2)
#                     classIds.append(classId)
#                     confidences.append(float(confidence))
#                     boxes.append([left, top, width, height])
#     else:
#         print('Unknown output layer type: ' + lastLayer.type)
#         exit()
#
#     indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
#     for i in indices:
#         i = i[0]
#         box = boxes[i]
#         left = box[0]
#         top = box[1]
#         width = box[2]
#         height = box[3]
#         drawPred(classIds[i], confidences[i], left, top, left + width, top + height)

# TODO : devo feeddare al programma dei frame => args da cambiare
def compute_video_file(video):
    print("[INFO] Sto aprendo il video con indirizzo : %s",video)
    # apro il video e leggo un fotogramma
    stream = cv2.VideoCapture(video)
    succes, image = stream.read()
    if not succes:
        return
    #image = cv2.imread(args.image)
    scale = 0.00392
    #test = cv2.imread(video)
    width = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))  # float
    height = int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float
    length = int(stream.get(cv2.CAP_PROP_FRAME_COUNT)) # mi restituisce il numero di frame del video
    fps = stream.get(cv2.CAP_PROP_FPS)
    print(width, height, length, fps)
    rgbImg = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # carico e imposto le classi
    print("[INFO] Sto aprendo il file delle classi YOLO")
    classes = None
    if yolo_classes:
        with open(yolo_classes, 'rt') as f:
            print("Leggo una classe Oggetto dal file classi")
            classes = f.read().rstrip('\n').split('\n')

    # with open(yolo_classes, 'r') as f:
    #     print("Leggo una classe e la aggiungo alla lista")
    #     classes = [line.strip() for line in f.readlines()]

    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
    print (rgbImg.shape)    # mi stampa height width e numero canali colori
    print(rgbImg.dtype)
    # leggo la rete neurale di Yolo
    print("[INFO] Leggo il file di rete neurale di YOLO e la configurazione")
    net = cv2.dnn.readNet(yolo_weights, yolo_config_file)


    conf_threshold = 0.5
    nms_threshold = 0.4
    print("[INFO] Creo il blob da processare")
    blob = cv2.dnn.blobFromImage(rgbImg, scale, (width, height), (0, 0, 0), True, crop=False)
    print("[INFO] Processo il blob con la rete neurale")
    net.setInput(blob)
    #net.setNetInputs(blob)
    print("[INFO] Ottengo l'output dalla rete")
    outs = net.forward(get_output_layers(net))
    #outs = net.forward(outNames)
    #postprocess(rgbImg, outs, conf_threshold, nms_threshold, classes, net)
    winName = 'Deep learning object detection in OpenCV'
    cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
    t, _ = net.getPerfProfile()
    label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
    cv2.putText(rgbImg, label, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
    cv2.imshow(winName, rgbImg)

# commento temporaneo
# for out in outs:
#     for detection in out:
#         scores = detection[5:]
#         class_id = np.argmax(scores)
#         confidence = scores[class_id]
#         if confidence > 0.5:
#             # ricavato il centro della detection
#             center_x = int(detection[0] * Width)
#             center_y = int(detection[1] * Height)
#             # ricavate le dimensioni di lunghezza e largh della detection
#             w = int(detection[2] * Width)
#             h = int(detection[3] * Height)
#             x = center_x - w / 2
#             y = center_y - h / 2
#             class_ids.append(class_id)
#             confidences.append(float(confidence))
#             boxes.append([x, y, w, h])
#
# indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
#
# for i in indices:
#     i = i[0]
#     box = boxes[i]
#     x = box[0]
#     y = box[1]
#     w = box[2]
#     h = box[3]
#     draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))
#
# cv2.imshow("object detection", image)
# cv2.waitKey()
#
# cv2.imwrite("object-detection.jpg", image)
# cv2.destroyAllWindows()

# TODO : parte che taglia la foto in corrispondenza della macchina o truck e invia l'immagine all'oggetto macchina corrispondente
# img = cv2.imread("lenna.png")
# crop_img = img[y:y+h, x:x+w]
# cv2.imshow("cropped", crop_img)
# cv2.waitKey(0)
