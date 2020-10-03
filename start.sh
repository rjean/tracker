cd /home/pi/follower
echo User:
whoami
until pids=$(pidof pigpiod)
do   
    sleep 1
done

/usr/bin/python3 controller.py

