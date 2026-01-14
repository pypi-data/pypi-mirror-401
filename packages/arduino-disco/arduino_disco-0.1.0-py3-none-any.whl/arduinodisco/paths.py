import os
from pathlib import Path
from typing import List

def default_arduino_data_dirs() -> List[Path]:
    dirs = []

    home = Path.home()

    # Linux / macOS
    dirs.append(home / ".arduino15")

    # Windows (Arduino 1.x / 2.x)
    local_appdata = os.environ.get("LOCALAPPDATA")
    if local_appdata:
        dirs.append(Path(local_appdata) / "Arduino15")

    # Optionale Override-Umgebungsvariable
    env_dir = os.environ.get("ARDUINO_DATA_DIR")
    if env_dir:
        dirs.insert(0, Path(env_dir))

    return [d for d in dirs if d.exists()]

def find_hardware_dirs() -> List[Path]:
    hw_dirs = []
    for data_dir in default_arduino_data_dirs():
        # Standard: <data_dir>/packages/<vendor>/hardware/<arch>/<version>/
        packages_dir = data_dir / "packages"
        if not packages_dir.is_dir():
            continue
        for vendor_dir in packages_dir.iterdir():
            hw_base = vendor_dir / "hardware"
            if not hw_base.is_dir():
                continue
            for arch_dir in hw_base.iterdir():
                if not arch_dir.is_dir():
                    continue
                for version_dir in arch_dir.iterdir():
                    if version_dir.is_dir():
                        hw_dirs.append(version_dir)
    return hw_dirs
