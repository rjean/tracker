# Follower
Small hobby project for a device that can track things using a laser pointer and a pan tilt system using the RaspberryPI. 

# Architecture
## User Interface
The basic UI is to be done via WebSockets. A static HTML page is served using NGINX

sudo apt install nginx

# Camera
Using pistreaming.
cd pistreaming
python3 server.py&

