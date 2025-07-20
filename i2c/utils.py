# noinspection PyPackageRequirements
import board
import busio
from adafruit_extended_bus import ExtendedI2C


def get_i2c_bus(bus_number: int | None = None) -> busio.I2C:
    return board.I2C() if bus_number is None else ExtendedI2C(bus_number)
