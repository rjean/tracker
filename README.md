# Tracker
Small hobby project for a device that can track things using a pan tilt system using the RaspberryPI.

The idea is to be able to build a unofficial "Portal Sentry Turret: https://theportalwiki.com/wiki/Sentry_Turret".

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
## Communication
A custom built "rtcom" library is used for communication.

It works by broadcasting endpoints on the network over UDP. 

## User Interface
The UI is handle by the video_reader.py file. It should be run on a PC, not on the raspberry pi.

As of now, it diplays the feed from the follower.

```
python video_reader.py
```

## Camera
Make sure the camera is enabled:
````
sudo raspi-config
interfacing options->camera->enable the camera
````

## AI 
The controller requires a Coral USB Accelerator for embedded inference. https://coral.ai/docs/accelerator/get-started/.

curl -OL "https://github.com/google-coral/edgetpu/raw/master/test_data/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite"

## Run at startup
See https://www.tomshardware.com/how-to/run-script-at-boot-raspberry-pi

Edit crontab for the user:
```
pi@turret:~ $ crontab -e
```

And add that line:
```
@reboot bash /home/pi/follower/start.sh > /home/pi/follower/start.log 2>&1
```

# Starting the controller.
On the raspberry pi, run 
``` 
python3 controller.py
```
