# Chicken Monitor
These files are designed to utilize a Raspberry Pi with the Camera Module (RPi Zero W in my setup) and a second Raspberry Pi (RPi3 in my setup) acting as the web server and doing the Tensorflow calculations.

The RPi Zero Camera will take a picture every 5 seconds and upload that to the RPi3 into an images folder that the web server can render as a contact sheet (via the NGINX XSLT module).

The following are the files and where they should go:
- `chicken_monitor.py` --> this goes on the RPi Zero W Camera device
- `nginx-default` --> on the RPi3 as `/etc/nginx/sites-enabled/default`
- `gal.xslt` --> on the RPi3 as `/usr/share/nginx/gal.xslt`

## Install and operation
1. On the RPi Zero W with Camera
  - Install screen - `$ sudo apt-get install screen`
  - Put `chicken_monitor.py` on the device
  - Start screen - `screen`
  - Run `$ python3 chicken_monitor.py`
  - Exit screen - Ctrl-A Ctrl-D
  - To resume the screen session `screen -r`
2. On the RPi3
  - In the root of user pi's home folder `$ mkdir chickens chickens/images`
  - Install nginx and the xslt module - `$ sudo apt-get install nginx-simple libnginx-mod-http-xslt-filter`
  - Put `nginx-default` on the device as `/etc/nginx/sites-enabled/default`
  - Put `gal.xslt` on the device as `/usr/share/nginx/gal.xslt`
  - Create symbolic link for the images folder in /var/www/html - `$ sudo ln -s ~pi/chickens/images`
  - Restart nginx - `$ sudo systemctl restart nginx`
  - Periodically delete the images in `~pi/chickens/images` to keep the image contact sheet cleaner

## To Do
- [ ] Get Tensorflow working on the RPi3
- [ ] Get enough sample images to train a Tensorflow model to watch for chickens as well as for eggs
- [ ] More cameras to watch other locations
- [ ] Date tag the images in the file name and on the image itself (see the Keras image analysis tutorial)
- [ ] Recognize when there is a chicken or egg in the picture and only render those images to the web contact page
- [ ] Make the imageAnalysis.py a bit more flexible that just looking over an entire directory
