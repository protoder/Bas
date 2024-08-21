import cv2
import numpy as np

# Загрузка видео
cap = cv2.VideoCapture('video.mp4')

# Загрузка весов модели YOLOv3
net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')

# Получение списка имен классов
classes = []
with open('coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Определение цветов для каждого класса
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Проход по кадрам видео
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Обнаружение объектов на кадре с помощью YOLO
    blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(net.getUnconnectedOutLayersNames())
    boxes = []
    confidences = []
    class_ids = []
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                w = int(detection[2] * frame.shape[1])
                h = int(detection[3]
                x = center_x - w // 2
                y = center_y - h // 2
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

                # Отслеживание найденных объектов
                indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
                for i in indices:
                    i = i[0]
                box = boxes[i]
                x, y, w, h = box
                label = f'{classes[class_ids[i]]}: {confidences[i]:.2f}'
                color = colors[class_ids[i]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # Отображение результата на видео
                cv2.imshow('Object Tracking', frame)
                if cv2.waitKey(1) == ord('q'):
                    break

                cap.release()
                cv2.destroyAllWindows()
