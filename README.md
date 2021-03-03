# Handwriting-synthesis-with-the-help-of-machine-learning

Handwriting synthesis with the help of machine learningThis engineering work aimed to create a program that imitates handwriting, based on a datasetconsisting of handwritten text images. For this reason, the project contains two main parts.The first is responsible for processing the input image, recognising the handwriting and ex-tracting the individual characters. The recognition module is based on an existing mechanicalhandwriting recognition model, modified to recognise handwriting. A collection containing ex-amples of different handwriting styles has been used to achieve this.The second, much more extensive part of the work is responsible for mapping the appropriatehandwriting style. It is based on the results of the first module. From the extracted images,skeletons and corresponding sequences of control points are created. This data is then processedand combined in various configurations to create a new, correct skeleton. The resulting letterbase is different from all input data while retaining its unique character. Then comes the finalstage of synthesis. The new letters’ final version is created based on the skeletons created andusing the previously trained model. The only thing left to do is to combine letters into wordsand words into sentences.For the convenience of use, a graphic interface has also been created, allowing for an easy andclear way not only to recognise the text in a selected photo or create a synthesis of a letter butalso to interfere with these processes or create a new style of imitation. By inputting photos ofthe script, the user can create their font, and thanks to extensive parameterisable options, theycan improve the results. Of course, the program is configurable, and the authors have left thedoor open for entering other models.

Authors: <br/>
[Martin Mrugała](https://github.com/MartinM98) <br/>
[Patryk Walczak](https://github.com/Walczi123) <br/>
[Bartłomiej Żyła](https://github.com/zbartkus3150) <br/>

Installation instruction

The installation process is straightforward, consisting of just a few steps. In this section,instructions on installing and running the application depending on the selected system areexplained. It is enough for the user to choose an appropriate section and follow the describedsteps

Tesseract
The Tesseract OCR is suitable for many operating systems. There are prepared installationinstructions for Windows, Mac OS and Linux.

Windows
On Windows, the Tesseract OCR may not be installed with the code from it’s official GitHubrepository. The Tesseract at UB Mannheim version is for Windows. In order to install it, onehas to download the installer exec file and run it. The training tools may be added during theinstallation.

Mac OS
On this operating system the Tesseract OCR may be installed with Homebrew with thefollowing command:brew install tesseract # install tesseract

Linux
•Pacman:
sudo pacman -Sy tesseract # install tesseract
sudo pacman -Sy tesseract-data-eng # install english language
•Apt-get:
sudo apt-get install tesseract-ocr # install tesseract

Repository
For the control version, the GitHub platform was used, and there therepositoryis available.Moreover, the project’s set up contains only three commands (if the project is already down-loaded).
First step after downloading the project (and suitable Python) is checking and install allrequired libraries by
pip install -r requirements.txt
Next compile project using
pip install .
And last step, run graphical_interface.py
python src/graphical_interface/graphical_interface.py
After all the steps, the GUI shows, and the whole project is ready to use if Tesseract is installed.Otherwise, the first subsection describes the process of installing Tesseract.

Executable
The program has been compiled, and two executable versions of the application are availableonthe MEGa drive. The compressed application contains all needed libraries and is readyto use after decompression. There is no need for installation process if the Tesseract is alreadyinstalled. Otherwise no then he first subsection describes the process of installing Tesseract.Of course, choose Scripturam_Win10.zip for Windows 10 operating system and Scrip-turam_macOS.zip for computers with the macOS system.

Training dataset:

- [fki IAM Handwriting Database](http://www.fki.inf.unibe.ch/databases/iam-handwriting-database)

Cloud materials:

- https://mega.nz/folder/u81BhBYL#DPL0Z5TMQM9MSahIhLnnDw

Execuatble application:

- https://mega.nz/folder/fplijIqY#1pfGuol85CVme2IpYVeHBw
