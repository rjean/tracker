#sudo pigpiod to instanciate the Daemon.
import pigpio
import argparse

pi = pigpio.pi()

HORIZONTAL_SERVO_GPIO=12
VERTICAL_SERVO_GPIO=16

HORIZONTAL_OFFSET=3 # Manually calibrated
VERTICAL_OFFSET=-17 # Manually calibrated


def power_off():
    pi.set_servo_pulsewidth(HORIZONTAL_SERVO_GPIO, 0)
    pi.set_servo_pulsewidth(VERTICAL_SERVO_GPIO, 0)
    
def center():
    set_raw_horizontal_angle(0+HORIZONTAL_OFFSET)
    set_raw_vertical_angle(0+VERTICAL_OFFSET)

def angle_to_pwm(angle, min=-90, max=90):
    #Saturate the angle.
    angle = saturate(angle, min, max)
    min_pwm = 500 # Corresponds to -90 degrees.
    max_pwm = 2500 # Corresponds to 90 degress.
    m = (max_pwm-min_pwm) / (max-min)
    b = -m * min + min_pwm
    return m * angle + b

def saturate(value, min, max):
    if value < min:
        value=min
    if value > max:
        value=max
    return value

def set_horizontal_angle(angle, min=-90, max=90):
    angle=saturate(angle,min,max)
    set_raw_horizontal_angle(angle+HORIZONTAL_OFFSET)

def set_vertical_angle(angle, min=-25,max=25):
    angle=saturate(angle,min,max)
    set_raw_vertical_angle(angle+VERTICAL_OFFSET)

def set_raw_horizontal_angle(angle):
    pi.set_servo_pulsewidth(HORIZONTAL_SERVO_GPIO, angle_to_pwm(angle))

def set_raw_vertical_angle(angle):
    pi.set_servo_pulsewidth(VERTICAL_SERVO_GPIO, angle_to_pwm(angle))


def main():
    print("Hello World!")

if __name__ == "__main__":
    main()
    