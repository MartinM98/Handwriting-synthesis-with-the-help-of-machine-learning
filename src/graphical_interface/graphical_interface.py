from src.graphical_interface.common import EVT_CHANGE_PANEL_EVENT
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

        main_color = wx.Colour(242, 223, 206)
        second_color = wx.Colour(64, 1, 1)

        self.synthesis_panel = SynthesisPanel(
            self, self.statusBar, main_color, second_color)
        self.recognition_panel = RecognitionPanel(
            self, self.statusBar, main_color, second_color)

        self.synthesis_panel.Hide()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.synthesis_panel, 1, wx.EXPAND)
        self.sizer.Add(self.recognition_panel, 1, wx.EXPAND)
        self.sizer.SetMinSize(1400, 700)
        self.SetSizerAndFit(self.sizer)

        menuBar = wx.MenuBar()
        menu = wx.Menu()
        menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Exit this simple sample")

        # bind the menu event to an event handler
        self.Bind(wx.EVT_MENU, self.Menu_Close, id=wx.ID_EXIT)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(EVT_CHANGE_PANEL_EVENT, self.on_switch_panels)

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
            self.recognition_panel.editname.SetValue(
                self.synthesis_panel.editname.GetValue())
            self.synthesis_panel.Hide()
            self.recognition_panel.Show()
            self.statusBar.SetStatusText("Recognition Mode")
        else:
            self.synthesis_panel.editname.SetValue(
                self.recognition_panel.editname.GetValue())
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
