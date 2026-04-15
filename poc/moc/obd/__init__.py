import random as _random

def scan_serial() -> list[str]:
    return ['/dev/rftty0']

class Quantity:
    magnitude: float

    def __init__(self, magnitude):
        self.magnitude = magnitude

class OBDResponse:
    def __init__(self, value: Quantity):
        self.value = value

class OBD:
    def __init__(self, port: str) -> None:
        self.port = port

    def is_connected(self) -> bool:
        return True
    
    _DIST = {
        'RPM': (500, 7000),
        'SPEED': (0, 230),
        'THROTTLE': (0, 100),
        'COOLANT_TEMP': (20, 120),
        'OIL_TEMP': (20, 120),
    }

    def _command_value(self, command):
        min, max = OBD._DIST.get(command.name, (.1, 1))
        return _random.uniform(min, max)

    def query(self, command):
        return OBDResponse(Quantity(self._command_value(command)))
