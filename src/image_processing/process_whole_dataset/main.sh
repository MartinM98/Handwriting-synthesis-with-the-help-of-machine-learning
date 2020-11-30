#/bin/bash

for dir in $(find PATH_TO_THE_DIRECTORY -type d);
do
    mkdir $dir/skel/
    python3 skeletonize_live.py $dir
    python3 gabor_live.py $dir/skel/
done