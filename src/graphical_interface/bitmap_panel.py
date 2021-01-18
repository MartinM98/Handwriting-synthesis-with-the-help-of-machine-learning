import wx
import wx.lib.scrolledpanel as scrl


class BitmapPanel(scrl.ScrolledPanel):
    def __init__(self, parent, bitmap):
        scrl.ScrolledPanel.__init__(self, parent)

        self.mainSizer_v = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer_h = wx.BoxSizer(wx.HORIZONTAL)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, bitmap=bitmap)
        self.mainSizer_v.Add(self.imageCtrl, 1, wx.CENTER)
        self.mainSizer_h.Add(self.mainSizer_v, 1, wx.CENTER)
        self.SetSizerAndFit(self.mainSizer_h)
        self.SetupScrolling()
