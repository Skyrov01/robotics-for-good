# robot_sdk/feedback/leds.py

from .ws2812_driver import Adeept_SPI_LedPixel
import time

# -----------------------
# LED layout definition
# -----------------------

IGNORED = [0, 1]
LEFT_LEDS  = list(range(2, 8))    # 2–7
RIGHT_LEDS = list(range(8, 14))   # 8–13
ALL_LEDS   = LEFT_LEDS + RIGHT_LEDS

COLOR_MAP = {
    "red":    (255, 0, 0),
    "green":  (0, 255, 0),
    "blue":   (0, 0, 255),
    "yellow": (255, 125, 0),
    "cyan":   (0, 255, 255),
    "purple": (128, 0, 128),
    "white":  (255, 255, 255),
    "off":    (0, 0, 0),
}


class LEDs:
    """
    High-level LED interface.
    """

    def __init__(self, count=14, brightness=255):
        self._driver = Adeept_SPI_LedPixel(
            count=count,
            bright=brightness,
            sequence="GRB",
            bus=0,
            device=0
        )

        if not self._driver.is_alive():
            self._driver.daemon = True
            self._driver.start()

        self.off()

    # -----------------------
    # Core helpers
    # -----------------------

    def _color(self, color):
        if isinstance(color, str):
            color = color.lower()
            if color not in COLOR_MAP:
                raise ValueError(f"Unknown color '{color}'")
            return COLOR_MAP[color]
        return color

    def _set_indices(self, indices, color):
        r, g, b = self._color(color)
        self._driver.lightMode = "none"
        for i in indices:
            self._driver.set_led_color_data(i, r, g, b)
        self._driver.show()

    # -----------------------
    # High-level API
    # -----------------------

    def left(self, color):
        """Set LEFT side LEDs."""
        self._set_indices(LEFT_LEDS, color)

    def right(self, color):
        """Set RIGHT side LEDs."""
        self._set_indices(RIGHT_LEDS, color)

    def both(self, color):
        """Set BOTH sides."""
        self._set_indices(ALL_LEDS, color)

    def off(self):
        """Turn all LEDs off (except ignored)."""
        self._driver.lightMode = "none"
        for i in ALL_LEDS:
            self._driver.set_led_color_data(i, 0, 0, 0)
        self._driver.show()

    # -----------------------
    # Effects (side-aware)
    # -----------------------

    def left_breath(self, color):
        self._driver.lightMode = "none"
        r, g, b = self._color(color)
        self._driver.colorBreathR = r
        self._driver.colorBreathG = g
        self._driver.colorBreathB = b
        self._driver.lightMode = "breath"
        # NOTE: breath applies to all LEDs → we pre-clear others
        self._clear_except(LEFT_LEDS)

    def right_breath(self, color):
        self._driver.lightMode = "none"
        r, g, b = self._color(color)
        self._driver.colorBreathR = r
        self._driver.colorBreathG = g
        self._driver.colorBreathB = b
        self._driver.lightMode = "breath"
        self._clear_except(RIGHT_LEDS)

    def police(self):
        """Police effect on both sides."""
        self._driver.police()

    # -----------------------
    # Robot semantics
    # -----------------------

    def turn_signal(self, side, color="yellow", delay=0.3, cycles=5):
        """Blink left or right side like a turn signal."""
        indices = LEFT_LEDS if side == "left" else RIGHT_LEDS
        for _ in range(cycles):
            self._set_indices(indices, color)
            time.sleep(delay)
            self._set_indices(indices, "off")
            time.sleep(delay)

    # -----------------------
    # Internal
    # -----------------------

    def _clear_except(self, keep_indices):
        for i in ALL_LEDS:
            if i not in keep_indices:
                self._driver.set_led_color_data(i, 0, 0, 0)
        self._driver.show()
