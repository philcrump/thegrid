"""
Colour ripple pattern

Colours will rippple from the centre of The Grid, with the colour changing
gradually through the spectrum.  Pretty!  Hopefully.
"""

import numpy as np
import logging
from ..pattern import Pattern, register_pattern
logger = logging.getLogger(__name__)


@register_pattern("ColourRipple")
class ColourRipple(Pattern):
    """
    This class will have self.config set from the register_pattern argument,
    and self.ui set as a reference to the global UI helper.
    If you override __init__(), please call super().__init__().
    """

    @staticmethod
    def linear_colour_gradient(start_rgb=(0, 0, 0),
                               end_rgb=(255, 255, 255), n=50):
        for i in range(1, n):
            colour = [start_rgb[channel] +
                      i/(n-1) * (end_rgb[channel] - start_rgb[channel])
                      for channel in range(3)]
            yield tuple(colour)

    def update(self):
        """
        The update() method is called by the main control loop on a time basis
        you can specify. You should compute the new grid state in this method.

        The grid shape is specified by a (7, 7, 6) numpy array of type uint8,
        with the first two dimensions specifying the (x, y) pole coordinate,
        and the third dimension giving (red, green, blue, sound type, sound
        frequency, sound volume).

        Sound types:
            0: silent
            1: sine
            2: square
            3: triangle
            4: noise
            5: click

        Sound frequencies and volumes range 0-255 and are scaled in hardware to
        meet the available sounder response.

        The time until next update is specified in seconds.

        Return a tuple of (new_grid, update_time).
        """
        colour_gradient = self.linear_colour_gradient()
        grid = np.zeros((7, 7, 6), dtype=np.uint8)

        while True:
            logger.info("Updating pattern")
            grid[3][3] = next(colour_gradient) + (0, 0, 0)

            grid[:, 2] = next(colour_gradient) + (0, 0, 0)
            grid[:, 4] = next(colour_gradient) + (0, 0, 0)
            grid[2, :] = next(colour_gradient) + (0, 0, 0)
            grid[4, :] = next(colour_gradient) + (0, 0, 0)

            grid[:, 1] = next(colour_gradient) + (0, 0, 0)
            grid[:, 5] = next(colour_gradient) + (0, 0, 0)
            grid[1, :] = next(colour_gradient) + (0, 0, 0)
            grid[5, :] = next(colour_gradient) + (0, 0, 0)

            grid[:, 0] = next(colour_gradient) + (0, 0, 0)
            grid[:, 6] = next(colour_gradient) + (0, 0, 0)
            grid[0, :] = next(colour_gradient) + (0, 0, 0)
            grid[6, :] = next(colour_gradient) + (0, 0, 0)

            yield grid, 10
