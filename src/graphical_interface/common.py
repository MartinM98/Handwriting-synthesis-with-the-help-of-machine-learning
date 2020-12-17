import wx.lib.newevent

SomeNewEvent, EVT_SOME_NEW_EVENT = wx.lib.newevent.NewEvent()
SomeNewCommandEvent, EVT_SOME_NEW_COMMAND_EVENT = wx.lib.newevent.NewCommandEvent()


def PIL2wx(image):  # This function converts PIL image to wx image
    width, height = image.size
    return wx.Bitmap.FromBuffer(width, height, image.tobytes())
