from robot_sdk.motion.motors import Motors
from robot_sdk.feedback.leds import LEDs
from robot_sdk.arm.arm import Arm
from robot_sdk.vision.camera import SimpleCamera
import time

# Initialize the robot's components
motors = Motors()
servos = Arm()
led = LEDs()
cam = SimpleCamera()


# Define the speed of the robot
SPEED = 40


plot_order = {
    "first" : "green",
    "second": "nothing",
    "third" : "orange"
}

# Assuming same starting position of the robot.

def detect_plot_order():
    print("[INFO] Detecting plot order...")

    # Plot detection from here
    iterations = 10
    initial_detected_order = cam.get_plot_order(min_area=500, target_colors=["green", "orange", "gray"])
    
    order = initial_detected_order

    # Repeat the detection until we get a consistent order for a few iterations to ensure reliability
    while iterations > 0:
        order = cam.get_plot_order(min_area=500, target_colors=["green", "orange", "gray"])
        print("[DEBUG] Detected order: {}".format(order))

        if order == initial_detected_order:
            iterations -= 1
        else:
            iterations = 10
            initial_detected_order = order
    
    # Assign the final detected order to the plot_order dictionary
    plot_order["first"] = order[0]
    plot_order["second"] = order[1]
    plot_order["third"] = order[2]

    print("[INFO] Detected order \n- First: {}, Second: {}, Third: {}".format(plot_order["first"], plot_order["second"], plot_order["third"]))

def initialize_robot():
    # Initial setup for the robot, if needed
    print("[INFO] Initializing robot components...")
    # For example, we could reset the arm position here
    led.both("blue")
    servos.home()
    time.sleep(1)
    servos.base(-20)
    servos.shoulder(-40)
    servos.move_camera(100)

    print("[INFO] Robot initialization complete.")


def perform_action(color):
    """Perform an action at the color position, like flashing the LEDs."""
    if color == "white":
        
        print("[INFO] Performing action at gray plot")
        led.both("white")
        time.sleep(2)
        led.both("off")
        pass
    elif color == "gray":
        pass

    elif color == "green":
        print("[INFO] Performing action at green plot")
        led.both("green")
        motors.rotate_left(SPEED)
        time.sleep(2.1)
        motors.stop()
        time.sleep(0.5)
        # Assuming the green seeds are in front
        # Drop seeds at the plot
        arm.base(0)
        time.sleep(0.5)
        initialize_robot_arm()
        # Always return to drive forward
        motors.rotate_right(SPEED)
        time.sleep(1.8)
        motors.stop()

        led.off()

    elif color == "orange":
        print("[INFO] Performing action at orange plot")
        led.both("orange")
        time.sleep(0.5)
        led.off()
    else:
        print("[INFO] Skip this plot")

def get_plot_color():

    possible_colors = ["white", "gray", "orange", "green"]
    for color in possible_colors:
        count = 0
        for i in range(10):
            detected, position, cx, cy, best_area, contour, frame = cam.get_color_position(color_name=color, min_area=500)
        
        
            if detected and position == "center-bottom":
                count += 1

        if count > 3:
            return color    
    return "nothing"



def main():

    initialize_robot()
    time.sleep(1)
    led.off()


    # Step 1: Move to first plot
    print("[INFO] Moving to first plot...")

    # CODE FOR MOVEMENT HERE
    motors.forward(SPEED)
    time.sleep(100)
    
    # Step 1.1: Perform plot detection
    first_plot_color = get_plot_color()
    print(f"[INFO] Color {first_plot_color} detected")
    # Step 1.2: Perform action based on detected color
    perform_action(first_plot_color)

    # Step 2: Move to second plot
    print("[INFO] Moving to second plot...")

    # CODE FOR MOVEMENT HERE

    # Step 2.2: Perform plot detection
    second_plot_color = get_plot_color()
    print(f"[INFO] Color {second_plot_color} detected")
    perform_action(second_plot_color)

    # Step 3: Move to third plot
    print("[INFO] Moving to third plot...")


    # CODE FOR MOVEMENT HERE

    third_plot_color = get_plot_color()
    print(f"[INFO] Color {third_plot_color} detected")
    perform_action(third_plot_color)

    # Step 4: Move out of map
    print("[INFO] Moving out of the map...")

    motors.stop()


if __name__ == "__main__":

    main()

    


    exit()
