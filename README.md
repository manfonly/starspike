# starspike
star spike is a python script to add lens spikes on the starry photo, it's a demo project for opencv image processing API.
![](https://github.com/manfonly/starspike/blob/main/output.jpg?raw=true)

Dependencies
=======
python 3.x

opencv

Installation
=======
       pip install python-opencv

Quick Start
=======
**Get basic help info:

      python ./run.py -h
      usage: run.py [-h] [-i IMAGE] [-t THRESHOLD] [-r RADIUS] [-w WATERMARK]
                    [-n SPIKENUM]

      optional arguments:
        -h, --help            show this help message and exit
        -i IMAGE, --image IMAGE
                              path to the image file
        -t THRESHOLD, --threshold THRESHOLD
                              high light threshold(1-255)
        -r RADIUS, --radius RADIUS
                              Output light point radius threshold
        -w WATERMARK, --watermark WATERMARK
                              Add water mark image
        -n SPIKENUM, --spikenum SPIKENUM
                              Number of spikes
**Example.1 Processing existing photo:

       python ./run.py -i testimg.jpg
 
**Example.2 Processing user's photo:

       python ./run.py -i userphoto.jpg
