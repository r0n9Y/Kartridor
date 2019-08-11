#import pywintypes
import ctypes
import win32gui
import win32ui
import win32con
import win32api
from win32com.client import Dispatch
import wmi
import win32process
from constants import Winfo
from constants import PrintWinfo
from PIL import Image

APP_O = "o" # all shape info, top left x, top left y, right bottom x, right bottom y, window width and height
APP_RECT = "rectangle"
APP_HWND = "hwnd"
APP_TITLE = "title"
APP_PATH = "path"
APP_VSBL = "visible"
APP_NAME = "name"
# https://bytes.com/topic/python/answers/576924-win32ui-vs-wxpy-screen-capture-multi-monitor
str_sumulator_title_key = "阴阳师"
#str_sumulator_title_key = "Calculator"

mumu_window = {}
def enumerateWindows(hwnd, windowInfo):
    is_visible  = win32gui.IsWindowVisible(hwnd) == 1
    str_root_title = win32gui.GetWindowText(hwnd) # the root proc title
    if len(str_root_title) <= 0:
        return
    rectangle = win32gui.GetWindowRect(hwnd)
    #print(">>>> ",str_root_title)
    if len(str_root_title) > 4 and str_sumulator_title_key in str_root_title:
        print("Found the YYS")
        mumu_window[APP_HWND] = hwnd
        mumu_window[APP_TITLE] = str_root_title
        mumu_window[APP_RECT] = rectangle # Trying to deprecated
        mumu_window[APP_VSBL] = is_visible
        mumu_window[APP_NAME] = getAppName(hwnd)
        mumu_window[APP_PATH] = getAppPath(hwnd)
        #x0 = mumu_window[APP_RECT][0]
        #y0 = mumu_window[APP_RECT][1]
        #x1 = mumu_window[APP_RECT][2]
        #y1 = mumu_window[APP_RECT][3]
        #width = x1 - x0
        #height = y1 - y0
        #print(">>>>", width, height)
        #mumu_window[APP_O] = [x0, y0, x1, y1, width, height]
        SetWindowInfo()
        print("HWND: ", hwnd)
        print(str_root_title)
        print("App name: ", mumu_window[APP_NAME])
        print("App path: ", mumu_window[APP_PATH])
        print("App rect: ", mumu_window[APP_RECT])

        if mumu_window[APP_PATH]:
            print("Setting focus to " + str(mumu_window["path"]) + " : " + str(win32gui.SetForegroundWindow(hwnd)))
        print("-------------------------------------------")
        return True

def getAppPath(hwnd):
    """Get applicatin path given hwnd."""
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        for p in wmi.WMI().query('SELECT ExecutablePath FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
            ret_path = p.ExecutablePath
            break
    except:
        return None
    else:
        return ret_path


def getAppName(hwnd):
    """Get applicatin filename given hwnd."""
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        for p in wmi.WMI().query('SELECT Name FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
            ret_name = p.Name
            break
    except:
        return None
    else:
        return ret_name

def SetWindowInfo():
    Winfo.x0 = mumu_window[APP_RECT][0]
    Winfo.y0 = mumu_window[APP_RECT][1]
    Winfo.x1 = mumu_window[APP_RECT][2]
    Winfo.y1 = mumu_window[APP_RECT][3]
    Winfo.w = Winfo.x1 - Winfo.x0
    Winfo.h = Winfo.y1 - Winfo.y0
    mumu_window[APP_O] = [Winfo.x0, Winfo.y0, Winfo.x1, Winfo.y1, Winfo.w, Winfo.h]
    PrintWinfo()

# [TODO] currently it does not handle window move, using hwnd to get window frame position will be ideal
def GetFrame():
    wDC = win32gui.GetWindowDC(mumu_window[APP_HWND])
    dcObj =win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap  = win32ui.CreateBitmap()
 
    SetWindowInfo()
    dataBitMap.CreateCompatibleBitmap(dcObj, Winfo.w, Winfo.h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(Winfo.w, Winfo.h) , dcObj, (0,0), win32con.SRCCOPY)
    bmpInfo = dataBitMap.GetInfo()
    dataBitMap.SaveBitmapFile(cDC, "test.bmp")
    print(bmpInfo)
    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(mumu_window[APP_HWND], wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

def initalizeCollector():
    info = []
    win32gui.EnumWindows(enumerateWindows, info)
    return bool(mumu_window), mumu_window