import win32gui
import win32api
import win32con
import win32com.client

def get_position_mouse():
    return win32api.GetCursorPos()

# Function get windows opens
def enum_windows():
    windows = []
    # set enumerations
    def enum_window(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            windows.append((hwnd, win32gui.GetWindowText(hwnd)))

    win32gui.EnumWindows(enum_window, None)
    return windows

# Function get current positon mouse
def get_windows_behind_mouse(x_mouse,y_mouse):
    #x_mouse, y_mouse = obtener_posicion_mouse()
    for hwnd, _ in enum_windows():
        rect = win32gui.GetWindowRect(hwnd)
        if rect[0] <= x_mouse <= rect[2] and rect[1] <= y_mouse <= rect[3]:
            return hwnd

# Disable focus windows
def disable_focus_windows(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)
    win32gui.SetForegroundWindow(hwnd)

# Enable focus windows
def enable_focus_windows(hwnd):
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(hwnd)

# Print name windows
def get_name_windows(self,hwnd_windows_mouse):
    if hwnd_windows_mouse:
        titulo_ventana_mouse = win32gui.GetWindowText(hwnd_windows_mouse)
        print(f"Windows name: {hwnd_windows_mouse} - Tittle: {titulo_ventana_mouse}")
        hwnd_windows_mouse.enable_focus_windows(hwnd_windows_mouse)
    else:
        print("No window containing the mouse position was found.")