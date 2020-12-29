from src.graphical_interface.create_text import TextImageRenderAllDifferentWidths
from src.graphical_interface.common import ChangePanelEvent, PIL2wx
from src.image_processing.letters import extract, correct
from src.image_processing.resize import resize_directory, combine_directory, resize_skeletons_directory
from src.synthesis.process import process_directory
from src.image_processing.automated_functions import process_dataset
from src.file_handler.file_handler import combine_paths, ensure_create_and_append_file, get_absolute_path, read_from_file
import wx
import os
import enum
from src.graphical_interface.load_dialog import LoadDialog
from src.graphical_interface.model_dialog import ModelDialog
from src.image_processing.automated_functions import process_options, process_model_options
from src.file_handler.file_handler import remove_dir_with_content
from src.file_handler.file_handler import ensure_create_dir
from src.image_processing.automated_functions import prepare_letters


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
            'img/load_dataset_button.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        self.button_load_dataset = wx.BitmapButton(
            self.upper_panel, id=wx.ID_ANY, bitmap=pic, size=(pic.GetWidth() - 3, pic.GetHeight() - 3))
        self.Bind(wx.EVT_BUTTON, self.on_load_click, self.button_load_dataset)
        self.sizer_2.Add(self.button_load_dataset, 0,
                         wx.TOP | wx.LEFT | wx.ALL, border=5)

        path = get_absolute_path(
            'img/generate_button.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        self.button_generate_font = wx.BitmapButton(
            self.upper_panel, id=wx.ID_ANY, bitmap=pic, size=(pic.GetWidth() - 3, pic.GetHeight() - 3))
        self.Bind(wx.EVT_BUTTON, self.on_generate, self.button_generate_font)
        self.sizer_2.Add(self.button_generate_font, 0,
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
            self.upper_panel, choices=self.image_sizes, value='Large', size=(80, -1))
        self.image_size_combobox.Bind(
            wx.EVT_COMBOBOX, self.on_image_size_combo)
        self.sizer_2.Add(self.image_size_combobox, 0,
                         wx.CENTER | wx.LEFT | wx.ALL, border=5)

        self.checkbox = wx.CheckBox(self.upper_panel, label='use GPU')
        self.checkbox.SetForegroundColour("white")
        self.sizer_2.Add(self.checkbox, 0, wx.CENTER | wx.ALL, border=5)

        path = get_absolute_path(
            'img/save_button.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        self.button_save = wx.BitmapButton(
            self.upper_panel, id=wx.ID_ANY, bitmap=pic, size=(pic.GetWidth() - 3, pic.GetHeight() - 3))
        self.Bind(wx.EVT_BUTTON, parent.save, self.button_save)
        self.sizer_2.Add(self.button_save, 0,
                         wx.TOP | wx.LEFT | wx.ALL, border=5)

        path = get_absolute_path(
            'img/render_button.png')
        pic = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        self.button_render = wx.BitmapButton(
            self.upper_panel, id=wx.ID_ANY, bitmap=pic, size=(pic.GetWidth() - 3, pic.GetHeight() - 3))
        self.Bind(wx.EVT_BUTTON, self.on_render_click, self.button_render)
        self.sizer_2.Add(self.button_render, 0, wx.RIGHT | wx.ALL, border=5)

        self.sizer_2.AddStretchSpacer()

        path = get_absolute_path(
            'img/recognition_button.png')
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

    def clear_directories_render(self):
        remove_dir_with_content(get_absolute_path(
            './src/graphical_interface/synthesis/synthesized/'))
        remove_dir_with_content(get_absolute_path(
            './src/graphical_interface/synthesis/skeletons/'))
        ensure_create_dir(get_absolute_path(
            './src/graphical_interface/synthesis/skeletons/'))
        ensure_create_dir(get_absolute_path(
            './src/graphical_interface/synthesis/synthesized/'))

    def on_render_click(self, event):
        """
        Creates a handwriting imitation image
        """
        self.clear_directories_render()
        prepare_letters(self.editname.GetValue())

        use_gpu = self.checkbox.GetValue()
        if (self.use_synthesis):
            process_directory(get_absolute_path(
                './src/graphical_interface/export'), get_absolute_path('./src/graphical_interface/synthesis/skeletons/'), use_gpu)
            text_renderer = TextImageRenderAllDifferentWidths(
                get_absolute_path('./src/graphical_interface/synthesis/synthesized/'), self.image_size.value[0], self.image_size.value[1], 50, self.editname.GetValue())
            img = text_renderer.create_synth_image()
        else:
            text_renderer = TextImageRenderAllDifferentWidths(
                get_absolute_path('./src/graphical_interface/letters_dataset/'), self.image_size.value[0], self.image_size.value[1], 50, self.editname.GetValue())
            img = text_renderer.create_image()

        self.imageCtrl.SetBitmap(PIL2wx(img))
        self.Layout()

    def clear_directories_load(self, path):
        remove_dir_with_content(path + '/letters_dataset')
        remove_dir_with_content(path + '/training_dataset')
        ensure_create_dir(path + '/training_dataset')
        ensure_create_dir(path + '/training_dataset/letters')
        ensure_create_dir(path + '/training_dataset/skeletons')
        ensure_create_dir(path + '/training_dataset/combined')

    def on_generate(self, event):
        print('generate')

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
        dd = wx.DirDialog(self, 'Choose a directory')
        if dd.ShowModal() != wx.ID_OK:
            dd.Destroy()
            return
        directory = dd.GetPath()
        dd.Destroy()
        path = get_absolute_path('src/graphical_interface/')
        self.clear_directories_load(path)

        dir = extract(directory, path)
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

        options = []
        md = ModelDialog(self, title='Model settings', size=(300, 200))
        if md.ShowModal() == wx.ID_CANCEL:
            md.Destroy()
            return
        options = process_model_options(md)
        md.Destroy()

        train_command = 'python src/synthesis/pix2pix.py --mode train --output_dir src/graphical_interface/model/ --max_epochs ' + \
            str(options[0]) + ' --input_dir src/graphical_interface/training_dataset/combined --which_direction BtoA --ngf ' + \
            str(options[1]) + ' --ndf ' + str(options[2])
        os.system(train_command)
        export_command = 'python src/synthesis/pix2pix.py --mode export --output_dir src/graphical_interface/export/ --checkpoint src/graphical_interface/model/ --which_direction BtoA'
        os.system(export_command)


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
        self.panel = "synthesis"

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.synthesis_panel, 1, wx.EXPAND)
        self.sizer.SetMinSize(1400, 700)
        self.SetSizerAndFit(self.sizer)

        self.Bind(wx.EVT_CLOSE, self.on_close)

        menuBar = wx.MenuBar()
        # ------------------ menu - File ------------------ #
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_SAVE, "S&ave\tAlt-S", helpString="Save result")

        file_menu.Append(wx.ID_OPEN, "L&oad\tAlt-L", helpString="Load text")

        menuBar.Append(file_menu, "&File")
        # ------------------ menu - File ------------------ #

        # ------------------ menu - Options ------------------ #
        option_menu = wx.Menu()
        option_menu.Append(wx.ID_EXIT, "E&xit\tAlt-X",
                           "Exit this simple sample")

        menuBar.Append(option_menu, "&Options")
        # ------------------ menu - Options ------------------ #

        # ------------------ menu - About ------------------ #
        about_menu = wx.Menu()
        about_menu.Append(wx.ID_ABOUT, "A&bout the project\tAlt-A",
                          "Show informations about the application")

        about_menu.Append(100, "Au&tors\tAlt-U",
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

    def menuhandler(self, event):
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
        else:
            self.synthesis_panel.editname.SetValue(
                self.recognition_panel.editname.GetValue())
            self.synthesis_panel.Show()
            self.recognition_panel.Hide()
            self.statusBar.SetStatusText("Synthesis Mode")
            self.panel = "synthesis"
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
