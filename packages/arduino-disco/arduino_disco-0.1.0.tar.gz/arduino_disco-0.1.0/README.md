# Arduino Disco

A lightweight Python library and CLI tool to discover Arduino boards connected via serial ports. It matches connected devices against the Arduino board database to provide FQBN (Fully Qualified Board Name) and architecture information.

The project is available on GitHub: [https://github.com/christoph2/arduino-disco](https://github.com/christoph2/arduino-disco)

## Features

- **Automated Discovery**: Scans serial ports and identifies connected Arduino-compatible hardware.
- **Board Database Matching**: Uses your local Arduino installation to identify boards.
- **Heuristic Scoring**: Smart matching based on VID/PID, product strings, and manufacturer information.
- **CLI Tool**: Quick overview of connected boards directly from the terminal.
- **Python API**: Easy integration into your own Python projects.

## Installation

```bash
pip install arduino-disco
```

## Usage

### Command Line Interface (CLI)

Run the tool to list discovered boards:

```bash
arduino-disco
```

To include all serial ports (even unrecognized ones), use the `--all` or `-a` flag:

```bash
arduino-disco --all
```

Example output for `--all`:
```text
Port         Board                          FQBN                           Core      
COM6         Unknown                        -                              -         
COM11        Unknown                        -                              -         
COM5         Unknown                        -                              -         
COM7         Unknown                        -                              -         
COM10        Arduino Uno                    arduino:avr:uno                avr       
COM4         Arduino Uno                    arduino:avr:uno                avr       
COM8         ESP32 Family Device            esp32:esp32:esp32_family       esp32 
```

Example output (default):
```text
Port         Board                          FQBN                           Core
COM4         Arduino Uno                    arduino:avr:uno                avr       
COM8         ESP32 Family Device            esp32:esp32:esp32_family       esp32     
```

### Python API

You can use the library in your own scripts:

```python
from arduinodisco import discover_boards

# Get only recognized boards
boards = discover_boards()

for entry in boards:
    print(f"Found {entry.board.name} on {entry.port.device}")
    print(f"FQBN: {entry.board.fqbn}")

# Get all ports, including unrecognized ones
all_ports = discover_boards(include_all_ports=True)
```

## Development

### Prerequisites

Install development dependencies:

```bash
pip install -e ".[dev]"
```

### Versioning

To bump the version (using [bumpver](https://pypi.org/project/bumpver/)):

```bash
bumpver update --patch
```

### Pre-commit Hooks

To ensure code quality, install the pre-commit hooks:

```bash
pre-commit install
```

## License

This project is licensed under the MIT License - see the `pyproject.toml` for details.
