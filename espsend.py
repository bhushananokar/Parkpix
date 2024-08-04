import cv2
import numpy as np
import urllib.request
import firebase_admin
from firebase_admin import credentials, storage
import os

# Firebase initialization
cred = credentials.Certificate() #path to your firbase admin sdk
firebase_admin.initialize_app(cred, {
    'storageBucket': 'Your-project-id.appspot.com'
})
bucket = storage.bucket()

def upload_to_firebase(frame, frame_counter):

    local_file = f'frame_{frame_counter}.jpg'
    cv2.imwrite(local_file, frame)
    
 
    blob = bucket.blob(f'webcam_frames/frame_{frame_counter}.jpg')
    blob.upload_from_filename(local_file)
    
 
    os.remove(local_file)
    print(f'Uploaded frame_{frame_counter}.jpg to Firebase Storage')

def main():
    url = 'http://192.168.83.169/cam-hi.jpg'
    frame_counter = 0

    while True:
    
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        im = cv2.imdecode(imgnp, -1)

        upload_to_firebase(im, frame_counter)
        frame_counter += 1

        cv2.imshow('Image', im)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
