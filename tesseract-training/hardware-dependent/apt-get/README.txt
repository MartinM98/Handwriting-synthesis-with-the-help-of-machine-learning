The bash scripts residing in this directory may be used for installing
tesseract as well as training it ( it this case fine tune training is used).

There are two scripts:
- install_tesseract.sh : installs tesseract itself and training tools (should be run only once)
- train-apt.sh : trains tesseract

In order to use the train-apt.sh script one should run it with the 
argument being the path to the directory which conatins images which 
should be used for training ( the path may be either absolute 
or relative) Here are a example:
    ./train-apt.sh /absoulte/path/to/the/directory/with/images

IMPORTANT: the images have to have the tif extension!

After running one of the above mentioned scripts the engnew.traineddata is created. The following line may be executed:
    tesseract -l engnew /path/to/the/image /filename/of/the/result/text/file # the -l option is used for choosing the language ( eng is used by default)