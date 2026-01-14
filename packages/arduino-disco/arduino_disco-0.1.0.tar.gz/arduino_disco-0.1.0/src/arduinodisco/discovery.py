from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple

from .ports import SerialPortInfo, enumerate_serial_ports
from .arduino_db import BoardDefinition, load_all_board_definitions

@dataclass
class DiscoveryResult:
    port: SerialPortInfo
    board: Optional[BoardDefinition]
    confidence: float
    reason: str


def score_candidate(port: SerialPortInfo, board: BoardDefinition) -> float:
    ##
    ## Implement a "smart" scoring mechanism to improve the accuracy of the discovery process.
    ##
    score = 0.0

    # 1. VID/PID Match
    if port.vid is not None and port.pid is not None:
        if (port.vid, port.pid) in board.vid_pid:
            score += 1.0

    # 2. Productstring contains board name?
    if port.product and board.name.lower() in port.product.lower():
        score += 0.3

    # 3. Manufacturer fit package?
    if port.manufacturer:
        if board.package.lower() in port.manufacturer.lower():
            score += 0.2

    # 4. Architecture?
    if port.product:
        if board.architecture.lower() in port.product.lower():
            score += 0.1

    # 5. CH340/CP2102 Heuristics
    if port.product:
        if "ch340" in port.product.lower() or "cp210" in port.product.lower():
            # Viele Arduino-Klone
            if board.board_id in ("uno", "nano", "mega"):
                score += 0.05
    return score

class BoardDatabase:
    def __init__(self, boards: List[BoardDefinition]):
        self.boards = boards
        self.vid_pid_index: Dict[Tuple[int, int], List[BoardDefinition]] = {}
        for b in boards:
            for vp in b.vid_pid:
                self.vid_pid_index.setdefault(vp, []).append(b)

    @classmethod
    def from_arduino_installation(cls) -> "BoardDatabase":
        return cls(load_all_board_definitions())
    def match_port(self, port: SerialPortInfo) -> DiscoveryResult:
        candidates = []

        for board in self.boards:
            score = score_candidate(port, board)
            if score > 0:
                candidates.append((score, board))

        if not candidates:
            return DiscoveryResult(
                port=port,
                board=None,
                confidence=0.0,
                reason="No matching board found"
            )

        # Bestes Ergebnis auswählen
        candidates.sort(key=lambda x: x[0], reverse=True)
        best_score, best_board = candidates[0]

        reason = "Heuristic match"
        if best_score >= 1.0:
            reason = "VID/PID matched boards.txt"

        return DiscoveryResult(
            port=port,
            board=best_board,
            confidence=min(best_score, 1.0),
            reason=reason
        )

def discover_boards(include_all_ports: bool = False) -> List[DiscoveryResult]:
    db = BoardDatabase.from_arduino_installation()
    serial_ports = enumerate_serial_ports()
    disco_ports = [db.match_port(p) for p in serial_ports]
    disco_ports.sort(key=lambda x: x.board.name if x.board else "")
    if include_all_ports:
        return disco_ports
    return [d for d in disco_ports if d.board is not None]

