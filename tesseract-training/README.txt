The bash scripts residing in this directory may be used for installing
tesseract as well as training it ( it this case fine tune training is used).

There are three scripts:
- train-apt.sh : for Linux OSes with apt package manager
- train-brew.sh : for MacOS with brew package manager
- train-pacman.sh : for Linux OSes with pacman package manager

In order to use one of the available scripts one should run it with the 
argument being the path to the directory which conatins images which 
should be used for training ( the path may be either absolute 
or relative) Here are some examples:
    ./train-brew.sh relative/path/to/the/directory/with/images
    ./train-apt.sh /absoulte/path/to/the/directory/with/images

IMPORTANT: the images have to have the tif extension!

After running one of the above mentioned scripts the engnew.traineddata is created. The following line may be executed:
    tesseract -l engnew /path/to/the/image /filename/of/the/result/text/file # the -l option is used for choosing the language ( eng is used by default)