from .servo_driver import ServoCtrl
import time


class Arm:
    
    # Logical joint mapping (adjust once)
    BASE = 7
    SHOULDER = 1
    ELBOW = 2
    GRIPPER = 3
    CAMERA = 4

    def __init__(self):
        self.ctrl = ServoCtrl()
        self.ctrl.moveInit()
        self.ctrl.start()

    # --------------------
    # Joint control
    # --------------------

    def base(self, angle):
        print("Moving base to angle:", angle)
        self.ctrl.moveAngle(self.BASE, angle)

    def shoulder(self, angle):
        print("Moving shoulder to angle:", angle)
        self.ctrl.moveAngle(self.SHOULDER, angle)

    def elbow(self, angle):
        print("Moving elbow to angle:", angle)
        self.ctrl.moveAngle(self.ELBOW, angle)

    def hand(self, angle):
        print("Moving gripper to angle:", angle)
        self.ctrl.moveAngle(self.GRIPPER, angle)

    # --------------------
    # Gripper
    # --------------------

    def open_hand(self):
        print("Opening gripper")
        self.ctrl.moveAngle(self.GRIPPER, -50)

    def close_hand(self):
        print("Closing gripper")
        self.ctrl.moveAngle(self.GRIPPER, 50)

    # --------------------
    # Poses
    # --------------------

    def home(self):
        print("Moving to home position")
        self.base(0)
        self.shoulder(0)
        self.elbow(0)
        self.open_hand()

    def shutdown(self):
        print("Shutting down arm")
        self.ctrl.stop()
        self.ctrl.join()


    def move_camera(self, angle):
        print("Moving camera")
        self.ctrl.moveAngle(self.CAMERA, angle)
