import logging

logger = logging.getLogger(__file__)

try:
    import neopixel
    import board

    pixels = neopixel.Neopixel(getattr(board, "D4"), 50, brightness=.5, auto_write=False)
except (NotImplementedError, ModuleNotFoundError):
    logger.debug("No Neopixel devices found, mocking CircuitPython objects")
    from unittest import mock

    board = mock.MagicMock()
    pixels = mock.MagicMock()