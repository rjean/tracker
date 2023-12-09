#import the lgpio module for the rapberry pi
import gpiozero

HORIZONTAL_SERVO_GPIO=13
VERTICAL_SERVO_GPIO=12
from time import sleep

class TurretServoController:
    def __init__(self, vertical_offset_degrees=-15, horizontal_offset_degrees=0):
        self.horizontal_servo = gpiozero.Servo(HORIZONTAL_SERVO_GPIO, min_pulse_width=0.0005, max_pulse_width=0.0025)
        self.vertical_servo = gpiozero.Servo(VERTICAL_SERVO_GPIO, min_pulse_width=0.0005, max_pulse_width=0.0025)
        self.vertical_offset_degrees = vertical_offset_degrees
        self.horizontal_offset_degrees = horizontal_offset_degrees

    @property
    def horizontal_angle_degrees(self):
        return self.horizontal_servo.value * 90
    
    @horizontal_angle_degrees.setter
    def horizontal_angle_degrees(self, angle):
        self.horizontal_servo.value = angle / 90

    @property
    def vertical_angle_degrees(self):
        return self.vertical_servo.value * 90 + self.vertical_offset_degrees
    
    @vertical_angle_degrees.setter
    def vertical_angle_degrees(self, angle, min_angle=0, max_angle=45):
        angle = min(max_angle, max(min_angle, angle))
        angle += self.vertical_offset_degrees
        self.vertical_servo.value = angle / 90

def test_horizontal_servo():
    # create a servo object for the horizontal servo
    horizontal_servo = gpiozero.Servo(HORIZONTAL_SERVO_GPIO, min_pulse_width=0.0005, max_pulse_width=0.0025)
    for i in range(0, 2):
        horizontal_servo.value = 1
        sleep(1)
        horizontal_servo.value = -1
        sleep(1)

    # set the horizontal servo to 0
    horizontal_servo.value = 0
    sleep(1)

def test_vertical_servo():
    # create a servo object for the horizontal servo
    vertical_servo = gpiozero.Servo(VERTICAL_SERVO_GPIO, min_pulse_width=0.0005, max_pulse_width=0.0025)
    for i in range(0, 2):
        vertical_servo.value = 1
        sleep(1)
        vertical_servo.value = -1
        sleep(1)

    # set the horizontal servo to 0
    vertical_servo.value = 0
    sleep(1)

def test_servo_controller():
    controller = TurretServoController()
    for i in range(0, 2):
        controller.horizontal_angle_degrees = -90
        sleep(1)
        controller.horizontal_angle_degrees = 90
        sleep(1)
        controller.vertical_angle_degrees = 0
        sleep(1)
        controller.vertical_angle_degrees = 90
        sleep(1)

    # set the horizontal servo to 0
    controller.horizontal_angle_degrees = 0
    controller.vertical_angle_degrees = 0
    sleep(1)

