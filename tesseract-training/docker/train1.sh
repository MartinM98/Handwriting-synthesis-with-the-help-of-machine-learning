#!/bin/bash

cd /root/tesstrain # change direcotry to the direcotry with images for training

path=$(pwd)
listfile="listfile.txt" # name of the file listing training data files
tessdatapath="/usr/share/tesseract-ocr/4.00/tessdata" # absoulte path to the directory containing traineddata's

if [ -f "$listfile" ]; then # check if a file with filename listfile exists
    rm "$listfile"
fi

touch "$listfile" 

for filename in *.tif; do # iterate trough all files with the tif extension
filename2="${filename%.*}" # extract filename without extension
tesseract $filename $filename2 -l eng wordstrbox # make box file ( based on filename the box file with the name filename2 is created) the .box file structure is described here: https://tesseract-ocr.github.io/tessdoc/TrainingTesseract-4.00#making-box-files
done

echo "Correct the textboxes. After that run the train2.sh script"