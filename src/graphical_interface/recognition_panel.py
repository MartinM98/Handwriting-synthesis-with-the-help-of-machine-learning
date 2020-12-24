from src.graphical_interface.common import SomeNewEvent
import wx
import os


class RecognitionPanel(wx.Panel):
    def __init__(self, parent, editname, statusBar):
        # self.use_synthesis = True
        wx.Panel.__init__(self, parent)
        self.statusBar = statusBar

        # create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        # ------------------ hSizer1 ------------------ #
        self.button_read = wx.Button(
            self, label="Read")
        self.Bind(wx.EVT_BUTTON, self.on_read_click, self.button_read)
        hSizer1.Add(self.button_read, 0, wx.TOP | wx.RIGHT | wx.ALL, border=5)

        hSizer1.AddStretchSpacer()

        self.change_panel = wx.Button(
            self, label="Synthesis Mode")
        self.Bind(wx.EVT_BUTTON, self.on_change_panel, self.change_panel)
        hSizer1.Add(self.change_panel, 0, wx.RIGHT | wx.ALL, border=5)
        # ------------------ hSizer1 ------------------ #

        # ------------------ hSizer2 ------------------ #
        hSizer2.AddStretchSpacer()

        self.editname = editname
        hSizer2.Add(self.editname, 3, wx.EXPAND, border=10)

        hSizer2.AddStretchSpacer()

        # ------------------ hSizer2 ------------------ #

        mainSizer.Add(hSizer1, 0, wx.EXPAND)
        mainSizer.Add(hSizer2, 1, wx.CENTER | wx.EXPAND)
        self.SetSizerAndFit(mainSizer)

    def on_change_panel(self, event):
        evt = SomeNewEvent()
        wx.PostEvent(self.Parent, evt)
        event.Skip()

    def on_read_click(self, event):
        """
        Reads text from picrute and writes it to the textbox
        """
        with wx.FileDialog(self, 'Choose an image', wildcard='PNG files (*.png)|*.png') as fd:
            if fd.ShowModal() == wx.ID_OK:
                filename = fd.GetPath()
                textfile = filename[:-4] + '.txt'
                command = 'tesseract ' + filename + ' ' + filename[:-4] + ' -l engnew quiet'
                os.system(command)
                if os.path.isfile(textfile):
                    f = open(textfile, 'r')
                    self.editname.Value = f.read()[:-1]
                    f.close()
                    os.remove(textfile)
