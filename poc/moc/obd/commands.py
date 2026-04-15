import dataclasses as _dataclasses

@_dataclasses.dataclass
class OBDCommand:
    name: str

def __getattr__(key: str):
    return OBDCommand(key)
