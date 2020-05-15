#sudo pigpiod to instanciate the Daemon.
import pigpio

pi = pigpio.pi()

def center():
    set_horizontal_angle(0)
    set_vertical_angle(0)

def angle_to_pwm(angle, min=-90, max=90):
    #Saturate the angle.
    if angle > max:
        angle=max
    if angle < min:
        angle=min
    min_pwm = 500 # Corresponds to -90 degrees.
    max_pwm = 2500 # Corresponds to 90 degress.
    m = (max_pwm-min_pwm) / (max-min)
    b = -m * min + min_pwm
    return m * angle + b

def set_horizontal_angle(angle):
    pi.set_servo_pulsewidth(12, angle_to_pwm(angle))

def set_vertical_angle(angle):
    pi.set_servo_pulsewidth(16, angle_to_pwm(angle))

center()

