# YOLO Object Detection with Flask and Firebase

This project demonstrates how to use YOLOv3 (You Only Look Once) for real-time object detection on images stored in Firebase Cloud Storage. It utilizes a Flask server (`app.py`) to serve the processed video stream with detected objects and provides a web interface to view the video feed. Additionally, it includes a script (`espsender.py`) to capture images from a URL and upload them to Firebase.

## Project Overview

- **Object Detection**: Uses YOLOv3 to detect objects in images.
- **Firebase Integration**: Uploads and retrieves images from Firebase Cloud Storage.
- **Flask Web Server**: Hosts a web interface to display the video feed with detected objects.
- **Image Capture and Upload**: Captures images from a URL and uploads them to Firebase.
- **Real-time Processing**: Processes images and updates the video feed in real-time.

## Features

- Real-time object detection using YOLOv3.
- Integration with Firebase for storing and retrieving images.
- Web-based video feed with detected objects highlighted.
- Efficient object detection with Non-Maximum Suppression (NMS).
- Captures and uploads images from a specified URL.

## Installation

### Prerequisites

- Python 3.x
- Flask
- OpenCV
- Firebase Admin SDK
- YOLOv3 weights and configuration files

## Install dependancies:
pip install flask opencv-python firebase-admin numpy

## Download YOLOv3 files:
Download yolov3.cfg, yolov3.weights, and coco.names from the YOLO website and place them in the project director

## Configure Firebase:
Obtain your Firebase Admin SDK JSON file and replace the placeholder in app.py:
cred = credentials.Certificate('path/to/your/firebase-adminsdk.json')
Replace 'Your-project-id.appspot.com' with your actual Firebase Storage bucket URL.

## Configure the Image Capture Script:
Update the URL in espsender.py with the URL of your image source:
url = 'http://your-camera-ip/cam-hi.jpg'
Replace 'path/to/your/firebase-adminsdk.json' and 'Your-project-id.appspot.com' with your actual values.
