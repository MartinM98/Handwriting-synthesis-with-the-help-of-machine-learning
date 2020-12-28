from src.graphical_interface.create_text import TextImageRenderAllDifferentWidths
from src.graphical_interface.common import ChangePanelEvent, PIL2wx
from src.image_processing.letters import extract, correct
from src.image_processing.resize import resize_directory, combine_directory, resize_skeletons_directory
from src.synthesis.process import process_directory
from src.image_processing.automated_functions import process_dataset
from src.file_handler.file_handler import combine_paths, ensure_create_and_append_file, get_absolute_path
import wx
import os
import enum
from src.graphical_interface.load_dialog import LoadDialog
from src.image_processing.automated_functions import process_options
from src.file_handler.file_handler import remove_dir_with_content
from src.file_handler.file_handler import ensure_create_dir


class ImageSize(enum.Enum):
    Small = (450, 300)
    Medium = (675, 450)
    Large = (900, 600)


class SynthesisPanel(wx.Panel):
    def __init__(self, parent, statusBar, main_color, second_color, models):
        self.use_synthesis = True
        wx.Panel.__init__(self, parent)
        # self.Bind(wx.EVT_SIZE, self.on_resize)
        self.statusBar = statusBar
        self.SetBackgroundColour(main_color)

        # create some sizers
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.hSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.hSizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.hSizer4 = wx.BoxSizer(wx.HORIZONTAL)

        # ------------------ hSizer1 ------------------ #

        self.upper_panel = wx.Panel(self, wx.ID_ANY)
        self.upper_panel.SetBackgroundColour(second_color)
        self.hSizer1.Add(self.upper_panel, 1, wx.EXPAND, 0)

        self.sizer_2 = wx.BoxSizer(wx.HORIZONTAL)

        path = get_absolute_path(
            'src/graphical_interface/buttons/load_button.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_ANY)
        self.button_load = wx.BitmapButton(
            self.upper_panel, id=wx.ID_ANY, bitmap=pic, size=(pic.GetWidth() - 3, pic.GetHeight() - 3))
        self.Bind(wx.EVT_BUTTON, self.on_load_click, self.button_load)
        self.sizer_2.Add(self.button_load, 0,
                         wx.TOP | wx.LEFT | wx.ALL, border=5)

        self.styles = models
        self.combobox = wx.ComboBox(
            self.upper_panel, choices=self.styles, value=self.styles[0], size=(80, -1))
        self.combobox.Bind(wx.EVT_COMBOBOX, self.on_combo)
        self.sizer_2.Add(self.combobox, 0,
                         wx.CENTER | wx.LEFT | wx.ALL, border=5)

        self.font_sizes = [str(x) for x in range(8, 25)]
        self.font_size_combobox = wx.ComboBox(
            self.upper_panel, choices=self.font_sizes, value='10', size=(80, -1))
        self.font_size_combobox.Bind(wx.EVT_COMBOBOX, self.on_combo)
        self.sizer_2.Add(self.font_size_combobox, 0,
                         wx.CENTER | wx.LEFT | wx.ALL, border=5)

        self.image_sizes = ['Small', 'Medium', 'Large']
        self.image_size_combobox = wx.ComboBox(
            self.upper_panel, choices=self.image_sizes, value='Medium', size=(80, -1))
        self.image_size_combobox.Bind(
            wx.EVT_COMBOBOX, self.on_image_size_combo)
        self.sizer_2.Add(self.image_size_combobox, 0,
                         wx.CENTER | wx.LEFT | wx.ALL, border=5)

        self.checkbox = wx.CheckBox(self.upper_panel, label='use GPU')
        self.checkbox.SetForegroundColour("white")
        self.sizer_2.Add(self.checkbox, 0, wx.CENTER | wx.ALL, border=5)

        path = get_absolute_path(
            'src/graphical_interface/buttons/save_button.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_ANY)
        self.button_save = wx.BitmapButton(
            self.upper_panel, id=wx.ID_ANY, bitmap=pic, size=(pic.GetWidth() - 3, pic.GetHeight() - 3))
        self.Bind(wx.EVT_BUTTON, parent.save, self.button_save)
        self.sizer_2.Add(self.button_save, 0,
                         wx.TOP | wx.LEFT | wx.ALL, border=5)

        path = get_absolute_path(
            'src/graphical_interface/buttons/render_button.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_ANY)
        self.button_render = wx.BitmapButton(
            self.upper_panel, id=wx.ID_ANY, bitmap=pic, size=(pic.GetWidth() - 3, pic.GetHeight() - 3))
        self.Bind(wx.EVT_BUTTON, self.on_render_click, self.button_render)
        self.sizer_2.Add(self.button_render, 0, wx.RIGHT | wx.ALL, border=5)

        self.sizer_2.AddStretchSpacer()

        path = get_absolute_path(
            'src/graphical_interface/buttons/recognition_button.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_ANY)
        self.change_panel = wx.BitmapButton(
            self.upper_panel, id=wx.ID_ANY, bitmap=pic, size=(pic.GetWidth() - 3, pic.GetHeight() - 3))
        self.Bind(wx.EVT_BUTTON, self.on_change_panel, self.change_panel)
        self.sizer_2.Add(self.change_panel, 0, wx.RIGHT | wx.ALL, border=5)

        self.upper_panel.SetSizer(self.sizer_2)
        # ------------------ hSizer1 ------------------ #

        # ------------------ hSizer2 ------------------ #

        self.hSizer2.AddStretchSpacer(1)
        self.editname = wx.TextCtrl(
            self, value='Test', style=wx.TE_MULTILINE)
        self.editname.SetMinSize(
            (300, 300))
        self.hSizer2.Add(self.editname, 30, wx.EXPAND, border=10)

        self.hSizer2.AddStretchSpacer(1)

        self.image_size = ImageSize.Medium
        img = wx.Image(self.image_size.value[0], self.image_size.value[1])
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY,
                                         wx.Bitmap(img))
        self.hSizer2.Add(self.imageCtrl, 50, wx.CENTER, border=10)

        self.hSizer2.AddStretchSpacer(1)
        # ------------------ hSizer2 ------------------ #

        self.hSizer3.AddStretchSpacer(1)
        self.hSizer4.AddStretchSpacer(1)

        self.mainSizer.Add(self.hSizer1, 0, wx.EXPAND)
        self.mainSizer.Add(self.hSizer3, 1, wx.EXPAND)
        self.mainSizer.Add(self.hSizer2, 30, wx.EXPAND)
        self.mainSizer.Add(self.hSizer4, 1, wx.EXPAND)
        self.SetSizerAndFit(self.mainSizer)

    def on_combo(self, event):
        path = combine_paths('./data/synthesis_models',
                             self.combobox.GetValue())
        print(path)

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

    def clear_directories(self, path):
        remove_dir_with_content(path + '/letters_dataset')
        remove_dir_with_content(path + '/training_dataset')
        ensure_create_dir(path + '/training_dataset')
        ensure_create_dir(path + '/training_dataset/letters')
        ensure_create_dir(path + '/training_dataset/skeletons')
        ensure_create_dir(path + '/training_dataset/combined')

    def on_load_click(self, event):
        """
        Creates new dataset from pictures from selected directory
        """
        md = wx.MessageDialog(self, message='Do you want to use the advanced mode?',
                              caption='Advanced mode', style=wx.YES_NO)
        options = []
        if md.ShowModal() == wx.ID_YES:
            ld = LoadDialog(None)
            if ld.ShowModal() == wx.ID_CANCEL:
                ld.Destroy()
                return
            options = process_options(ld)
            ld.Destroy()
        md.Destroy()

        path = get_absolute_path('src/graphical_interface/')
        self.clear_directories(path)

        dir = extract(self, path)
        if dir is None:
            return
        correct(self, dir)
        process_dataset(path + '/letters_dataset', options)
        resize_directory(path + '/letters_dataset',
                         path + '/training_dataset/letters')
        resize_skeletons_directory(
            path + '/letters_dataset', path + '/training_dataset/skeletons')
        combine_directory(path + '/training_dataset/letters',
                          path + '/training_dataset/skeletons', path + '/training_dataset/combined')
        train_command = 'python src/synthesis/pix2pix.py --mode train --output_dir src/graphical_interface/model/ --max_epochs 400 --input_dir src/graphical_interface/training_dataset/combined --which_direction BtoA --ngf 8 --ndf 8'
        os.system(train_command)
        export_command = 'python src/synthesis/pix2pix.py --mode export --output_dir src/graphical_interface/export/ --checkpoint src/graphical_interface/model/ --which_direction BtoA'
        os.system(export_command)
