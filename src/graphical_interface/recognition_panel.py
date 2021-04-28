from src.graphical_interface.common import ChangePanelEvent
from src.file_handler.file_handler import get_absolute_path
import wx
import os


class RecognitionPanel(wx.Panel):
    def __init__(self, parent, statusBar, main_color, second_color, font):
        self.is_tesseract_loaded = False
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
            'resources/read_button.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        self.button_read = wx.BitmapButton(
            self.upper_panel, id=wx.ID_ANY, bitmap=pic, size=(pic.GetWidth() - 3, pic.GetHeight() - 3))
        self.Bind(wx.EVT_BUTTON, self.on_read_click, self.button_read)
        sizer_2.Add(self.button_read, 0, wx.TOP | wx.RIGHT | wx.ALL, border=5)

        sizer_2.AddStretchSpacer()

        path = get_absolute_path(
            'resources/synthesis_button.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
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

        self.editname = wx.TextCtrl(
            self, value='Scripturam', style=wx.TE_MULTILINE)
        self.editname.SetFont(font)
        self.editname.SetMinSize(
            (300, 300))
        hSizer2.Add(self.editname, 3, wx.EXPAND, border=10)

        hSizer2.AddStretchSpacer()
        # ------------------ hSizer2 ------------------ #

        hSizer3.AddStretchSpacer()
        hSizer4.AddStretchSpacer()

        mainSizer.Add(hSizer1, 0, wx.EXPAND)
        mainSizer.Add(hSizer3, 1, wx.CENTER | wx.EXPAND)
        mainSizer.Add(hSizer2, 30, wx.CENTER | wx.EXPAND)
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
            self.statusBar.SetStatusText('Recognition model loaded')
        self.statusBar.SetStatusText('Choosing file...')
        with wx.FileDialog(self, 'Choose an image', wildcard='PNG files (*.png)|*.png') as fd:
            if fd.ShowModal() == wx.ID_OK:
                self.statusBar.SetStatusText('Reading file...')
                filename = fd.GetPath()
                textfile = filename[:-4] + '.txt'
                tesseract_command = 'tesseract "' + filename + \
                    '" "' + filename[:-4] + '" -l engnew quiet'
                os.system(tesseract_command)
                if os.path.isfile(textfile):
                    f = open(textfile, 'r')
                    self.editname.Value = f.read()[:-1]
                    f.close()
                    os.remove(textfile)
                    self.statusBar.SetStatusText('File read')
                else:
                    self.statusBar.SetStatusText('Error during read')

    def export_tesseract(self):
        path_to_model = './data/recognition_model/'
        os.environ["TESSDATA_PREFIX"] = path_to_model
