from dataclasses import dataclass
from typing import Optional, List
from serial.tools import list_ports

@dataclass
class SerialPortInfo:
    device: str
    description: str
    hwid: str
    vid: Optional[int]
    pid: Optional[int]
    manufacturer: Optional[str]
    product: Optional[str]
    serial_number: Optional[str]

def enumerate_serial_ports() -> List[SerialPortInfo]:
    result = []
    for p in list_ports.comports():
        info = SerialPortInfo(
            device=p.device,
            description=p.description or "",
            hwid=p.hwid or "",
            vid=p.vid,
            pid=p.pid,
            manufacturer=getattr(p, "manufacturer", None),
            product=getattr(p, "product", None),
            serial_number=getattr(p, "serial_number", None),
        )
        result.append(info)
    return result
