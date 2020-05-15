#sudo pigpiod to instanciate the Daemon.
import pigpio

pi = pigpio.pi()

pi.set_servo_pulsewidth(12, 1500)
pi.set_servo_pulsewidth(16, 1500)

