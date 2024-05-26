from ast import Constant
from constant import constants
import pyautogui
import utils_windows
import win32gui

current_monitor = 0
last_number_monitor = None

class MonitorControl:

    def __init__(self):
        pass

    def getMonitorByPosition(self,x,y,z):
        if y < -10:
            current_monitor = constants.MONITOR_CODE_RIGHT
            self.update_position_mouse_in_monitor(current_monitor)
            text="LEFT"
        elif y > 10:
            current_monitor = constants.MONITOR_CODE_LEFT
            self.update_position_mouse_in_monitor(current_monitor)
            text="RIGHT"
        elif x < -10:
            current_monitor = constants.KEYBOARD
            self.update_position_mouse_in_monitor(current_monitor)
            text="KEYBOARD"
        elif x > 10:
            current_monitor = constants.MONITOR_CODE_UP
            self.update_position_mouse_in_monitor(current_monitor)
            text="UP"
        elif x>-5 and x < 5:
            current_monitor = constants.MONITOR_CODE_CENTER
            text="CENTER"
            self.update_position_mouse_in_monitor(current_monitor)
        else:
            text="UNKNOWN"
        
        return text
    

    def update_position_mouse_in_monitor(self,monitor_number):
        global last_number_monitor
      
        if(monitor_number != 0):
            # Check last_monitor center.
            if monitor_number == last_number_monitor:
                return         
            # Centering coordinates of each monitor
            if monitor_number == 1:
                center_x = 960
                center_y = -540
            elif monitor_number == 2:
                center_x = -1920 + (1920 // 2)
                center_y = (1080 // 2)
            elif monitor_number == 3:
                center_x = (1920 // 2)
                center_y = (1080 // 2)
            elif monitor_number == 4:
                center_x =  1920 + (1920 // 2)
                center_y = (1080 // 2)
            else:
                print("Monitor number not valid")
                return
            
            #Change position mouse to center monitor.
            pyautogui.moveTo(center_x, center_y)
            
            #Update monitor last number.
            last_number_monitor = monitor_number

            #Get current position mouse.
            position_mouse = pyautogui.position()

            #Get windows to behind mouse.
            hwnd_ventana_mouse = utils_windows.get_windows_behind_mouse(position_mouse.x,position_mouse.y)

            #Set focus windows behind mouse
            utils_windows.enable_focus_windows(hwnd_ventana_mouse)

            
    
