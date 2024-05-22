from services.command_service import CommandService
import warnings

# Suppress deprecated specific warning in google.protobuf.symbol_database
warnings.filterwarnings('ignore', category=UserWarning, module='google.protobuf.symbol_database')

commandService = CommandService(True)
commandService.start()

#deprecate
if commandService.get_status_thread_command() == False:
    print("Exit program...")