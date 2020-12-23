from src.graphical_interface.create_text import TextImageRenderAllDifferentWidths
from src.graphical_interface.common import SomeNewEvent, PIL2wx
from src.image_processing.letters import extract, correct
from src.image_processing.resize import resize_directory, combine_directory, resize_skeletons_directory
from src.synthesis.process import process_directory
from tkinter import filedialog
import tkinter as tk
import wx
import os


class SynthesisPanel(wx.Panel):
    def __init__(self, parent, editname, statusBar):
        self.use_synthesis = True
        wx.Panel.__init__(self, parent)
        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.statusBar = statusBar

        # create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.button_load = wx.Button(
            self, label="Load")
        self.Bind(wx.EVT_BUTTON, self.on_load_click, self.button_load)
        hSizer1.Add(self.button_load, 0, wx.TOP | wx.LEFT | wx.ALL, border=5)

        self.button_save = wx.Button(
            self, label="Save")
        self.Bind(wx.EVT_BUTTON, self.on_save_click, self.button_save)
        hSizer1.Add(self.button_save, 0, wx.TOP | wx.LEFT | wx.ALL, border=5)

        self.styles = ['Style 1', 'Style 2', 'Style 3']
        self.combobox = wx.ComboBox(
            self, choices=self.styles, value='Style 1', size=(80, -1))
        self.combobox.Bind(wx.EVT_COMBOBOX, self.on_combo)
        hSizer1.Add(self.combobox, 0, wx.CENTER | wx.LEFT | wx.ALL, border=5)

        self.button_render = wx.Button(
            self, label="Render")
        self.Bind(wx.EVT_BUTTON, self.on_render_click, self.button_render)
        hSizer1.Add(self.button_render, 0, wx.RIGHT | wx.ALL, border=5)

        hSizer1.AddStretchSpacer()

        self.change_panel = wx.Button(
            self, label="Recognition Mode")
        self.Bind(wx.EVT_BUTTON, self.on_change_panel, self.change_panel)
        hSizer1.Add(self.change_panel, 0, wx.RIGHT | wx.ALL, border=5)
        # ------------------ hSizer1 ------------------ #

        # ------------------ hSizer2 ------------------ #
        # hSizer2.AddStretchSpacer()

        self.editname = editname
        hSizer2.Add(self.editname, 1, wx.EXPAND, border=10)

        # hSizer2.AddStretchSpacer()

        img = wx.Image(240, 240)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY,
                                         wx.Bitmap(img))
        hSizer2.Add(self.imageCtrl, 1, wx.EXPAND, border=10)

        # hSizer2.AddStretchSpacer()
        # ------------------ hSizer2 ------------------ #

        mainSizer.Add(hSizer1, 0, wx.EXPAND)
        mainSizer.Add(hSizer2, 1, wx.EXPAND)
        self.SetSizerAndFit(mainSizer)

    def on_combo(self, event):
        print("selected " + self.combobox.GetValue() + " from Combobox")

    def on_change_panel(self, event):
        evt = SomeNewEvent()
        wx.PostEvent(self.Parent, evt)
        event.Skip()

    def on_resize(self, event):
        self.resize_image()
        event.Skip()

    def resize_image(self):
        window_size = self.GetSize()
        editname_size = ((window_size[0] - 10) / 2, window_size[1] - 30)
        self.editname.SetSize(editname_size)

        img = self.imageCtrl.GetBitmap().ConvertToImage()
        img = img.Scale((window_size[0] - 10) / 2, window_size[1] - 30)
        self.imageCtrl.SetBitmap(wx.Bitmap(img))
        self.Refresh()

    def on_render_click(self, event):
        """
        Creates a handwriting imitation image
        """
        if (self.use_synthesis):
            process_directory('./export', './synthesis/skeletons/')
            text_renderer = TextImageRenderAllDifferentWidths(
                './synthesis/synthesized/', 290, 250, 50, self.editname.GetValue())
        else:
            text_renderer = TextImageRenderAllDifferentWidths(
                './letters_dataset/', 290, 250, 50, self.editname.GetValue())
        img = text_renderer.create_image()

        self.imageCtrl.SetBitmap(PIL2wx(img))

    def on_load_click(self, event):
        """
        Creates new dataset from pictures from selected directory
        """
        path = os.getcwd()
        dir = extract(path)
        correct(dir)
        resize_directory(path + '/letters_dataset',
                         path + '/training_dataset/letters')
        resize_skeletons_directory(
            path + '/letters_dataset', path + '/training_dataset/skeletons')
        combine_directory(path + '/training_dataset/letters',
                          path + '/training_dataset/skeletons', path + '/training_dataset/combined')
        train_command = 'python ../synthesis/pix2pix.py --mode train --output_dir ./model/ --max_epochs 100 --input_dir ./training_dataset/combined --which_direction BtoA --ngf 32 --ndf 32'
        os.system(train_command)
        export_command = 'python ../synthesis/pix2pix.py --mode export --output_dir ./export/ --checkpoint ./model/ --which_direction BtoA'
        os.system(export_command)

    def on_save_click(self, event):
        """
        Saves created image
        """
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.asksaveasfilename(
            filetypes=[("PNG file", "*.png")], defaultextension=[("PNG file", "*.png")])
        img = self.imageCtrl.GetBitmap()
        if len(filename) > 0:
            self.statusBar.SetStatusText("Saving...")
            img.SaveFile(filename, wx.BITMAP_TYPE_PNG)
            self.statusBar.SetStatusText("File saved.")
