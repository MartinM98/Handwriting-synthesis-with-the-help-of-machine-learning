import wx
import wx.lib.scrolledpanel as scrl


class BitmapPanel(scrl.ScrolledPanel):
    def __init__(self, parent, bitmap):
        scrl.ScrolledPanel.__init__(self, parent)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY,
                                         bitmap=bitmap)
        self.mainSizer.Add(self.imageCtrl, 1, wx.EXPAND)
        self.SetSizerAndFit(self.mainSizer)
        self.SetupScrolling()
