""" 
    This example demonstrates how to use the ultrasonic sensor to detect obstacles and control the robot's movement accordingly. 
    The robot will move forward until it detects an obstacle within a certain distance, at which point it will stop, back up, and turn to avoid the obstacle. 
    The LEDs provide visual feedback on the robot's status (green for clear path, red for obstacle detected, yellow for backing up).
""" 

from robot_sdk.motion.motors import Motors
from robot_sdk.feedback.leds import LEDs
from robot_sdk.sensors.ultrasonic import Ultrasonic

import time

# Initialize hardware
motors = Motors()
leds = LEDs()
ultra = Ultrasonic()

SAFE_DISTANCE_CM = 25   # stop distance
SPEED = 40
MOTION_IS_ACTIVE = True

try:
    leds.both("green")

    while True:
        distance = ultra.get_distance_cm()
        print(f"Distance: {distance:.1f} cm")

        # No obstacle detected
        if distance > SAFE_DISTANCE_CM:
            leds.both("green")
            if MOTION_IS_ACTIVE:
                motors.forward(SPEED)
        
        # Obstacle detected
        else:
            print("Obstacle detected!")
            leds.both("red")
            if MOTION_IS_ACTIVE:
                motors.stop()
            time.sleep(0.5)

            # Back up
            leds.both("yellow")
            if MOTION_IS_ACTIVE:
                motors.backward(30)
            time.sleep(0.8)

            # Turn to avoid obstacle
            leds.left("red")
            if MOTION_IS_ACTIVE:
                motors.rotate_left(40)
            time.sleep(0.6)

            leds.off()

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nProgram stopped by user")

finally:
    # Always leave robot in safe state
    motors.stop()
    leds.off()
    ultra.close()
    print("Robot stopped, LEDs off, ultrasonic released")
