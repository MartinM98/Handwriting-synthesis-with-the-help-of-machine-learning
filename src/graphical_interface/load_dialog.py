import wx
from wx.lib import sized_controls


class LoadDialog(sized_controls.SizedDialog):
    def __init__(self, *args, **kwargs):
        super(LoadDialog, self).__init__(*args, **kwargs)
        pane = self.GetContentsPane()
        pane.SetSizerType("grid", {"cols": 3})

        wx.StaticText(pane, -1, "Filter type").SetSizerProps()
        wx.StaticText(pane, -1, "Grid shape").SetSizerProps()
        wx.StaticText(pane, -1, "No of points").SetSizerProps()

        wx.StaticText(pane, -1, "Consecutive").SetSizerProps()
        self.consecutive_n = wx.TextCtrl(pane, validator=Validator(self))
        self.consecutive_n.SetSizerProps()
        self.consecutive_k = wx.TextCtrl(pane, validator=Validator(self))
        self.consecutive_k.SetSizerProps()

        wx.StaticText(pane, -1, "Random").SetSizerProps()
        self.random_n = wx.TextCtrl(pane, validator=Validator(self))
        self.random_n.SetSizerProps()
        self.random_k = wx.TextCtrl(pane, validator=Validator(self))
        self.random_k.SetSizerProps()

        wx.StaticText(pane, -1, "BS").SetSizerProps()
        self.bs_n = wx.TextCtrl(pane, validator=Validator(self))
        self.bs_n.SetSizerProps()
        self.bs_k = wx.TextCtrl(pane, validator=Validator(self))
        self.bs_k.SetSizerProps()

        wx.StaticText(pane, -1, "").SetSizerProps()
        self.cancel_button = wx.Button(pane, id=wx.ID_CANCEL, label='Cancel')
        self.cancel_button.SetSizerProps()
        self.ok_button = wx.Button(pane, id=wx.ID_OK, label='OK')
        self.ok_button.SetSizerProps()

        self.Bind(wx.EVT_BUTTON, self.confirm, id=wx.ID_OK)

    def confirm(self, event):
        self.EndModal(wx.ID_OK)


class Validator(wx.Validator):
    def __init__(self, win):
        wx.Validator.__init__(self)
        self.Bind(wx.EVT_TEXT, self.Validate)
        self.win = win

    def TransferToWindow(self):
        return True

    def TransfertFromWindow(self):
        return True

    def Clone(self):
        return Validator(self.win)

    def Validate(self, win):
        control = self.GetWindow()
        input = control.GetValue()
        if input.isdigit() or len(input) == 0:
            control.SetBackgroundColour('White')
        else:
            control.SetBackgroundColour('Red')
        inputs = []
        inputs.append(self.win.consecutive_n.GetValue())
        inputs.append(self.win.consecutive_k.GetValue())
        inputs.append(self.win.random_n.GetValue())
        inputs.append(self.win.random_k.GetValue())
        inputs.append(self.win.bs_n.GetValue())
        inputs.append(self.win.bs_k.GetValue())
        disable = False
        for elem in inputs:
            if not elem.isdigit() and elem != '':
                disable = True

        if disable:
            self.win.ok_button.Disable()
        else:
            self.win.ok_button.Enable()

        return True


if __name__ == "__main__":
    app = wx.App(False)
    dlg = LoadDialog(None)
    result = dlg.ShowModal()
