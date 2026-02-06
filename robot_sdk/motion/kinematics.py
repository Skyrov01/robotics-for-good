import math
import time

class DifferentialDrive:

    def __init__(self, motor_driver, track_width=0.18):
        """
        track_width: distance between treads (meters)
        """
        self.motors = motor_driver
        self.L = track_width

        # Pose (for simulation / estimation)
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.last_time = time.time()

    # -----------------------------
    # LOW LEVEL (still intuitive)
    # -----------------------------

    def set_wheel_speeds(self, left_speed, right_speed):
        """
        left_speed, right_speed in range [-100, 100]
        """
        # Left motor = channel 1
        self.motors.motor(1, 1 if left_speed >= 0 else -1, abs(left_speed))

        # Right motor = channel 2
        self.motors.motor(2, 1 if right_speed >= 0 else -1, abs(right_speed))

        self._update_odometry(left_speed, right_speed)

    def stop(self):
        self.motors.stop()

    # -----------------------------
    # STUDENT-FRIENDLY MOTIONS
    # -----------------------------

    def forward(self, speed=50):
        self.set_wheel_speeds(speed, speed)

    def backward(self, speed=50):
        self.set_wheel_speeds(-speed, -speed)

    def turn_left(self, speed=50):
        self.set_wheel_speeds(-speed, speed)

    def turn_right(self, speed=50):
        self.set_wheel_speeds(speed, -speed)

    def curve(self, left_speed, right_speed):
        self.set_wheel_speeds(left_speed, right_speed)

    # -----------------------------
    # KINEMATIC MODEL (CORE IDEA)
    # -----------------------------

    def _update_odometry(self, left_speed, right_speed):
        """
        Update (x, y, theta) using differential drive kinematics
        This works both for simulation AND real robot estimation
        """
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        # Normalize speeds to m/s (simple linear model)
        v_l = left_speed / 100.0
        v_r = right_speed / 100.0

        v = (v_l + v_r) / 2.0
        omega = (v_r - v_l) / self.L

        self.theta += omega * dt
        self.x += v * math.cos(self.theta) * dt
        self.y += v * math.sin(self.theta) * dt

    # -----------------------------
    # TELEMETRY (for plots)
    # -----------------------------

    def pose(self):
        return self.x, self.y, self.theta
