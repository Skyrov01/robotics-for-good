import cv2
import numpy as np
from .base_camera import BaseCamera
from picamera2 import Picamera2
import libcamera


class SimpleCamera(BaseCamera):
    """
    SimpleCamera using Picamera2 + OpenCV
    """

    COLOR_PRESETS = {
        "red":     ([0, 140, 80],    [8, 255, 255]),
        "red2":    ([172, 140, 80],  [180, 255, 255]),
        "green":   ([45, 100, 80],   [75, 255, 255]),
        "blue":    ([95, 100, 80],   [125, 255, 255]),
        "yellow":  ([22, 140, 120],  [32, 255, 255]),
        "orange":  ([12, 150, 120],  [18, 255, 255]),
        "purple":  ([135, 100, 80],  [155, 255, 255]),
        "pink":    ([162, 100, 120], [168, 255, 255]),
        "cyan":    ([85, 100, 80],   [95, 255, 255]),
        "magenta": ([145, 100, 80],  [160, 255, 255]),
        "black":   ([0, 0, 0],       [180, 180, 25]),
        "white":   ([0, 0, 215],     [180, 20, 255]),
        "gray":    ([0, 0, 100],     [180, 20, 200]),
    }

    def __init__(self, color="yellow"):
        super().__init__()
        self.set_color(color)

    # -------------------------------------------------
    # Camera capture (Picamera2)
    # -------------------------------------------------

    @staticmethod
    def frames():
        picam2 = Picamera2()

        config = picam2.create_preview_configuration(
            main={"size": (640, 480), "format": "RGB888"},
            transform=libcamera.Transform(hflip=False, vflip=False)
        )

        picam2.configure(config)
        picam2.start()

        try:
            while True:
                frame = picam2.capture_array()
                yield frame
        finally:
            picam2.stop()

    # -------------------------------------------------
    # Color handling
    # -------------------------------------------------

    def set_color(self, color_name):
        if color_name not in self.COLOR_PRESETS:
            raise ValueError(
                f"Unknown color '{color_name}'. "
                f"Available: {list(self.COLOR_PRESETS.keys())}"
            )

        lower, upper = self.COLOR_PRESETS[color_name]
        self.color_name = color_name
        self.color_lower = np.array(lower)
        self.color_upper = np.array(upper)

    def set_color_range(self, lower, upper):
        if lower[0] > 180 or upper[0] > 180:
            raise ValueError("HSV Hue must be between 0 and 180")

        self.color_lower = np.array(lower, dtype=np.uint8)
        self.color_upper = np.array(upper, dtype=np.uint8)
        self.color_name = "custom"

    def add_color_preset(self, name, lower, upper):
        """
        Add a new HSV color preset.

        Parameters:
            name  : str
            lower : [H, S, V]
            upper : [H, S, V]
        """

        if len(lower) != 3 or len(upper) != 3:
            raise ValueError("Color bounds must be [H, S, V]")

        self.COLOR_PRESETS[name] = (lower, upper)

    # -------------------------------------------------
    # Vision logic
    # -------------------------------------------------

    def detect_bigest_color(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        mask = cv2.inRange(hsv, self.color_lower, self.color_upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours, _ = cv2.findContours(
            mask.copy(),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if len(contours) == 0:
            return False, None, None, None, None

        c = max(contours, key=cv2.contourArea)

        ((x, y), radius) = cv2.minEnclosingCircle(c)

        if radius < 10:
            return False, None, None, None, None

        M = cv2.moments(c)
        if M["m00"] == 0:
            return False, None, None, None, None

        center = (
            int(M["m10"] / M["m00"]),
            int(M["m01"] / M["m00"])
        )

        h, w, _ = frame.shape
        error_x = (w // 2) - center[0]
        error_y = (h // 2) - center[1]

        return True, center, radius, error_x, error_y


    # -------------------------------------------------
    # Visualization (optional)
    # -------------------------------------------------

    def get_frame_with_detection(self, delay=50):

        frame = self.get_frame()
        if frame is None:
            return True  # camera not ready yet

        frame = frame.copy()

        found, center, radius, error_x, error_y = self.detect_bigest_color(frame)

        if found:
            cv2.circle(frame, center, int(radius), (255, 255, 255), 2)
            cv2.circle(frame, center, 4, (255, 0, 0), -1)
            text = f"{self.color_name} detected  ex:{error_x} ey:{error_y}"
        else:
            text = f"Searching for {self.color_name}"

        cv2.putText(
            frame,
            text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

        cv2.imshow("Camera View", frame)

        if cv2.waitKey(delay) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            return False

        return True
    # -------------------------------------------------
    # Target direction logic
    # ------------------------------------------------- 

    def get_target_direction(self, width=640):
        found, center, _ = self.detect_bigest_color(self.get_frame())
        if not found:
            return None
        if center[0] < width / 3:
            return "left"
        elif center[0] > width * 2 / 3:
            return "right"
        return "center"

    def calibrate_color(self, roi_size=80, samples=30):
        """
        Calibrate HSV range by sampling a central ROI.
        Press 'c' to capture samples.
        Press 'q' to quit.
        """
        hsv_samples = []

        while True:
            frame = self.get_frame()
            if frame is None:
                continue

            h, w, _ = frame.shape
            cx, cy = w // 2, h // 2
            half = roi_size // 2

            roi = frame[
                cy - half : cy + half,
                cx - half : cx + half
            ]

            hsv = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV)

            display = frame.copy()
            cv2.rectangle(
                display,
                (cx - half, cy - half),
                (cx + half, cy + half),
                (0, 255, 0),
                2
            )

            cv2.imshow("Calibration", display)
            key = cv2.waitKey(20) & 0xFF

            if key == ord("c"):
                hsv_samples.append(hsv.reshape(-1, 3))
                print(f"Captured sample {len(hsv_samples)}")


                if len(hsv_samples) >= samples:
                    break

            if key == ord("q"):
                cv2.destroyAllWindows()
                # return None

        cv2.destroyAllWindows()

        all_pixels = np.vstack(hsv_samples)

        h_min, s_min, v_min = np.min(all_pixels, axis=0)
        h_max, s_max, v_max = np.max(all_pixels, axis=0)

        margin = np.array([5, 20, 20])

        lower = np.clip([h_min, s_min, v_min] - margin, 0, 255)
        upper = np.clip([h_max, s_max, v_max] + margin, 0, 255)

        print(f"Calibrated HSV range: lower={lower}, upper={upper}")
        
        self.color_lower = np.array(lower)[::-1]
        self.color_upper = np.array(upper)[::-1]

        return (lower.astype(int).tolist(), upper.astype(int).tolist())

    def save_calibrated_color(self, name, roi_size=80, samples=1):
        result = self.calibrate_color(roi_size=roi_size, samples=samples)
        if result is None:
            return False

        lower, upper = result
        self.add_color_preset(name, lower, upper)
        return True

    def show_debug(self, color_name="red", delay=1):
        self.set_color(color_name) 
        frame = self.get_frame()
        found, center, radius = self.detect_bigest_color(frame)

        if found:
            print(f"{color_name} detected at {center} with radius {radius}")
            cv2.circle(frame, center, radius, (255, 255, 255), 2)
            cv2.circle(frame, center, 4, (255, 0, 0), -1)
        else:
            print(f"No {color_name} detected")

        cv2.imshow("Camera Debug", frame)

        if cv2.waitKey(delay) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            return False

        return True


