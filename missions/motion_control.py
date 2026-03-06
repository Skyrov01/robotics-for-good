import time
from robot_sdk.sensors.accelerometer import Accelerometer
from robot_sdk.motion.motors import Motors

class MotionController:

    def __init__(self, motors, accelerometer):
        self.motors = motors
        self.acc = accelerometer

    def move_forward_distance(self, distance_m=0.1, speed=80):
        """
        Move robot forward a given distance (meters).
        Example: 0.1 = 10 cm
        """

        velocity = 0
        position = 0

        dt = 0.05
        alpha = 0.2
        filtered_acc = 0

        print("Moving forward", distance_m, "meters")

        self.motors.forward(speed)

        last_time = time.time()

        while position < distance_m:

            axes = self.acc.get_acceleration()

            # Z axis = forward/back (based on your sensor orientation)
            acc = axes['z']

            # smoothing
            filtered_acc = alpha * acc + (1 - alpha) * filtered_acc

            now = time.time()
            dt = now - last_time
            last_time = now

            velocity += filtered_acc * dt
            position += velocity * dt

            print("distance:", round(position, 3))

            time.sleep(0.02)

        self.motors.stop()

        print("Target reached:", round(position, 3))
    
    def move_backward_distance(self, distance_m=0.1, speed=80):
        """
        Move robot backward a given distance (meters).
        Example: 0.1 = 10 cm
        """

        velocity = 0
        position = 0

        dt = 0.05
        alpha = 0.2
        filtered_acc = 0

        print("Moving backward", distance_m, "meters")

        self.motors.backward(speed)

        last_time = time.time()

        while position < distance_m:

            axes = self.acc.get_acceleration()

            # Z axis = forward/back (based on your sensor orientation)
            acc = -axes['z']  # invert for backward

            # smoothing
            filtered_acc = alpha * acc + (1 - alpha) * filtered_acc

            now = time.time()
            dt = now - last_time
            last_time = now

            velocity += filtered_acc * dt
            position += velocity * dt

            print("distance:", round(position, 3))

            time.sleep(0.02)

        self.motors.stop()

        print("Target reached:", round(position, 3))


if __name__ == "__main__":
    motors = Motors()
    sensor = Accelerometer()

    controller = MotionController(motors, sensor)

    controller.move_forward_distance(0.30)  

    # controller.move_backward_distance(0.20)  