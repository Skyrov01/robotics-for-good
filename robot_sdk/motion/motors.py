from .motor_driver import MotorDriver


class Motors:
    """
    Student-friendly tank drive controller.

    Motor mapping:
    - Motor 1 → LEFT tread
    - Motor 2 → RIGHT tread
    """

    FORWARD = 1
    BACKWARD = -1

    def __init__(self):
        self._driver = MotorDriver()

    # --------------------
    # Basic movement
    # --------------------

    def left_forward(self, speed=100):
        """Left motor forward, right stopped."""
        self._driver.motor(1, self.FORWARD, speed)
        self._driver.motor(2, self.FORWARD, 0)

    def right_forward(self, speed=100):
        """Right motor forward, left stopped."""
        self._driver.motor(1, self.FORWARD, 0)
        self._driver.motor(2, self.FORWARD, speed)

    def forward(self, speed=100):
        """Both motors forward."""
        self._driver.motor(1, self.FORWARD, speed)
        self._driver.motor(2, self.FORWARD, speed)

    def backward(self, speed=100):
        """Both motors backward."""
        self._driver.motor(1, self.BACKWARD, speed)
        self._driver.motor(2, self.BACKWARD, speed)

    def rotate_left(self, speed=100):
        """Rotate left in place."""
        self._driver.motor(1, self.BACKWARD, speed)
        self._driver.motor(2, self.FORWARD, speed)

    def rotate_right(self, speed=100):
        """Rotate right in place."""
        self._driver.motor(1, self.FORWARD, speed)
        self._driver.motor(2, self.BACKWARD, speed)

    def stop(self):
        """Stop both motors."""
        self._driver.motor(1, self.FORWARD, 0)
        self._driver.motor(2, self.FORWARD, 0)

    def shutdown(self):
        """Clean shutdown."""
        self._driver.destroy()
