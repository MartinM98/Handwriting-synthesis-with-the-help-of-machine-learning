from src.graphical_interface.common import ChangePanelEvent
from src.file_handler.file_handler import get_absolute_path
from src.graphical_interface.common import resource_path
import wx
import os


class RecognitionPanel(wx.Panel):
    def __init__(self, parent, editname, statusBar, main_color, second_color):
        self.is_tesseract_loaded = False
        # self.use_synthesis = True
        wx.Panel.__init__(self, parent)
        self.statusBar = statusBar
        self.SetBackgroundColour(main_color)

        # create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hSizer3 = wx.BoxSizer(wx.HORIZONTAL)
        hSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hSizer4 = wx.BoxSizer(wx.HORIZONTAL)

        # ------------------ hSizer1 ------------------ #
        self.upper_panel = wx.Panel(self, wx.ID_ANY)
        self.upper_panel.SetBackgroundColour(second_color)
        hSizer1.Add(self.upper_panel, 1, wx.EXPAND, 0)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)

        path = get_absolute_path(
            'buttons/read_button.png')
        print(path)
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_ANY)
        self.button_read = wx.BitmapButton(
            self.upper_panel, id=wx.ID_ANY, bitmap=pic, size=(pic.GetWidth() - 3, pic.GetHeight() - 3))
        self.Bind(wx.EVT_BUTTON, self.on_read_click, self.button_read)
        # self.button_read.SetBackgroundColour(wx.Colour(217, 131, 26))
        # self.button_read.SetToolTip("ToolTip")
        sizer_2.Add(self.button_read, 0, wx.TOP | wx.RIGHT | wx.ALL, border=5)

        sizer_2.AddStretchSpacer()

        path = get_absolute_path(
            'buttons/synthesis_button.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_ANY)
        self.change_panel = wx.BitmapButton(
            self.upper_panel, id=wx.ID_ANY, bitmap=pic, size=(pic.GetWidth() - 3, pic.GetHeight() - 3))
        self.Bind(wx.EVT_BUTTON, self.on_change_panel, self.change_panel)
        self.change_panel.SetBackgroundColour(wx.Colour(217, 131, 26))
        self.change_panel.SetToolTip("ToolTip")
        sizer_2.Add(self.change_panel, 0, wx.RIGHT | wx.ALL, border=5)

        self.upper_panel.SetSizer(sizer_2)
        # ------------------ hSizer1 ------------------ #

        # ------------------ hSizer2 ------------------ #
        hSizer2.AddStretchSpacer()

        self.editname = editname
        hSizer2.Add(self.editname, 3, wx.EXPAND, border=10)

        hSizer2.AddStretchSpacer()
        # ------------------ hSizer2 ------------------ #

        hSizer3.AddStretchSpacer()
        hSizer4.AddStretchSpacer()

        mainSizer.Add(hSizer1, 0, wx.EXPAND)
        mainSizer.Add(hSizer3, 1, wx.CENTER | wx.EXPAND)
        mainSizer.Add(hSizer2, 10, wx.CENTER | wx.EXPAND)
        mainSizer.Add(hSizer4, 1, wx.CENTER | wx.EXPAND)
        self.SetSizerAndFit(mainSizer)

    def on_change_panel(self, event):
        evt = ChangePanelEvent()
        wx.PostEvent(self.Parent, evt)
        event.Skip()

    def on_read_click(self, event):
        """
        Reads text from picrute and writes it to the textbox
        """
        if self.is_tesseract_loaded is False:
            self.export_tesseract()
            self.is_tesseract_loaded = True
        with wx.FileDialog(self, 'Choose an image', wildcard='PNG files (*.png)|*.png') as fd:
            if fd.ShowModal() == wx.ID_OK:
                filename = fd.GetPath()
                textfile = filename[:-4] + '.txt'
                tesseract_command = 'tesseract ' + filename + \
                    ' ' + filename[:-4] + ' -l engnew quiet'
                os.system(tesseract_command)
                if os.path.isfile(textfile):
                    f = open(textfile, 'r')
                    self.editname.Value = f.read()[:-1]
                    f.close()
                    os.remove(textfile)

    def export_tesseract(self):
        path_to_model = get_absolute_path('./data/recognition_model/')
        os.environ["TESSDATA_PREFIX"] = path_to_model


class Frame(wx.Frame):
    """
    This is MyFrame.  It just shows a few controls on a wxPanel,
    and has a simple menu.
    """

    def __init__(self, parent, title, position, size):
        wx.Frame.__init__(self, parent, -1, title,
                          pos=position, size=size)

        self.editname = wx.TextCtrl(
            self, value="Testing", style=wx.TE_MULTILINE)
        self.editname.SetMinSize(
            (300, 300))
        self.editname.SetSize(
            (900, 600))

        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetStatusText("Synthesis Mode")

        main_color = wx.Colour(242, 223, 206)
        second_color = wx.Colour(64, 1, 1)

        self.recognition_panel = RecognitionPanel(
            self, self.editname, self.statusBar, main_color, second_color)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.recognition_panel, 1, wx.EXPAND)
        self.sizer.SetMinSize(1400, 700)
        self.SetSizerAndFit(self.sizer)

        menuBar = wx.MenuBar()
        menu = wx.Menu()
        menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Exit this simple sample")

        # bind the menu event to an event handler
        self.Bind(wx.EVT_MENU, self.Menu_Close, id=wx.ID_EXIT)
        self.Bind(wx.EVT_CLOSE, self.onClose)

        menuBar.Append(menu, "&Options")
        self.SetMenuBar(menuBar)

    def Menu_Close(self, event):
        self.Close()

    def onClose(self, event):
        event.Skip()
        # dlg = wx.MessageDialog(
        #     None, "Do you want to exit?", 'See you later?', wx.YES_NO | wx.ICON_QUESTION)
        # result = dlg.ShowModal()

        # if result == wx.ID_YES:
        #     event.Skip()

    def on_switch_panels(self, event):
        if self.synthesis_panel.IsShown():
            self.synthesis_panel.Hide()
            self.recognition_panel.Show()
            self.statusBar.SetStatusText("Recognition Mode")
        else:
            self.synthesis_panel.Show()
            self.recognition_panel.Hide()
            self.statusBar.SetStatusText("Synthesis Mode")
        self.Layout()


class Application(wx.App):
    def OnInit(self):
        frame = Frame(None, "Bachelor Project", (150, 150), (1280, 720))
        frame.Show()
        return True


if __name__ == '__main__':
    app = Application(redirect=False)  # TODO change to True at the end
    app.MainLoop()
