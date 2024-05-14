import cv2
import threading
import queue
import time

# Cola para los comandos
command_queue = queue.Queue()

# Variable global para controlar la cámara
capture_enabled = True

def camera_thread():
    global capture_enabled
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: No se puede abrir la cámara")
        return

    while True:
        if capture_enabled:
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

def command_thread():
    global capture_enabled

    while True:
        command = input("Ingrese comando: ")
        command_queue.put(command)
        if command == "exit":
            break

def process_commands():
    global capture_enabled

    while True:
        command = command_queue.get()
        if command == "exit":
            break
        elif command == "start":
            capture_enabled = True
            print("Captura de cámara activada")
        elif command == "stop":
            capture_enabled = False
            print("Captura de cámara desactivada")
        else:
            print(f"Comando desconocido: {command}")

if __name__ == "__main__":
    # Crear hilos para la cámara y para los comandos
    camera_t = threading.Thread(target=camera_thread)
    command_t = threading.Thread(target=command_thread)

    # Iniciar los hilos
    camera_t.start()
    command_t.start()

    # Procesar comandos en el hilo principal
    process_commands()

    # Esperar que los hilos terminen
    command_t.join()
    camera_t.join()

    print("Programa terminado")
