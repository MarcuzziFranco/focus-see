from services.command_service import CommandService

commandService = CommandService(True)
commandService.start()

if commandService.get_status_thread_command() == False:
    print("Exit program...")