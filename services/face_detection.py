import cv2
import mediapipe as mp
import numpy as np
import os
import math
from asyncio.windows_events import NULL
import constant.constants as Constant
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks.python import vision
from monitor_control import MonitorControl

   
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
        self.monitor_control = MonitorControl()

    def load_model_file(self):
        # Check exist file model
        if not os.path.isfile(Constant.PATH_MODEL):
            print(f"Error: Model Ia file not found {Constant.PATH_MODEL}.")
            exit()
        print("File model ia loaded.")
        return Constant.PATH_MODEL

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
               self.calculate_angles_rotation(frame_to_prossesing,landmarks)
            
            self.frame_detected = frame_to_prossesing

        except Exception as e:
            print(e) 

    def calculate_angles_rotation(self,image,landmarks):

        img_h , img_w, img_c = image.shape
        face_2d = []
        face_3d = []

        for idx, lm in enumerate(landmarks):
            if idx == 33 or idx == 263 or idx ==1 or idx == 61 or idx == 291 or idx==199:
                        if idx ==1:
                            nose_2d = (lm.x * img_w,lm.y * img_h)
                            nose_3d = (lm.x * img_w,lm.y * img_h,lm.z * 3000)
                        x,y = int(lm.x * img_w),int(lm.y * img_h)

                        face_2d.append([x,y])
                        face_3d.append(([x,y,lm.z]))


        #Get 2d Coord
        face_2d = np.array(face_2d,dtype=np.float64)

        face_3d = np.array(face_3d,dtype=np.float64)

        focal_length = 1 * img_w

        cam_matrix = np.array([[focal_length,0,img_h/2],
                               [0,focal_length,img_w/2],
                               [0,0,1]])
        distortion_matrix = np.zeros((4,1),dtype=np.float64)

        success,rotation_vec,translation_vec = cv2.solvePnP(face_3d,face_2d,cam_matrix,distortion_matrix)

        #getting rotational of face
        rmat,jac = cv2.Rodrigues(rotation_vec)

        angles,mtxR,mtxQ,Qx,Qy,Qz = cv2.RQDecomp3x3(rmat)

        x = angles[0] * 360
        y = angles[1] * 360
        z = angles[2] * 360
      
        text = self.monitor_control.getMonitorByPosition(x,y,z)
        
        #nose_3d_projection,jacobian = cv2.projectPoints(nose_3d,rotation_vec,translation_vec,cam_matrix,distortion_matrix) # type: ignore

        p1 = (int(nose_2d[0]),int(nose_2d[1]))
        p2 = (int(nose_2d[0] + y*10), int(nose_2d[1] -x *10))

        cv2.line(image,p1,p2,(255,0,0),3)

        cv2.putText(image,text,(20,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),2)
        cv2.putText(image,"x: " + str(np.round(x,2)),(500,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        cv2.putText(image,"y: "+ str(np.round(y,2)),(500,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        cv2.putText(image,"z: "+ str(np.round(z, 2)), (500, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    def get_frame_detected(self):
        return self.frame_detected   
    
    

   
   


   

   