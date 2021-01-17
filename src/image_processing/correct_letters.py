import os
import wx
from src.image_processing.letters import extract


def correct(_self, path=None):
    for r, d, f in os.walk(path):
        for folder in d:
            directory = os.path.join(r, folder)
            with wx.FileDialog(_self, 'Choose a directory', defaultDir=directory, style=wx.TE_MULTILINE) as fd:
                fd.ShowModal()
                files = fd.GetPaths()
            files = list(files)
            for file in files:
                os.remove(file)
            if not os.listdir(directory):
                os.rmdir(directory)
            else:
                i = 0
                for filename in sorted(os.listdir(directory), key=lambda x: int(x[:-4])):
                    os.rename(directory + '/' + filename,
                              directory + '/' + str(i) + '.png')
                    i += 1


if __name__ == '__main__':
    letters = extract()
    correct(letters)
