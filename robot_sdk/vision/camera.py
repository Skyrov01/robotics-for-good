import cv2
import numpy as np
import time

if __name__ == "__main__":  
    from base_camera import BaseCamera
else:
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
        "green":   ([40, 70, 50],   [85, 255, 255]),
        "blue":    ([95, 100, 80],   [125, 255, 255]),
        "yellow":  ([22, 140, 120],  [32, 255, 255]),
        "orange":  ([12, 100, 80],  [25, 255, 255]),
        "purple":  ([135, 100, 80],  [155, 255, 255]),
        "pink":    ([162, 100, 120], [168, 255, 255]),
        "cyan":    ([85, 100, 80],   [95, 255, 255]),
        "magenta": ([145, 100, 80],  [160, 255, 255]),
        "black":   ([0, 0, 0],       [180, 180, 25]),
        "white":   ([0, 0, 215],     [180, 10, 255]),
        "gray": ([0, 0, 180], [255, 40, 230])
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


    # Detect the position of a color and return its position
    def get_color_position(self, color_name, min_area=500):

        if color_name not in self.COLOR_PRESETS:
            raise ValueError(f"Unknown color: {color_name}")

        frame = self.get_frame()
        if frame is None:
            return False, None, None, None, 0, None, None

        # Initialize detection variables
        best_contour = None
        best_area = 0
        detected = False
        position = None
        cx, cy = None, None
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        height, width, _ = frame.shape
        left_limit = int(0.40 * width)
        right_limit = int(0.60 * width)

        # Get the HSV color range for the specified color
        lower, upper = self.COLOR_PRESETS[color_name]
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)

        # Create a mask for the specified color
        color_mask = cv2.inRange(hsv, lower, upper)
        color_mask = cv2.erode(color_mask, None, iterations=2)
        color_mask = cv2.dilate(color_mask, None, iterations=2)

        # Find contours in the mask
        _, gray_mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        
        valid_mask = cv2.bitwise_and(color_mask, gray_mask)

        contours, _ = cv2.findContours(valid_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour that meets the minimum area requirement
        for c in contours:
            area = cv2.contourArea(c)
            if area >= min_area and area > best_area:
                best_area = area
                best_contour = c

        if best_contour is not None:
            M = cv2.moments(best_contour)
            # Calculate the center of the contour if it exists
            if M["m00"] != 0:
                
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # Determine position based on horizontal location
                if cx < left_limit:
                    position = "left"
                elif cx > right_limit:
                    position = "right"
                else:
                    position = "center"

                detected = True

        return detected, position, cx, cy, best_area, best_contour, frame

    # -------------------------------------------------
    # Debugging
    # -------------------------------------------------

    def draw_debug_lines(self, frame):
        frame = frame.copy()
        height, width, _ = frame.shape

        # Band limits
        left_limit = int(0.40 * width)
        right_limit = int(0.60 * width)

        # Draw band separators
        cv2.line(frame, (left_limit, 0), (left_limit, height), (255, 255, 255), 2)
        cv2.line(frame, (right_limit, 0), (right_limit, height), (255, 255, 255), 2)

        # Band labels
        cv2.putText(frame, "LEFT", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, "CENTER", (left_limit + 20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, "RIGHT", (right_limit + 20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        return frame


    def debug(self, frame, color_name, position, cx, cy, area, contour, delay=30):

        frame = self.draw_debug_lines(frame)

        if contour is not None and area > 0:
            ((x, y), radius) = cv2.minEnclosingCircle(contour)
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)

            label = f"{color_name} | {position}"
            cv2.putText(frame, label, (cx - 60, cy - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow("Color Object Debug", frame)

        if cv2.waitKey(delay) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            return False

        return True
    # -------------------------------------------------
    # Detect the order of colors based on a list of target colors
    # Returns a list of detected colors ordered from left to right
    # The order is based on the horizontal position of the detected colors in the camera frame
    # Colors that are not detected will be placed at the end of the list
    def get_plot_order(self, min_area=500, target_colors=["green", "orange", "gray"]):
        plots = []

        for color in target_colors:
            result = self.get_color_position(color, min_area)
            if result is None:
                continue

            detected, position, cx, cy, area, contour, frame = result
            if detected:
                plots.append((color, cx))
            else:
                plots.append((color, float('inf')))  # Not detected, put at the end

        # Sort by x position
        plots.sort(key=lambda p: p[1])

        return [color for color, _ in plots]

    # Same but with debug visualization
    def debug_plot_order(self, min_area=500, delay=30):
        frame = self.get_frame()
        if frame is None:
            return True

        frame = frame.copy()
        height, width, _ = frame.shape

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        detected = []

        # Only the plots we care about
        for color_name in ["orange", "green", "gray"]:
            if color_name not in self.COLOR_PRESETS:
                continue

            lower, upper = self.COLOR_PRESETS[color_name]
            lower = np.array(lower, dtype=np.uint8)
            upper = np.array(upper, dtype=np.uint8)

            # Create a mask for the specified color
            color_mask = cv2.inRange(hsv, lower, upper)
            color_mask = cv2.erode(color_mask, None, iterations=2)
            color_mask = cv2.dilate(color_mask, None, iterations=2)
            
            
            # Find contours in the mask
            _, gray_mask = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY_INV)
            

            valid_mask = color_mask # cv2.bitwise_and(color_mask, gray_mask)

            if color_name == "gray":
                # Resize masks to the same dimensions (if needed)
                height, width = gray_mask.shape
                scale_percent = 75
                new_width = int(width * scale_percent / 100)
                new_height = int(height * scale_percent / 100)
                
                color_mask_resized = cv2.resize(color_mask, (new_width, new_height))
                gray_mask_resized = cv2.resize(gray_mask, (new_width, new_height))
                valid_mask_resized = cv2.resize(valid_mask, (new_width, new_height))

                # Convert single-channel masks to 3-channel (BGR) for concatenation
                color_mask_bgr = cv2.cvtColor(color_mask_resized, cv2.COLOR_GRAY2BGR)
                gray_mask_bgr = cv2.cvtColor(gray_mask_resized, cv2.COLOR_GRAY2BGR)
                valid_mask_bgr = cv2.cvtColor(valid_mask_resized, cv2.COLOR_GRAY2BGR)

                # Add labels to each mask
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(color_mask_bgr, f"Color Mask ({color_name})", (10, 20), font, 0.5, (125, 0, 255), 1, cv2.LINE_AA)
                cv2.putText(gray_mask_bgr, "Gray Mask", (10, 20), font, 0.5, (125, 0, 255), 1, cv2.LINE_AA)
                cv2.putText(valid_mask_bgr, "Valid Mask", (10, 20), font, 0.5, (125, 0, 255), 1, cv2.LINE_AA)

                # Concatenate masks horizontally
                combined = cv2.hconcat([color_mask_bgr, gray_mask_bgr, valid_mask_bgr])
                # Show the combined image
                cv2.imshow(f"All Masks (Color | {color_name} | Valid)", combined)

            contours, _ = cv2.findContours(valid_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            best_contour = None
            best_area = 0

            for c in contours:
                area = cv2.contourArea(c)
                if area >= min_area and area > best_area:
                    best_area = area
                    best_contour = c

            if best_contour is None:
                continue

            M = cv2.moments(best_contour)
            if M["m00"] == 0:
                continue

            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            detected.append({
                "color": color_name,
                "cx": cx,
                "cy": cy,
                "area": best_area,
                "contour": best_contour
            })

        # Sort by diagonal distance from top-left (0, 0)
        # Objects closer to the top-left come first
        detected.sort(key=lambda d: (-d["cy"], d["cx"]))  # Sum of x and y coordinates

        # Draw detections
        for idx, obj in enumerate(detected, start=1):
            cx, cy = obj["cx"], obj["cy"]
            color = obj["color"]

            ((x, y), radius) = cv2.minEnclosingCircle(obj["contour"])
            # cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)

            label = f"{color} ({idx})"
            cv2.putText(
                frame,
                label,
                (cx - 40, cy - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

            # Draw vertical and horizontal lines from the center
            cv2.line(frame, (cx, 0), (cx, height), (255, 255, 255), 1)
            cv2.line(frame, (0, cy), (width, cy), (255, 255, 255), 1)

        # Draw order summary
        if detected:
            order_text = " - ".join([d["color"] for d in detected])
            cv2.putText(
                frame,
                f"Order: {order_text}",
                (20, height - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

        cv2.imshow("Plot Order Debug", frame)

        if cv2.waitKey(delay) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            return False

        return True


if __name__ == "__main__":

    cam = SimpleCamera("yellow")


    while True:
        # detected, position, cx, cy, best_area, contour, frame = cam.get_color_position(color_name="green", min_area=500)
        # cam.debug(frame, "green", position, cx, cy, best_area, contour)
        # print(cam.get_plot_order(min_area=500, target_colors=["green", "orange", "gray"]))
        cam.debug_plot_order()
        time.sleep(0.05)
