#import the lgpio module for the rapberry pi
import gpiozero

from turret.servo import TurretServoController, HORIZONTAL_SERVO_GPIO, VERTICAL_SERVO_GPIO
from time import sleep

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

