import argparse
from arduinodisco import discover_boards

def main():
    parser = argparse.ArgumentParser(description="Discover Arduino boards connected via serial ports.")
    parser.add_argument(
        "-a", "--all", 
        action="store_true", 
        dest="include_all_ports",
        help="Include all serial ports, even those not identified as Arduino boards"
    )
    
    args = parser.parse_args()

    print(f"{'Port':<12} {'Board':<30} {'FQBN':<30} {'Core':<10}")
    
    boards = discover_boards(include_all_ports=args.include_all_ports)
    
    for entry in boards:
        port = entry.port.device
        name = entry.board.name if entry.board else "Unknown"
        fqbn = entry.board.fqbn if entry.board else "-"
        architecture = entry.board.architecture if entry.board else "-"
        print(f"{port:<12} {name:<30} {fqbn:<30} {architecture:<10}")

if __name__ == "__main__":
    main()
