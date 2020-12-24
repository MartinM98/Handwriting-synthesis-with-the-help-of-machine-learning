import wx.lib.newevent

ChangePanelEvent, EVT_CHANGE_PANEL_EVENT = wx.lib.newevent.NewEvent()


def PIL2wx(image):  # This function converts PIL image to wx image
    width, height = image.size
    return wx.Bitmap.FromBuffer(width, height, image.tobytes())
