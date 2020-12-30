import wx.lib.newevent
import enum

ChangePanelEvent, EVT_CHANGE_PANEL_EVENT = wx.lib.newevent.NewEvent()


def PIL2wx(image):  # This function converts PIL image to wx image
    width, height = image.size
    return wx.Bitmap.FromBuffer(width, height, image.tobytes())


class ImageSize(enum.Enum):
    Small = (450, 300)
    Medium = (675, 450)
    Large = (900, 600)
