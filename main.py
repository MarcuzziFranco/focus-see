import json
from command import Command

commands = []
commands_map = {}



# Definir las funciones que se usarán en los comandos
def greet_function():
    print("Hello! How are you?")

def farewell_function():
    print("Goodbye! See you soon!")

functions = {
    "greet_function": greet_function,
    "farewell_function": farewell_function
}

# Mapeo de nombres de funciones a objetos de función
def load_command_file():
    with open('commands.json','r') as file:
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


if __name__ == "__main__":
    print("Init focus-see!")
    load_command_file()
    while True:
        user_input = input("Enter a command: ")
        if user_input.lower() == "exit":
            break
        execute_command(user_input)