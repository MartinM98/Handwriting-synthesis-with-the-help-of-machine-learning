from create_text_different_widths_big_dataset import TextImageRenderAllDifferentWidths
from src.image_processing.letters import Extract
import wx
import os
# from create_text_with_font_static import TextImageRenderAllConstantWidths


class Frame(wx.Frame):
    """
    This is MyFrame.  It just shows a few controls on a wxPanel,
    and has a simple menu.
    """

    def __init__(self, parent, title, position, size):
        wx.Frame.__init__(self, parent, -1, title,
                          pos=position, size=size)

        menuBar = wx.MenuBar()
        menu = wx.Menu()
        menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Exit this simple sample")

        # bind the menu event to an event handler
        self.Bind(wx.EVT_MENU, self.Menu_Close, id=wx.ID_EXIT)
        self.Bind(wx.EVT_CLOSE, self.onClose)

        menuBar.Append(menu, "&Options")
        self.SetMenuBar(menuBar)

        self.CreateStatusBar()

    def Menu_Close(self, event):
        self.Close()

    def onClose(self, event):
        event.Skip()
        # dlg = wx.MessageDialog(
        #     None, "Do you want to exit?", 'See you later?', wx.YES_NO | wx.ICON_QUESTION)
        # result = dlg.ShowModal()

        # if result == wx.ID_YES:
        #     event.Skip()


class Panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(hgap=2, vgap=2)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.button_render = wx.Button(
            self, label="Render", pos=(200, 325), style=wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.OnRenderClick, self.button_render)
        grid.Add(self.button_render, pos=(0, 0), span=(0, 1))

        self.button_load = wx.Button(
            self, label="Load", pos=(400, 325), style=wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.OnLoadClick, self.button_load)
        grid.Add(self.button_load, pos=(0, 1), span=(0, 1))

        self.editname = wx.TextCtrl(
            self, value="Example text.", size=(290, 250), style=wx.TE_MULTILINE)
        grid.Add(self.editname, pos=(1, 0))

        img = wx.Image(290, 250)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY,
                                         wx.Bitmap(img))
        grid.Add(self.imageCtrl, pos=(1, 1))

        hSizer.Add(grid, 0, wx.ALL, 5)
        mainSizer.Add(hSizer, 0, wx.ALL, 5)
        self.SetSizerAndFit(mainSizer)

    def OnRenderClick(self, event):
        # print("Render")
        text_renderer = TextImageRenderAllDifferentWidths('./letters_dataset/', 290, 250, 30, self.editname.GetValue())
        img = text_renderer.create_image()

        self.imageCtrl.SetBitmap(PIL2wx(img))

    def OnLoadClick(self, event):
        Extract(cwd=os.getcwd())


# This function converts PIL image to wx image
def PIL2wx(image):
    width, height = image.size
    return wx.Bitmap.FromBuffer(width, height, image.tobytes())


class Application(wx.App):
    def OnInit(self):
        frame = Frame(None, "Bachelor Project", (150, 150), (600, 400))
        Panel(frame)
        self.SetTopWindow(frame)
        frame.Show()
        return True


if __name__ == '__main__':
    app = Application(redirect=True)
    app.MainLoop()
