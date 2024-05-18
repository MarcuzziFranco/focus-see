import threading
import cv2

class CameraServiceThread(threading.Thread):
    
    def __init__(self,running):
        threading.Thread.__init__(self,name="camera",target=self.thread_camera)
        self.run_thread_camera = running
        self.was_turned_off = False
        self.cap = cv2.VideoCapture(0)

    def thread_camera(self):
        while True:
            while self.run_thread_camera:
                self.create_camera_window()
            if not self.was_turned_off:
                self.was_turned_off = True
                self.destroy_camera_window()
                
    
    def enable(self):
        if self.run_thread_camera:
            print("The camera is already running")
        else: 
            self.run_thread_camera = True
            self.cap = cv2.VideoCapture(0)
            print("Camera enable")
    
    def disable(self):
        if not self.run_thread_camera:
            print("The camera already off")
        else:
            self.run_thread_camera = False
            self.was_turned_off = False
            print("Camera disable")
    
    def create_camera_window(self):
        ret, frame = self.cap.read()
        if ret:
            cv2.imshow('Camera', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.capture_stop()
            elif not self.cap.isOpened():
                print("Error: No se puede abrir la cámara")
        
    def destroy_camera_window(self):
        self.cap.release()
        cv2.destroyAllWindows()
