import logging
import config

logger = logging.getLogger(__file__)
settings = config.get()

try:
    import neopixel
    import board

    pixels = neopixel.Neopixel(getattr(board, settings.pixel_pin), 50, brightness=.5, auto_write=False, pixel_order=getattr(neopixel, settings.color_order))
except (NotImplementedError, ModuleNotFoundError):
    logger.debug("No Neopixel devices found, mocking CircuitPython objects")
    from unittest import mock

    board = mock.MagicMock()
    pixels = mock.MagicMock()