import gpiozero

HORIZONTAL_SERVO_GPIO=13
VERTICAL_SERVO_GPIO=12
from time import sleep

class TurretServoController:
    """A class to control the servos on the turret"""
    def __init__(self, vertical_offset_degrees:float=-15, horizontal_offset_degrees:float=0):
        self.horizontal_servo = gpiozero.Servo(HORIZONTAL_SERVO_GPIO, min_pulse_width=0.0005, max_pulse_width=0.0025)
        self.vertical_servo = gpiozero.Servo(VERTICAL_SERVO_GPIO, min_pulse_width=0.0005, max_pulse_width=0.0025)
        self.vertical_offset_degrees = vertical_offset_degrees
        self.horizontal_offset_degrees = horizontal_offset_degrees

    @property
    def horizontal_angle_degrees(self) -> float:
        return self.horizontal_servo.value * 90
    
    @horizontal_angle_degrees.setter
    def horizontal_angle_degrees(self, angle:float) -> None:
        self.horizontal_servo.value = angle / 90

    @property
    def vertical_angle_degrees(self) -> float:
        return self.vertical_servo.value * 90 + self.vertical_offset_degrees
    
    @vertical_angle_degrees.setter
    def vertical_angle_degrees(self, angle:float, min_angle:float=0, max_angle:float=45):
        angle = min(max_angle, max(min_angle, angle))
        angle += self.vertical_offset_degrees
        self.vertical_servo.value = angle / 90
