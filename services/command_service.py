from services.camera_service import CameraServiceThread
from model.command import Command
import threading
import json
import time
import os

class CommandService(threading.Thread):

    def __init__(self,running):
        threading.Thread.__init__(self,name="command",target=self.thread_command)
        self.run_thread_command = running

        # Create thread camera.
        self.cameraServiceThread = CameraServiceThread(False)
        self.cameraServiceThread.start()

        self.path = "./commands.json"
        self.diccionaryCommands = []
        self.bind_diccionary_commands()

        self.load_command_file()

    def bind_diccionary_commands(self):
        self.functionsCommands = {
            "on camera": self.start_camera,
            "off camera": self.stop_camera,
            "cls":self.clear_lines,
            "reset":self.reset_program,
            "exit":self.exit_program,            
            "help":self.print_help_menu
        }       
    
    def start_camera(self):
        self.cameraServiceThread.enable()

    def stop_camera(self):
        self.cameraServiceThread.disable()

    def clear_lines(self):
        os.system('cls' if os.name == 'nt' else 'clear')       
    
    def print_help_menu(self):
        print("----------------------Menu-Commands----------------------")
        print("|                                                       |")
        print(f"-----Command-------------Description---------------------")
        for command in self.diccionaryCommands:
            print (f"|   {command.code:<10}         {command.description:<30}   |")  
            print("---------------------------------------------------------")

    def thread_command(self):
        while self.run_thread_command:
            try:
                user_input = input("#:")
                # execute command.
                self.execute_command(user_input.lower())
            except EOFError as e:
                print(f"Error thread command:{e}")
                break
        print("Close thread command")

    def enable(self):
        self.run_thread_command = True
    
    def disable(self):
        self.run_thread_command = False

    def reset_program(self):
        print("The command is not implemented")

    def exit_program(self):
        print("This program will turn off 1 seg...")
        time.sleep(1)  # Delay of 2 seconds
        os._exit(0)  # Forceful exit

    def get_status_thread_command(self): #deprecate
        return self.run_thread_command
    
    def load_command_file(self):
        try:
            with open(self.path,'r') as file:
                data_json = json.load(file)
                self.builder_command_diccionary(data_json)
        except Exception as e:
            print(f"Error in the command {e} or the activation function was not found")
    
    def builder_command_diccionary(self,jsonRaw):
        for command_data in jsonRaw["commands"]:
            code = command_data["code"]
            description = command_data["description"]
            command = Command(code=code,execute=self.functionsCommands[code],description=description)
            self.diccionaryCommands.append(command)
    
    def execute_command(self,code):
        if code in self.functionsCommands:
            self.functionsCommands[code]()
        else:
            print(f"Command '{code}' not found, use the 'help' command to see command menu")
