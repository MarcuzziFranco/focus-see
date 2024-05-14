import json
from command import Command
from camera_service import CameraService

commands = []
commands_map = {}

camera_service = CameraService()


def initialice_camera_thread():
    print("Initialice thread camera...")
    camera_service.create_thread()

def command_start_camera():
    camera_service.capture_start()

def command_stop_camera():
    camera_service.capture_stop()

functions = {
    "start_camera": command_start_camera,
    "stop_camera": command_stop_camera
}

# Cargar archivo de comandos y asignar funciones a comandos
def load_command_file():
    with open('commands.json', 'r') as file:
        data = json.load(file)

    for command_data in data["commands"]:
        name = command_data["name"]
        func_name = command_data["function"]
        command = Command(code=name, execute=functions[func_name])
        commands.append(command)
    
    for cmd in commands:
        commands_map[cmd.code] = cmd

def execute_command(command_name):
    if command_name in commands_map:
        commands_map[command_name].run()
    else:
        print(f"Command '{command_name}' not found")

def main():
    print("Init focus-see!")

    load_command_file()

    initialice_camera_thread()  # Inicializa el hilo de la cámara desde el principio

    try:
        while True:
            user_input = input("Enter a command: ")
            if user_input.lower() == "exit":
                break
            execute_command(user_input)
    except KeyboardInterrupt:
        pass
    finally:
        camera_service.stop()

def finish_program():
    print("finished program")

if __name__ == "__main__":
   main()
   finish_program()


