import os
import firebase_admin
from firebase_admin import credentials, storage
from flask import Flask, Response, render_template
import cv2
import numpy as np

# Firebase initialization
cred = credentials.Certificate("")# path to your firebase admin sdk  
firebase_admin.initialize_app(cred, {
    'storageBucket': 'Your project name.appspot.com'
})
bucket = storage.bucket()

app = Flask(__name__)

# Load YOLOv3 network
yolo_config_path = r"yolov3.cfg"
yolo_weights_path = r"yolov3.weights"
yolo_names_path = r"coco.names"

net = cv2.dnn.readNetFromDarknet(yolo_config_path, yolo_weights_path)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

with open(yolo_names_path, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]


def get_image_files():
    blobs = bucket.list_blobs(prefix='webcam_frames/')
    image_files = [blob.name for blob in blobs]
    return sorted(image_files)


def detect_objects(img):
    height, width = img.shape[:2]
    blob = cv2.dnn.blobFromImage(img, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    detections = net.forward(output_layers)
    
    boxes = []
    confidences = []
    class_ids = []

    # Class IDs for humans and vehicles
    target_classes = [0, 1, 2, 3, 5, 7]# change as per objects you need to detect , refer coco.names for IDs

    for output in detections:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id in target_classes:
                box = detection[0:4] * np.array([width, height, width, height])
                (centerX, centerY, w, h) = box.astype("int")
                x = int(centerX - (w / 2))
                y = int(centerY - (h / 2))
                boxes.append([x, y, int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    
    object_count = 0
    if len(indices) > 0:
        for i in indices.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            color = [int(c) for c in np.random.randint(0, 255, size=(3,))]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            text = f"{classes[class_ids[i]]}: {confidences[i]:.4f}"
            cv2.putText(img, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            object_count += 1

 
    cv2.putText(img, f"Object Count: {object_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return img


def generate():
    image_files = get_image_files()
    for image_file in image_files:
        blob = bucket.blob(image_file)
        image_data = blob.download_as_string()

        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        img = detect_objects(img)

        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
