#!/usr/bin/env python3
from gpiozero import DistanceSensor
from time import sleep


class Ultrasonic:
    def __init__(self, trig_pin=23, echo_pin=24, max_distance=2.0):
        """
        Initialize ultrasonic sensor.

        :param trig_pin: GPIO pin for TRIG (BCM)
        :param echo_pin: GPIO pin for ECHO (BCM)
        :param max_distance: Maximum distance in meters
        """
        self.sensor = DistanceSensor(
            trigger=trig_pin,
            echo=echo_pin,
            max_distance=max_distance
        )

    def get_distance_cm(self):
        """
        Read distance in centimeters.
        :return: distance (float) in cm
        """
        return self.sensor.distance * 100

    def get_distance_m(self):
        """
        Read distance in meters.
        :return: distance (float) in meters
        """
        return self.sensor.distance

    def close(self):
        """
        Cleanly release GPIO resources.
        """
        self.sensor.close()


