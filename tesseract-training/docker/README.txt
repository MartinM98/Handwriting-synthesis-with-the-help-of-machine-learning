This is a platform independent way of training tesseract. The procedure is as follows:

First, install Docker Desktop. You can do it using this link:
https://docs.docker.com/engine/install/

Next, run the create_container.sh script. It will create a container with Ubuntu image. 
This script needs one argument so that it could work properly. This argument should be a path ( either absolute or relative ) 
to a directory containing images that should be used for training.

After that the container's shell is opened. That is the time when install_tesseract.sh script should be run.
It installs tesseract with training tools. The important thing is that it is neccessary to run this script, 
as well as create_container.sh, only once.(When we want to create the container)

The training itself is done with two scripts - train1.sh and train2.sh. One should start with the train1.sh, of course.
In order to train the tesseract one should run test1.sh script. Next step is to correct files 
with .box extension in the /root/tesstrain directory. The last thing to do is to run train2.sh script.

After all above described steps are completed successfully, the engnew.traineddata can be found in the 
/usr/share/tesseract-ocr/4.00/tessdata directory.