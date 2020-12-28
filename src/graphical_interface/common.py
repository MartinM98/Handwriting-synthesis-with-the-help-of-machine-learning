import wx.lib.newevent
# from src.file_handler.file_handler import get_absolute_path
import sys
import os

ChangePanelEvent, EVT_CHANGE_PANEL_EVENT = wx.lib.newevent.NewEvent()


def PIL2wx(image):  # This function converts PIL image to wx image
    width, height = image.size
    return wx.Bitmap.FromBuffer(width, height, image.tobytes())


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    # try:
    #     # PyInstaller creates a temp folder and stores path in _MEIPASS
    #     base_path = sys._MEIPASS
    # except Exception:
    #     base_path = get_absolute_path(".")

    # return os.path.join(base_path, relative_path)
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


if __name__ == "__main__":
    path = getattr(sys, '_MEIPASS', os.getcwd())
    print(resource_path('.'))
    print(path)
