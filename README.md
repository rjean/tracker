# Follower
Small hobby project for a device that can track things using a laser pointer and a pan tilt system using the RaspberryPI. 
# Setup.
Install the required packages:

```
pip3 install -r requirements.txt
```
Make sure the gpio daemon is started when the raspberry pi boots:
```
sudo systemctl enable pigpiod
```

# Architecture
## User Interface
The basic UI is to be done via WebSockets. A static HTML page is served using NGINX

```
sudo apt install nginx
```
We need to make the "www" subfolder available to NGINX. 
```
sudo rm /var/www/html/
sudo rmdir /var/www/html/
sudo ln -s www /var/www/html
```

# Camera
## First-time setup.
Make sure the pistreaming module has been properly imported:
```
git submodule init
git submodule update
```
Make sure the camera is enabled:
````
sudo raspi-config
interfacing options->camera->enable the camera
````

To start the camera, ising pistreaming:

```
cd pistreamingls
python3 server.py&
``

# AI 
curl -OL "https://github.com/google-coral/edgetpu/raw/master/test_data/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite"

# Run at startup
See https://www.tomshardware.com/how-to/run-script-at-boot-raspberry-pi

Edit crontab for the user:
```
pi@turret:~ $ crontab -e
```

And add that line:
```
@reboot bash /home/pi/follower/start.sh > /home/pi/follower/start.log 2>&1
```
