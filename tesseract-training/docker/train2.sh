#!/bin/bash

cd /root/tesstrain # change direcotry to the direcotry with images for training

path=$(pwd)
listfile="listfile.txt" # name of the file listing training data files
tessdatapath="/usr/share/tesseract-ocr/4.00/tessdata" # absoulte path to the directory containing traineddata's

for filename in *.tif; do # iterate trough all files with the tif extension
filename2="${filename%.*}" # extract filename without extension
tesseract $filename $filename2 --psm 7 lstm.train # create .lstm file ( based on filename the .lstm file with the name filename2 is created) the available --psm options are described here: https://github.com/tesseract-ocr/tesseract/issues/434
echo "$path"/"$filename2".lstmf >> "$listfile" # list the file absolute path in the listfile
done

lstmtraining --sequential_training --net_spec '[1,48,0,1 Ct3,3,16 Mp3,3 Lfys64 Lfx96 Lrx96 Lfx512 O1c111]'   --traineddata "$tessdatapath"/eng.traineddata   --train_listfile "$path"/"$listfile" --model_output "$path"/result # train

lstmtraining --stop_training --continue_from "$path"/result_checkpoint --traineddata "$tessdatapath"/eng.traineddata --model_output "$tessdatapath"/engnew.traineddata # combine the output files into traineddata. The eng.traineddata is improved which creates engnew.traineddata
