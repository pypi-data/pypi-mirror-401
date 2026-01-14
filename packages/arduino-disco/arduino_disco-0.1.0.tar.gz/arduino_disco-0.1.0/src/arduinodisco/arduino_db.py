from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Dict, Optional

@dataclass
class BoardDefinition:
    fqbn: str
    name: str
    package: str
    architecture: str
    board_id: str
    vid_pid: List[Tuple[int, int]]

def parse_boards_txt(path: Path,
                     package: str,
                     arch: str) -> List[BoardDefinition]:
    # boards.txt ist ein einfaches key=value Format
    if not path.is_file():
        return []

    # Roh-Struktur: board_id -> dict(key -> value)
    boards_raw: Dict[str, Dict[str, str]] = {}

    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            # Beispiel: uno.name, uno.vid.0, mega.pid.0 etc.
            parts = key.split(".")
            board_id = parts[0]
            subkey = ".".join(parts[1:]) if len(parts) > 1 else ""

            board_dict = boards_raw.setdefault(board_id, {})
            board_dict[subkey] = value

    boards: List[BoardDefinition] = []
    for board_id, data in boards_raw.items():
        name = data.get("name")
        if not name:
            continue

        vid_pid_pairs: List[Tuple[int, int]] = []

        # keys wie "vid.0", "vid.1" / "pid.0", "pid.1"
        # Wir suchen Indizes 0..N
        index = 0
        while True:
            vid_key = f"vid.{index}"
            pid_key = f"pid.{index}"
            if vid_key not in data or pid_key not in data:
                break
            try:
                vid = int(data[vid_key], 0)   # 0x2341 -> int
                pid = int(data[pid_key], 0)
                vid_pid_pairs.append((vid, pid))
            except ValueError:
                pass
            index += 1

        fqbn = f"{package}:{arch}:{board_id}"
        boards.append(BoardDefinition(
            fqbn=fqbn,
            name=name,
            package=package,
            architecture=arch,
            board_id=board_id,
            vid_pid=vid_pid_pairs
        ))

    return boards

def load_all_board_definitions() -> List[BoardDefinition]:
    from .paths import find_hardware_dirs
    all_boards = []
    for hw_dir in find_hardware_dirs():
        boards_txt = hw_dir / "boards.txt"
        if not boards_txt.exists():
            continue
        # <data_dir>/packages/<vendor>/hardware/<arch>/<version>/
        parts = hw_dir.parts
        if len(parts) < 4:
            continue
        
        arch = parts[-2]
        package = parts[-4]

        all_boards.extend(parse_boards_txt(boards_txt, package, arch))
    return all_boards