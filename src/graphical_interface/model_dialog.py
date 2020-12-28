import wx
from wx.lib import sized_controls


class ModelDialog(sized_controls.SizedDialog):
    def __init__(self, *args, **kwargs):
        super(ModelDialog, self).__init__(*args, **kwargs)
        pane = self.GetContentsPane()
        pane.SetSizerType("grid", {"cols": 2})

        wx.StaticText(pane, -1, "Number of epochs:").SetSizerProps()
        self.epochs = wx.TextCtrl(pane, validator=Validator(self))
        self.epochs.ChangeValue("200")
        self.epochs.SetSizerProps()

        wx.StaticText(pane, -1, "ngf:").SetSizerProps()
        self.ngf = wx.TextCtrl(pane, validator=Validator(self))
        self.ngf.ChangeValue("16")
        self.ngf.SetSizerProps()

        wx.StaticText(pane, -1, "ndf:").SetSizerProps()
        self.ndf = wx.TextCtrl(pane, validator=Validator(self))
        self.ndf.ChangeValue("16")
        self.ndf.SetSizerProps()

        self.ok_button = wx.Button(pane, id=wx.ID_OK, label='OK')
        self.ok_button.SetSizerProps()
        self.cancel_button = wx.Button(pane, id=wx.ID_CANCEL, label='Cancel')
        self.cancel_button.SetSizerProps()

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
        inputs.append(self.win.epochs.GetValue())
        inputs.append(self.win.ndf.GetValue())
        inputs.append(self.win.ngf.GetValue())
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
    dlg = ModelDialog(None)
    result = dlg.ShowModal()
