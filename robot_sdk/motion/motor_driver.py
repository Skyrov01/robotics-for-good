#!/usr/bin/env python3

from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import motor


class MotorDriver:
    """
    Class-based version of Adeept motor driver.
    SAME logic, SAME behavior, no abstraction yet.
    """

    # Motor channel definitions (unchanged)
    MOTOR_M1_IN1 = 15
    MOTOR_M1_IN2 = 14
    MOTOR_M2_IN1 = 12
    MOTOR_M2_IN2 = 13
    MOTOR_M3_IN1 = 11
    MOTOR_M3_IN2 = 10
    MOTOR_M4_IN1 = 8
    MOTOR_M4_IN2 = 9

    _polarity = {
        1:  1,   # motor 1 normal
        2:  1,   # motor 2 normal
        3: -1,   # motor 3 inverted
        4: -1,   # motor 4 inverted
    }


    def __init__(self):
        # I2C + PCA9685 setup
        i2c = busio.I2C(SCL, SDA)
        self.pwm_motor = PCA9685(i2c, address=0x5F)
        self.pwm_motor.frequency = 50

        # Motor objects (exact mapping)
        self.motor1 = motor.DCMotor(
            self.pwm_motor.channels[self.MOTOR_M1_IN1],
            self.pwm_motor.channels[self.MOTOR_M1_IN2]
        )
        self.motor1.decay_mode = motor.SLOW_DECAY

        self.motor2 = motor.DCMotor(
            self.pwm_motor.channels[self.MOTOR_M2_IN1],
            self.pwm_motor.channels[self.MOTOR_M2_IN2]
        )
        self.motor2.decay_mode = motor.SLOW_DECAY

        self.motor3 = motor.DCMotor(
            self.pwm_motor.channels[self.MOTOR_M3_IN1],
            self.pwm_motor.channels[self.MOTOR_M3_IN2]
        )
        self.motor3.decay_mode = motor.SLOW_DECAY

        self.motor4 = motor.DCMotor(
            self.pwm_motor.channels[self.MOTOR_M4_IN1],
            self.pwm_motor.channels[self.MOTOR_M4_IN2]
        )
        self.motor4.decay_mode = motor.SLOW_DECAY

    # -----------------------------
    # Internal helper (unchanged)
    # -----------------------------

    def _map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) / (in_max - in_min) * (out_max - out_min) + out_min

    # -----------------------------
    # Public API (same behavior)
    # -----------------------------

    def motor(self, channel, direction, motor_speed):
        if motor_speed > 100:
            motor_speed = 100
        elif motor_speed < 0:
            motor_speed = 0

        speed = self._map(motor_speed, 0, 100, 0, 1.0)

        # Apply direction AND per-motor polarity
        throttle = speed * direction * self._polarity[channel]

        if channel == 1:
            self.motor1.throttle = throttle
        elif channel == 2:
            self.motor2.throttle = throttle
        elif channel == 3:
            self.motor3.throttle = throttle
        elif channel == 4:
            self.motor4.throttle = throttle

    def stop(self):
        """Stop all motors (same as motorStop)."""
        self.motor1.throttle = 0
        self.motor2.throttle = 0
        self.motor3.throttle = 0
        self.motor4.throttle = 0

    def destroy(self):
        """Clean shutdown (same as destroy)."""
        self.stop()
        self.pwm_motor.deinit()


