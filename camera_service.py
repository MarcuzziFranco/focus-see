import cv2
import threading

class CameraService:
    
    def __init__(self):
        print("Init camera service")
        self.camera_thread = None
        self.capture_enable = False
        self.cap = cv2.VideoCapture(0)
        self.lock = threading.Lock()

    def create_thread(self):
        self.camera_thread = threading.Thread(target=self.camera_thread_run)
        self.camera_thread.start()

    def camera_thread_run(self):
        print("Run camera")
        
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: No se puede abrir la cámara")
            return

        while True:
            if self.capture_enable:
                ret, frame = cap.read()
                if not ret:
                    print("Error: No se puede recibir el frame (se ha finalizado el stream?)")
                    break
                cv2.imshow('frame', frame)
            else:
                cv2.destroyAllWindows()
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def capture_start(self):
        with self.lock:
            print("capture enable")
            self.capture_enable = True

    def capture_stop(self):
        with self.lock:
            print("capture disable")
            self.capture_enable = False

    def stop(self):
        self.capture_stop()
        if self.camera_thread is not None:
            self.camera_thread.join()
