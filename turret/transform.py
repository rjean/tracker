# Coordinate transformation module.
# Will be used to convert location in pixels to angles commands for the pan tile
# module.

# Defaults units for this module will be millimeters.
import math

class Camera():
    #Defaults for the camera module are the intrisinc parameters for
    #the RaspberryPi camera.
    # https://elinux.org/Rpi_Camera_Module#Technical_Parameters_.28v.2_board.29
    # Pixel Size: 1.12 x 1.12 um
    # Pixel Count: 3280 x 2464 (active pixels) 3296 x 2512 (total pixels)
    # Lens: f=3.04 mm, f/2.0
    # Sensor size: 3.674 x 2.760 mm (1/4" format)
    def __init__(self, model="Pi2"):
        if model=="Pi2":
            self.focal_length = 3.04 #3.04mm
            self.pixel_size = (3.674/3296, 2.760/2512) #1.12 µM
            self.sensor_resolution = (3296, 2512)

    def pixel_to_sensor_position(self, position, image_resolution):
        x, y = position
        ratio_x = self.sensor_resolution[0] / image_resolution[0]
        ratio_y = self.sensor_resolution[1] / image_resolution[1]
        x *= ratio_x
        y *= ratio_y
        #We want to coordinates relative to the center of the center
        #for further calculations
        x -= int(self.sensor_resolution[0]/2)
        y -= int(self.sensor_resolution[1]/2)
        #Then the actual position on the sensor, in millimeters from the
        #center.
        x*=self.pixel_size[0]
        y*=self.pixel_size[1]
        return (x,y)

    def sensor_position_to_position_on_facing_plane(self, position, distance):
        x, y = position
        x = (x / self.focal_length) * distance
        y = (y / self.focal_length) * distance
        return (x,y)


def horizontal_pixel_to_angle(x, image_width, object_distance, delta):
    pass
