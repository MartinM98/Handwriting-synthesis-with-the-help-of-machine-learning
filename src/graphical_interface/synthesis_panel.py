from src.image_processing.automated_functions import prepare_letters
from src.file_handler.file_handler import ensure_create_dir
from src.file_handler.file_handler import remove_dir_with_content
from src.image_processing.automated_functions import process_model_options
from src.graphical_interface.model_dialog import ModelDialog
from src.graphical_interface.options_dialog import OptionsDialog
from src.graphical_interface.create_text import TextImageRenderAllDifferentWidths
from src.graphical_interface.common import ChangePanelEvent, ImageSize, PIL2wx
from src.image_processing.letters import extract, correct
from src.image_processing.resize import resize_directory, combine_directory, resize_skeletons_directory
from src.synthesis.process import process_directory
from src.image_processing.automated_functions import process_dataset
from src.file_handler.file_handler import combine_paths, get_absolute_path
import wx
import os
import numpy as np


class SynthesisPanel(wx.Panel):
    def __init__(self, parent, statusBar, main_color, second_color, models):
        self.parent = parent
        self.use_synthesis = True
        self.path_to_model = './data/synthesis_models/1'
        self.n_advanced_options = 0
        self.k_advanced_options = 0
        self.filter_type = 'Original'
        self.match_with_other = False
        wx.Panel.__init__(self, parent)
        # self.Bind(wx.EVT_SIZE, self.on_resize)
        self.statusBar = statusBar
        self.SetBackgroundColour(main_color)
        self.use_gpu = False

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
            'resources/load_dataset_button.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        self.button_load_dataset = wx.BitmapButton(
            self.upper_panel, id=wx.ID_ANY, bitmap=pic, size=(pic.GetWidth() - 3, pic.GetHeight() - 3))
        self.Bind(wx.EVT_BUTTON, self.on_load_click, self.button_load_dataset)
        self.sizer_2.Add(self.button_load_dataset, 0,
                         wx.TOP | wx.LEFT | wx.ALL, border=5)

        path = get_absolute_path(
            'resources/generate_button.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        self.button_generate_font = wx.BitmapButton(
            self.upper_panel, id=wx.ID_ANY, bitmap=pic, size=(pic.GetWidth() - 3, pic.GetHeight() - 3))
        self.Bind(wx.EVT_BUTTON, self.on_generate, self.button_generate_font)
        self.sizer_2.Add(self.button_generate_font, 0,
                         wx.TOP | wx.LEFT | wx.ALL, border=5)

        self.styles = models
        self.styles.append('*New font*')
        self.combobox = wx.ComboBox(
            self.upper_panel, choices=self.styles, value=self.styles[0], size=(80, -1), style=wx.CB_READONLY)
        self.combobox.Bind(wx.EVT_COMBOBOX, self.on_combo)
        self.sizer_2.Add(self.combobox, 0,
                         wx.CENTER | wx.LEFT | wx.ALL, border=5)

        self.font_sizes = [str(x) for x in range(8, 25)]
        self.font_size_combobox = wx.ComboBox(
            self.upper_panel, choices=self.font_sizes, value='10', size=(80, -1))
        self.font_size_combobox.Bind(wx.EVT_COMBOBOX, self.on_combo)
        self.font_size_combobox.Hide()
        # self.sizer_2.Add(self.font_size_combobox, 0,
        #                  wx.CENTER | wx.LEFT | wx.ALL, border=5)

        # self.image_sizes = ['Small', 'Medium', 'Large']
        # self.image_size_combobox = wx.ComboBox(
        #     self.upper_panel, choices=self.image_sizes, value='Large', size=(80, -1))
        # self.image_size_combobox.Bind(
        #     wx.EVT_COMBOBOX, self.on_image_size_combo)
        # self.sizer_2.Add(self.image_size_combobox, 0,
        #                  wx.CENTER | wx.LEFT | wx.ALL, border=5)

        # self.checkbox = wx.CheckBox(self.upper_panel, label='use GPU')
        # self.checkbox.SetForegroundColour("white")
        # self.sizer_2.Add(self.checkbox, 0, wx.CENTER | wx.ALL, border=5)

        path = get_absolute_path(
            'resources/save_button.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        self.button_save = wx.BitmapButton(
            self.upper_panel, id=wx.ID_ANY, bitmap=pic, size=(pic.GetWidth() - 3, pic.GetHeight() - 3))
        self.Bind(wx.EVT_BUTTON, parent.save, self.button_save)
        self.sizer_2.Add(self.button_save, 0,
                         wx.TOP | wx.LEFT | wx.ALL, border=5)

        path = get_absolute_path(
            'resources/render_button.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        self.button_render = wx.BitmapButton(
            self.upper_panel, id=wx.ID_ANY, bitmap=pic, size=(pic.GetWidth() - 3, pic.GetHeight() - 3))
        self.Bind(wx.EVT_BUTTON, self.on_render_click, self.button_render)
        self.sizer_2.Add(self.button_render, 0, wx.RIGHT | wx.ALL, border=5)

        self.sizer_2.AddStretchSpacer()

        path = get_absolute_path(
            'resources/recognition_button.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
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

        self.image_size = ImageSize.Large
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
        if(self.combobox.GetValue() != '*New font*'):
            self.path_to_model = combine_paths(
                './data/synthesis_models', self.combobox.GetValue())
        else:
            current = self.new_font()
            self.combobox.Clear()
            self.combobox.Append(self.parent.find_models())
            self.combobox.Append('*New font*')
            self.path_to_model = combine_paths(
                './data/synthesis_models', current)

    def new_font(self):
        styles = self.parent.find_models()
        new = str(int(styles[-1]) + 1)
        ensure_create_dir('./data/synthesis_models/' + new)
        return new

    def chane_image_size(self, size):
        self.resize_image(size)
        # if size == self.image_sizes[0]:
        #     self.resize_image(ImageSize.Small)
        # elif size == self.image_sizes[1]:
        #     self.resize_image(ImageSize.Medium)
        # elif size == self.image_sizes[2]:
        #     self.resize_image(ImageSize.Large)

    def change_match_flag(self):
        self.match_with_other = not self.match_with_other

    def on_advanced_options(self):
        od = OptionsDialog(self, title='Advanced options', size=(250, 150))
        od.set_options(self.n_advanced_options, self.k_advanced_options)
        if od.ShowModal() == wx.ID_CANCEL:
            od.Destroy()
            return
        self.n_advanced_options = int(od.n.GetValue())
        self.k_advanced_options = int(od.k.GetValue())
        od.Destroy()

    def on_change_panel(self, event):
        evt = ChangePanelEvent()
        wx.PostEvent(self.Parent, evt)
        event.Skip()

    def resize_image(self, size):
        self.image_size = size
        img = self.imageCtrl.GetBitmap().ConvertToImage()
        img = img.Scale(size.value[0], size.value[1])
        self.imageCtrl.SetBitmap(wx.Bitmap(img))
        self.Layout()

    def clear_directories_render(self):
        self.statusBar.SetStatusText('Clearing directories...')
        remove_dir_with_content('./data/synthesis/synthesized')
        remove_dir_with_content('./data/synthesis/skeletons')
        print('')
        ensure_create_dir('./data/synthesis/skeletons')
        ensure_create_dir('./data/synthesis/synthesized')

    def check_model(self):
        if (os.path.isdir(combine_paths(self.path_to_model, 'letters_dataset')) and os.path.isdir(combine_paths(self.path_to_model, 'export'))):
            return True
        else:
            return False

    def on_render_click(self, event):
        """
        Creates a handwriting imitation image
        """
        if (self.check_model()):
            self.clear_directories_render()
            self.statusBar.SetStatusText('Preparing skeletons...')
            print("Preparing skeletons")
            prepare_letters(self.editname.GetValue(), combine_paths(self.path_to_model, 'letters_dataset'),
                            self.n_advanced_options, self.k_advanced_options, self.filter_type, int(self.font_size_combobox.GetValue()), self.match_with_other)
            self.statusBar.SetStatusText('Rendering text...')
            print("Rendering text")
            if (self.use_synthesis):
                process_directory(combine_paths(
                    self.path_to_model, 'export'), './data/synthesis/skeletons/', self.use_gpu)
                text_renderer = TextImageRenderAllDifferentWidths(
                    './data/synthesis/synthesized/', self.image_size.value[0], self.image_size.value[1], 50, self.editname.GetValue())
                img = text_renderer.create_synth_image()
            else:
                text_renderer = TextImageRenderAllDifferentWidths(
                    combine_paths(self.path_to_model, 'letters_dataset'), self.image_size.value[0], self.image_size.value[1], 50, self.editname.GetValue())
                img = text_renderer.create_image()

            if np.mean(img) == 255:
                self.statusBar.SetStatusText('There was an error or no input given')
                print("There was an error or no input given")
            else:
                self.statusBar.SetStatusText('Text rendered')
                print("Text rendered")
            self.imageCtrl.SetBitmap(PIL2wx(img))
            self.Layout()
        else:
            self.statusBar.SetStatusText('Model or dataset does not exist')
            print('Model or dataset does not exist')

    def clear_directories_generate(self, path):
        self.statusBar.SetStatusText('Clearing directories...')
        remove_dir_with_content(path + '/training_dataset')
        remove_dir_with_content(self.path_to_model + '/export')
        ensure_create_dir(path + '/training_dataset')
        ensure_create_dir(path + '/training_dataset/letters')
        ensure_create_dir(path + '/training_dataset/skeletons')
        ensure_create_dir(path + '/training_dataset/combined')

    def clear_directories_load(self, path):
        self.statusBar.SetStatusText('Clearing directories...')
        remove_dir_with_content(path + '/letters_dataset')
        ensure_create_dir(path + '/letters_dataset')

    def on_generate(self, event):
        """
        Creates new model based on pictures from dataset
        """
        self.clear_directories_generate('./data')
        self.statusBar.SetStatusText('Resizing letters...')
        resize_directory(self.path_to_model + '/letters_dataset',
                         './data/training_dataset/letters')
        self.statusBar.SetStatusText('Resizing skeletons...')
        resize_skeletons_directory(
            self.path_to_model + '/letters_dataset', './data/training_dataset/skeletons')
        self.statusBar.SetStatusText('Combining images...')
        combine_directory('./data/training_dataset/letters',
                          './data/training_dataset/skeletons', './data/training_dataset/combined')

        self.statusBar.SetStatusText('Select options')
        options = []
        md = ModelDialog(self, title='Model settings', size=(300, 200))
        if md.ShowModal() == wx.ID_CANCEL:
            self.statusBar.SetStatusText('Action cancelled')
            md.Destroy()
            return
        options = process_model_options(md)
        md.Destroy()
        self.statusBar.SetStatusText('Training model... (It may take a while)')
        print('TEST ' + str(self.use_gpu))
        train_command = 'python ./pix2pix.py --mode train --output_dir ./data/model/ --max_epochs ' + \
            str(options[0]) + ' --input_dir ./data/training_dataset/combined --which_direction BtoA --ngf ' + \
            str(options[1]) + ' --ndf ' + str(options[2]) + ' --use_gpu ' + str(self.use_gpu)
        os.system(train_command)
        self.statusBar.SetStatusText('Exporting model...')
        export_command = 'python ./pix2pix.py --mode export --output_dir ' + self.path_to_model + '/export/ --checkpoint ./data/model/ --which_direction BtoA --use_gpu ' + str(self.use_gpu)
        os.system(export_command)
        remove_dir_with_content('./data/model')
        if(self.check_model()):
            self.statusBar.SetStatusText('Model created successfully')
        else:
            self.statusBar.SetStatusText('There was an error during model generation')

    def on_load_click(self, event):
        """
        Creates new dataset from pictures from selected directory
        """
        self.statusBar.SetStatusText('Choose a directory')
        dd = wx.DirDialog(self, 'Choose a directory')
        if dd.ShowModal() != wx.ID_OK:
            dd.Destroy()
            self.statusBar.SetStatusText('Action cancelled')
            return
        directory = dd.GetPath()
        dd.Destroy()
        self.clear_directories_load(self.path_to_model)
        dir = extract(directory, self.path_to_model)
        if dir is None:
            self.statusBar.SetStatusText('An error occured')
            return
        self.statusBar.SetStatusText('Select incorrect letters')
        correct(self, dir)
        self.statusBar.SetStatusText('Processing dataset...')
        process_dataset(self.path_to_model + '/letters_dataset')
        self.statusBar.SetStatusText('Dataset uploaded')
