from src.graphical_interface.create_text_different_widths_big_dataset import TextImageRenderAllDifferentWidths
from src.graphical_interface.common import ChangePanelEvent, PIL2wx
from src.image_processing.letters import extract, correct
from src.image_processing.resize import resize_directory, combine_directory, resize_skeletons_directory
from src.synthesis.process import process_directory
from src.file_handler.file_handler import get_absolute_path
from tkinter import filedialog
import tkinter as tk
import wx
import os
import enum


class ImageSize(enum.Enum):
    Small = (150, 100)
    Medium = (450, 300)
    Large = (900, 600)


class SynthesisPanel(wx.Panel):
    def __init__(self, parent, editname, statusBar):
        self.use_synthesis = True
        wx.Panel.__init__(self, parent)
        # self.Bind(wx.EVT_SIZE, self.on_resize)
        self.statusBar = statusBar

        # create some sizers
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.hSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.button_load = wx.Button(
            self, label="Load")
        self.Bind(wx.EVT_BUTTON, self.on_load_click, self.button_load)
        self.hSizer1.Add(self.button_load, 0,
                         wx.TOP | wx.LEFT | wx.ALL, border=5)

        self.button_save = wx.Button(
            self, label="Save")
        self.Bind(wx.EVT_BUTTON, self.on_save_click, self.button_save)
        self.hSizer1.Add(self.button_save, 0,
                         wx.TOP | wx.LEFT | wx.ALL, border=5)

        self.styles = ['Style 1', 'Style 2', 'Style 3']
        self.combobox = wx.ComboBox(
            self, choices=self.styles, value='Style 1', size=(80, -1))
        self.combobox.Bind(wx.EVT_COMBOBOX, self.on_combo)
        self.hSizer1.Add(self.combobox, 0,
                         wx.CENTER | wx.LEFT | wx.ALL, border=5)

        self.font_sizes = [str(x) for x in range(8, 24)]
        self.font_size_combobox = wx.ComboBox(
            self, choices=self.font_sizes, value='10', size=(80, -1))
        self.font_size_combobox.Bind(wx.EVT_COMBOBOX, self.on_combo)
        self.hSizer1.Add(self.font_size_combobox, 0,
                         wx.CENTER | wx.LEFT | wx.ALL, border=5)

        self.image_sizes = ['Small', 'Medium', 'Large']
        self.image_size_combobox = wx.ComboBox(
            self, choices=self.image_sizes, value='Medium', size=(80, -1))
        self.image_size_combobox.Bind(
            wx.EVT_COMBOBOX, self.on_image_size_combo)
        self.hSizer1.Add(self.image_size_combobox, 0,
                         wx.CENTER | wx.LEFT | wx.ALL, border=5)

        self.checkbox = wx.CheckBox(self, label='use GPU')
        self.hSizer1.Add(self.checkbox, 0, wx.CENTER | wx.ALL, border=5)

        self.button_render = wx.Button(
            self, label="Render")
        self.Bind(wx.EVT_BUTTON, self.on_render_click, self.button_render)
        self.hSizer1.Add(self.button_render, 0, wx.RIGHT | wx.ALL, border=5)

        self.hSizer1.AddStretchSpacer()

        self.change_panel = wx.Button(
            self, label="Recognition Mode")
        self.Bind(wx.EVT_BUTTON, self.on_change_panel, self.change_panel)
        self.hSizer1.Add(self.change_panel, 0, wx.RIGHT | wx.ALL, border=5)
        # ------------------ hSizer1 ------------------ #

        # ------------------ hSizer2 ------------------ #
        # hSizer2.AddStretchSpacer()

        self.editname = editname
        self.hSizer2.Add(self.editname, 2, wx.EXPAND, border=10)

        # hSizer2.AddStretchSpacer()
        self.image_size = ImageSize.Medium
        img = wx.Image(self.image_size.value[0], self.image_size.value[1])
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY,
                                         wx.Bitmap(img))
        self.hSizer2.Add(self.imageCtrl, 3, wx.CENTER, border=10)

        # hSizer2.AddStretchSpacer()
        # ------------------ hSizer2 ------------------ #

        self.mainSizer.Add(self.hSizer1, 0, wx.EXPAND)
        self.mainSizer.Add(self.hSizer2, 1, wx.EXPAND)
        self.SetSizerAndFit(self.mainSizer)

    def on_combo(self, event):
        print("selected " + self.combobox.GetValue() + " from Combobox")

    def on_image_size_combo(self, event):
        size = self.image_size_combobox.GetValue()
        if size == self.image_sizes[0]:
            self.resize_image(ImageSize.Small)
        elif size == self.image_sizes[1]:
            self.resize_image(ImageSize.Medium)
        elif size == self.image_sizes[2]:
            self.resize_image(ImageSize.Large)

    def on_change_panel(self, event):
        evt = ChangePanelEvent()
        wx.PostEvent(self.Parent, evt)
        event.Skip()

    def resize_image(self, size):
        self.image_size = size
        img = self.imageCtrl.GetBitmap().ConvertToImage()
        img = img.Scale(size.value[0], size.value[1])
        self.imageCtrl.SetBitmap(wx.Bitmap(img))
        # self.Update()
        # self.Refresh()
        self.Layout()

    def on_render_click(self, event):
        """
        Creates a handwriting imitation image
        """
        use_gpu = self.checkbox.GetValue()
        if (self.use_synthesis):
            process_directory(get_absolute_path(
                './src/graphical_interface/export'), get_absolute_path('./src/graphical_interface/synthesis/skeletons/'), use_gpu)
            text_renderer = TextImageRenderAllDifferentWidths(
                get_absolute_path('./src/graphical_interface/synthesis/synthesized/'), self.image_size.value[0], self.image_size.value[1], 50, self.editname.GetValue())
        else:
            text_renderer = TextImageRenderAllDifferentWidths(
                get_absolute_path('./src/graphical_interface/letters_dataset/'), self.image_size.value[0], self.image_size.value[1], 50, self.editname.GetValue())

        img = text_renderer.create_image()

        self.imageCtrl.SetBitmap(PIL2wx(img))
        self.Layout()

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


class Frame(wx.Frame):
    """
    This is MyFrame.  It just shows a few controls on a wxPanel,
    and has a simple menu.
    """

    def __init__(self, parent, title, position, size):
        wx.Frame.__init__(self, parent, -1, title,
                          pos=position, size=size)

        self.editname = wx.TextCtrl(
            self, value="Testing the function.", style=wx.TE_MULTILINE)
        window_size = self.GetSize()
        self.editname.SetMinSize((300, 400))
        self.editname.SetMaxSize((int(window_size[0] / 2), -1))
        # editname.SetMaxSize((200, 200))

        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetStatusText("Synthesis Mode")

        self.synthesis_panel = SynthesisPanel(
            self, self.editname, self.statusBar)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.synthesis_panel, 1, wx.EXPAND)
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
