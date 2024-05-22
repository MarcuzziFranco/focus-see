from asyncio.windows_events import NULL
import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import numpy as np
from mediapipe.tasks.python import vision
import os


PATH_MODEL = '' #Get path absolute
MID_FOREHEAD = 10
EYE_LEFT_INDEX = 468
EYE_RIGHT_INDEX = 473
NOSE_INDEX = 4
JAW = 152

COLOR = (0, 255, 0)  # Verde
THICKNESS = 2
   
class FaceDetection():

    def __init__(self):
        self.model_path = self.load_model_file() 
        # Import class mediapipe
        self.BaseOptions = mp.tasks.BaseOptions
        self.FaceLandmarker = mp.tasks.vision.FaceLandmarker
        self.FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
        self.FaceLandmarkerResult = mp.tasks.vision.FaceLandmarkerResult
        self.VisionRunningMode = mp.tasks.vision.RunningMode
        self.options = self.load_options_detector()
        self.landmarker = self.FaceLandmarker.create_from_options(self.options)
        self.frame_detected = None

    def load_model_file(self):
        # check exist file model
        if not os.path.isfile(PATH_MODEL):
            print(f"Error: El archivo del modelo no se encuentra en {PATH_MODEL}")
            exit()
        print("Archivo del modelo encontrado.")
        return PATH_MODEL

    def load_options_detector(self):
        # Load option detector
        options = self.FaceLandmarkerOptions(
            base_options=self.BaseOptions(model_asset_path=self.model_path),
            running_mode=self.VisionRunningMode.LIVE_STREAM,
            result_callback=self.print_result
        )
        return options

    def prosssing_frame(self,frame,cap):
        # Convert the frame OpenCV  in to MediaPipe
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        # Get current time.
        timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))

        # Process the image landmarker detector.
        self.landmarker.detect_async(mp_image, timestamp_ms)

    # Callback get result detector.
    def print_result(self,face_detection_result, input_image, timestamp_ms): 

        try:
            # Convert  mp.Image to numpy array
            frame_to_prossesing = input_image
            frame_to_prossesing = frame_to_prossesing.numpy_view()

            # Make a copy of the array so that it is not read-only
            frame_to_prossesing = frame_to_prossesing.copy()
            
            # Cycle through each detection in the results
            for landmarks in face_detection_result.face_landmarks:
               self.draw_point_image(frame_to_prossesing,landmarks)
            
            self.frame_detected = frame_to_prossesing

        except Exception as e:
            print(e) 

    def draw_point_image(self,image, landmarks):
        nose = landmarks[NOSE_INDEX]
        left_eye = landmarks[EYE_LEFT_INDEX]
        right_eye = landmarks[EYE_RIGHT_INDEX]
        mouth = landmarks[JAW]
        forehead = landmarks[MID_FOREHEAD]
                
        # Convert normalized coordinates to absolute
        h, w, _ = image.shape
        nose = int(nose.x * w), int(nose.y * h)
        left_eye = int(left_eye.x * w), int(left_eye.y * h)
        right_eye = int(right_eye.x * w), int(right_eye.y * h)
        mouth = int(mouth.x * w), int(mouth.y * h)
        forehead = int(forehead.x * w), int(forehead.y * h)
                
        # Draw points
        cv2.circle(image, nose, 5, COLOR, THICKNESS)
        cv2.circle(image, left_eye, 5, COLOR, THICKNESS)
        cv2.circle(image, right_eye, 5, COLOR, THICKNESS)
        cv2.circle(image, mouth, 5, COLOR, THICKNESS)
        cv2.circle(image, forehead, 5, COLOR, THICKNESS)

    def get_frame_detected(self):
        return self.frame_detected   
    
    

   
   


   

   