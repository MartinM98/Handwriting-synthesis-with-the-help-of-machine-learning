#!/bin/bash

<<<<<<< HEAD:tesseract-training/hardware-dependent/pacman/train-pacman.sh
=======


echo $1
cd "$1" # change direcotry to the direcotry with images for training

path=$(pwd)
listfile="listfile.txt" # name of the file listing training data files
tessdatapath="/usr/share/tessdata" # absoulte path to the directory containing traineddata's

if [ -f "$listfile" ]; then # check if a file with filename listfile exists
    rm "$listfile"
fi

touch "$listfile"

for filename in *.png; do # iterate trough all files with the tif extension
filename2="${filename%.*}" # extract filename without extension
tesseract $filename $filename2 -l eng wordstrbox # make box file ( based on filename the box file with the name filename2 is created) the .box file structure is described here: https://tesseract-ocr.github.io/tessdoc/TrainingTesseract-4.00#making-box-files
done

read -p "Correct the textboxes. After that press enter to continue the execution of the script
"

for filename in *.png; do # iterate trough all files with the tif extension
filename2="${filename%.*}" # extract filename without extension
tesseract $filename $filename2 --psm 7 lstm.train # create .lstm file ( based on filename the .lstm file with the name filename2 is created) the available --psm options are described here: https://github.com/tesseract-ocr/tesseract/issues/434
echo "$path"/"$filename2".lstmf >> "$listfile" # list the file absolute path in the listfile
done

sudo lstmtraining --sequential_training --net_spec '[1,48,0,1 Ct3,3,16 Mp3,3 Lfys64 Lfx96 Lrx96 Lfx512 O1c111]'   --traineddata "$tessdatapath"/eng.traineddata   --train_listfile "$path"/"$listfile" --model_output "$path"/result # train

sudo lstmtraining --stop_training --continue_from "$path"/result_checkpoint --traineddata "$tessdatapath"/eng.traineddata --model_output "$tessdatapath"/engnew.traineddata # combine the output files into traineddata. The eng.traineddata is improved which creates engnew.traineddata
