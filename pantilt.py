#sudo pigpiod to instanciate the Daemon.
import pigpio

pi = pigpio.pi()

HORIZONTAL_SERVO_GPIO=12
VERTICAL_SERVO_GPIO=16

HORIZONTAL_OFFSET=3 # Manually calibrated
VERTICAL_OFFSET=-17 # Manually calibrated

def center():
    set_raw_horizontal_angle(0+HORIZONTAL_OFFSET)
    set_raw_vertical_angle(0+VERTICAL_OFFSET)

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

def set_raw_horizontal_angle(angle):
    pi.set_servo_pulsewidth(HORIZONTAL_SERVO_GPIO, angle_to_pwm(angle))

def set_raw_vertical_angle(angle):
    pi.set_servo_pulsewidth(VERTICAL_SERVO_GPIO, angle_to_pwm(angle))


