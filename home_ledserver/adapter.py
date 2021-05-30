import logging
from config import GPIO_DATA_PIN, COLOR_ORDER

logger = logging.getLogger(__file__)

try:
    import neopixel
    import board

    pixels = neopixel.Neopixel(getattr(board, GPIO_DATA_PIN), 50, brightness=.5, auto_write=False, pixel_order=getattr(neopixel, COLOR_ORDER))
except (NotImplementedError, ModuleNotFoundError):
    logger.debug("No Neopixel devices found, mocking CircuitPython objects")
    from unittest import mock

    board = mock.MagicMock()
    pixels = mock.MagicMock()