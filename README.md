# Self-Driving-Pi-Car
## This is a project to create a self-driving car using a Raspberry Pi 3B and using the libraries **OpenCV** and **face_recognition**. 
### Below we have the instructions on how to set up all the required applications and libraries to ensure that you can compile OpenCV on your RPi.


OpenCV (Open Source Computer Vision Library) is an open source computer vision library and has bindings for C++, Python, and Java. It is has a multitude of applications including medical image analysis, stitching street view images, surveillance video, detecting and recognizing faces, tracking moving objects, extracting 3D models and much more.

In this guide we will be training the car to drive in circles until it detects a labrador. In which case it will drive directly towards it.

it is worth noting while the actual downloading and installation of the requisite parts are very fast, the actual build process can take 4-6 hours or longer due to the processing power of the Raspberry Pi! Once you've built it once, you won't have to re-build it again though so it's imperative you follow the instructions below line by line in the exact order outlined.

## Prerequisites
You must have the [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) operating system installed on your Raspberry Pi 3.
Python 2.7 **and** Python 3 installed

## Downloading and Installing OpenCV ~ 6+ Hours of work
Install OpenCV by building the library from the source. You will have complete control over the build options and OpenCV will be optimized for your system.
Begin by increasing your swap space to ensure that the build does not hang due to the low memory capacity. Be sure to switch this back after the build - this is an easy way to burn out your SD card!

``` bash
$ sudo nano /etc/dphys-swapfile
```
Change the `CONF_SWAPSIZE` value from the default `100` to `2048`
Save the file and restart the service for the change to take effect:
``` Bash
$ sudo /etc/init.d/dphys-swapfile restart
```

Now we must start to install and the required tools and dependencies for the OpenCV build. Carry out the below commands in order.
``` bash
$ sudo apt update
$ sudo apt install build-essential cmake git pkg-config libgtk-3-dev "libcanberra-gtk*"
$ sudo apt install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev
$ sudo apt install libjpeg-dev libpng-dev libtiff-dev gfortran openexr libatlas-base-dev opencl-headers
$ sudo apt install python3-dev python3-numpy libtbb2 libtbb-dev libdc1394-22-dev
```

Create the build directory and navigate to it. Clone the OpenCV and OpenCV contrib repositories from Github. At the time of writing, the most up to date version that will be installed will be 4.1.2
``` bash
$ mkdir ~/opencv_build && cd ~/opencv_build
$ git clone https://github.com/opencv/opencv.git
$ git clone https://github.com/opencv/opencv_contrib.git
```

Once the repositories have been successfully cloned, navigate to the opencv directory and create a temporary build directory.

``` bash
$ mkdir -p ~/opencv_build/opencv/build && cd ~/opencv_build/opencv/build
```

Set up the build configuration using `cmake`
``` bash
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D ENABLE_NEON=ON \
    -D OPENCV_EXTRA_EXE_LINKER_FLAGS=-latomic \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_build/opencv_contrib/modules \
    -D BUILD_EXAMPLES=OFF ..
```

You should see that the bottom 3 lines should give you confirmation of a successful output.
``` bash
-- Configuring done
-- Generating done
-- Build files have been written to: /home/pi/opencv_build/opencv/build
```

run `make` to start the 4 hour+ long compilation process.
``` bash
$ make -j4
```

Once this is complete (this took me 6 hours, so be patient with it!) you should see the below output
```
[100%] Linking CXX shared module ../../lib/python3/cv2.cpython-35m-arm-linux-gnueabihf.so
[100%] Built target opencv_python3
```

The final step is to install the compiled OpenCV files.
``` bash
$ sudo make install
```

You should see another success message output to the shell.
``` bash
-- Installing: /usr/local/bin/opencv_version
-- Set runtime path of "/usr/local/bin/opencv_version" to "/usr/local/lib"
```

You can confirm whether this has been successful by importing the OpenCV library `cv2` in a python script
``` bash
python3 -c "import cv2; print(cv2.__version__)"
```

output:
``` bash
4.1.2 dev
```

## Final steps and clean-up
You can delete the source files if you are running low on space
``` bash
rm -rf ~/opencv_build
```

As we mentioned above, restore the `CONF_SWAPSIZE` back to `100`
``` bash
sudo nano /etc/dphys-swapfile
```
`CONF_SWAPSIZE=100`

Restart the service for it to take effect
``` bash
sudo /etc/init.d/dphys-swapfile restart
```

## Further Steps
Work in Progress - will be updated soon! - Hridai 14th Nov 2019
