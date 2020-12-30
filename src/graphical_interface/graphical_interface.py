import os
from src.file_handler.file_handler import ensure_create_and_append_file, get_absolute_path, read_from_file
from src.graphical_interface.common import EVT_CHANGE_PANEL_EVENT, ImageSize
import wx
from src.graphical_interface.recognition_panel import RecognitionPanel
from src.graphical_interface.synthesis_panel import SynthesisPanel


class Frame(wx.Frame):
    """
    This is MyFrame.  It just shows a few controls on a wxPanel,
    and has a simple menu.
    """

    def __init__(self, parent, title, position, size):
        wx.Frame.__init__(self, parent, -1, title,
                          pos=position, size=size)

        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetStatusText("Synthesis Mode")

        main_color = wx.Colour(228, 228, 228)
        second_color = wx.Colour(161, 183, 168)

        self.synthesis_panel = SynthesisPanel(
            self, self.statusBar, main_color, second_color, self.find_models())
        self.recognition_panel = RecognitionPanel(
            self, self.statusBar, main_color, second_color)
        self.panel = "recognition"
        self.synthesis_panel.Hide()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.synthesis_panel, 1, wx.EXPAND)
        self.sizer.Add(self.recognition_panel, 1, wx.EXPAND)
        self.sizer.SetMinSize(1400, 700)
        self.SetSizerAndFit(self.sizer)

        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(EVT_CHANGE_PANEL_EVENT, self.on_switch_panels)

        menuBar = wx.MenuBar()
        # ------------------ menu - File ------------------ #
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_SAVE, "S&ave\tAlt-S", helpString="Save result")

        file_menu.Append(wx.ID_OPEN, "L&oad\tAlt-L", helpString="Load text")

        menuBar.Append(file_menu, "&File")
        # ------------------ menu - File ------------------ #

        # ------------------ menu - Options ------------------ #
        self.option_menu = wx.Menu()

        size_menu = wx.Menu()
        size_menu.Append(108, "Large",
                         "Large size of image", wx.ITEM_RADIO)
        size_menu.Append(107, "Medium",
                         "Medium size of image", wx.ITEM_RADIO)
        size_menu.Append(106, "Small",
                         "Small size of image", wx.ITEM_RADIO)

        self.option_menu.Append(105, 'Image size', size_menu)
        self.option_menu.Enable(105, False)

        self.option_menu.Append(
            104, 'Use GPU', 'Use GPU in synthesize', wx.ITEM_CHECK)
        self.option_menu.Enable(104, False)

        self.option_menu.AppendSeparator()

        advanced_option_menu = wx.Menu()

        filters_menu = wx.Menu()
        filters_menu.Append(113, "Original",
                            "Large size of image", wx.ITEM_RADIO)
        filters_menu.Append(114, "Cons",
                            "Medium size of image", wx.ITEM_RADIO)

        advanced_option_menu.Append(112, 'Filters', filters_menu)

        advanced_option_menu.Append(111, "Test", helpString="Test")

        self.option_menu.Append(110, 'Advanced', advanced_option_menu)
        self.option_menu.Enable(110, False)
        self.option_menu.AppendSeparator()

        self.option_menu.Append(wx.ID_EXIT, "E&xit\tAlt-X",
                                "Exit this simple sample")

        menuBar.Append(self.option_menu, "&Options")
        # ------------------ menu - Options ------------------ #

        # ------------------ menu - About ------------------ #
        about_menu = wx.Menu()
        about_menu.Append(wx.ID_ABOUT, "A&bout the project\tAlt-A",
                          "Show informations about the application")

        about_menu.Append(100, "Au&thors\tAlt-U",
                          "Show informations about the application authors")

        menuBar.Append(about_menu, "&About")
        # ------------------ menu - About ------------------ #
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.menuhandler)
        path = get_absolute_path("img/Bachelor_Thesis.ico")
        icon = wx.Icon(path, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

    def find_models(self):
        entries = [name for name in os.listdir(
            './data/synthesis_models') if not name.startswith('.')]
        return sorted(entries, key=lambda x: int(os.path.splitext(x)[0]))

    def menuhandler(self, event):  # noqa: C901
        id = event.GetId()
        if id == wx.ID_ABOUT:
            self.show_informations(event)
        elif id == wx.ID_EXIT:
            self.menu_close(event)
        elif id == wx.ID_EXIT:
            self.menu_close(event)
        elif id == wx.ID_SAVE:
            self.save(event)
        elif id == 100:
            self.show_authors(event)
        elif id == wx.ID_OPEN:
            self.load_text(event)
        elif id == 106:
            self.synthesis_panel.chane_image_size(ImageSize.Small)
        elif id == 107:
            self.synthesis_panel.chane_image_size(ImageSize.Medium)
        elif id == 108:
            self.synthesis_panel.chane_image_size(ImageSize.Large)
        elif id == 104:
            if self.synthesis_panel.use_gpu:
                self.synthesis_panel.use_gpu = False
            else:
                self.synthesis_panel.use_gpu = True
        elif id == 111:
            print('test')
        elif id == 113:
            print('opcja1')
        elif id == 114:
            print('opcja2')

    def load_text(self, event):
        with wx.FileDialog(self, 'Load file', wildcard='Text files (*.txt)|*.txt', style=wx.FD_OPEN) as fd:
            if fd.ShowModal() == wx.ID_OK:
                filename = fd.GetPath()
                txt = read_from_file(filename)
                if self.panel == "synthesis":
                    self.synthesis_panel.editname.SetValue(txt)
                else:
                    self.recognition_panel.editname.SetValue(txt)

    def show_informations(self, event):
        wx.MessageBox('This is the application created for Bachelor Thesis at Warsow University of Technology Faculty of Mathematics and Information Science.', 'Informations', wx.OK)

    def show_authors(self, event):
        wx.MessageBox(
            'The authors of the application are: \n - Martin Mrugała \n - Patryk Walczak \n - Bartłomiej Żyła', 'Authors', wx.OK)

    def menu_close(self, event):
        self.Close()

    def on_close(self, event):
        event.Skip()
        # dlg = wx.MessageDialog(
        #     None, "Do you want to exit?", 'See you later?', wx.YES_NO | wx.ICON_QUESTION)
        # result = dlg.ShowModal()

        # if result == wx.ID_YES:
        #     event.Skip()

    def on_switch_panels(self, event):
        if self.synthesis_panel.IsShown():
            self.recognition_panel.editname.SetValue(
                self.synthesis_panel.editname.GetValue())
            self.synthesis_panel.Hide()
            self.recognition_panel.Show()
            self.statusBar.SetStatusText("Recognition Mode")
            self.panel = "recognition"
            self.option_menu.Enable(105, False)
            self.option_menu.Enable(104, False)
            self.option_menu.Enable(110, False)
        else:
            self.synthesis_panel.editname.SetValue(
                self.recognition_panel.editname.GetValue())
            self.synthesis_panel.Show()
            self.recognition_panel.Hide()
            self.statusBar.SetStatusText("Synthesis Mode")
            self.panel = "synthesis"
            self.option_menu.Enable(105, True)
            self.option_menu.Enable(104, True)
            self.option_menu.Enable(110, True)
        self.Layout()

    def save(self, event):
        """
        Saves created image
        """
        if self.panel == "synthesis":
            with wx.FileDialog(self, 'Save image', wildcard='PNG files (*.png)|*.png', style=wx.FD_SAVE) as fd:
                if fd.ShowModal() == wx.ID_OK:
                    filename = fd.GetPath()
                    img = self.synthesis_panel.imageCtrl.GetBitmap()
                    if len(filename) > 0:
                        self.statusBar.SetStatusText('Saving...')
                        img.SaveFile(filename, wx.BITMAP_TYPE_PNG)
                        self.statusBar.SetStatusText('File saved.')
                    txt = self.synthesis_panel.editname.GetValue()
                    if len(txt) > 0:
                        self.statusBar.SetStatusText('Saving...')
                        filename = str.replace(filename, '.png', '.txt')
                        ensure_create_and_append_file(filename, txt)
                        self.statusBar.SetStatusText('File saved.')
        elif self.panel == "recognition":
            with wx.FileDialog(self, 'Save text', wildcard='text files (*.txt)|*.txt', style=wx.FD_SAVE) as fd:
                if fd.ShowModal() == wx.ID_OK:
                    filename = fd.GetPath()
                    txt = self.synthesis_panel.editname.GetValue()
                    if len(txt) > 0:
                        self.statusBar.SetStatusText('Saving...')
                        ensure_create_and_append_file(filename, txt)
                        self.statusBar.SetStatusText('File saved.')


class Application(wx.App):
    def OnInit(self):
        frame = Frame(None, "Scripturam", (150, 150), (1280, 720))
        frame.Show()
        return True


if __name__ == '__main__':
    app = Application(redirect=False)  # TODO change to True at the end
    app.MainLoop()
