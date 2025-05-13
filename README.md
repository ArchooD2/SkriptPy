
# SkriptPy

SkriptPy is a Python library and transpiler for working with Skript, a Bukkit plugin for creating custom scripts in Minecraft servers. This project enables bidirectional transpilation between Python and Skript, allowing you to write your server logic in Python and convert it to Skript, or convert existing Skript code to Python.

## Features

- Write Skript code using a Python-based domain-specific language (DSL)
- Transpile Python scripts to Skript files
- Convert Skript files to Python scripts
- Support for common Skript constructs:
  - Commands
  - Events
  - Variables (persistent and local)
  - Control flow (if/else, loops)
  - Actions (send, broadcast, teleport)

## Installation

```bash
# Clone the repository
git clone https://github.com/ArchooD2/SkriptPy.git
cd SkriptPy

# Install the package
pip install -e .
```

## Usage

### Python to Skript

Write your Skript logic in Python using the SkriptPy DSL:

```python
from skriptpy import *

@command("hello")
def _():
    send("Hello, world!")
```

Transpile it to Skript:

```bash
python skriptpy-transpile.py example.py example.sk
```

### Skript to Python

Convert existing Skript code to Python:

```bash
python skriptpy-transpile.py example.sk example_converted.py
```

## API Reference

### Decorators

- `@command(name)`: Define a Skript command
- `@event(name, condition=None)`: Define a Skript event handler
- `@function(name, *params)`: Define a Skript function

### Actions

- `send(msg)`: Send a message to the player
- `broadcast(msg)`: Broadcast a message to all players
- `teleport(entity, location)`: Teleport an entity to a location

### Variables

- `set_var(name, value)`: Set a persistent variable
- `get_var(name)`: Get a persistent variable
- `set_local(name, value)`: Set a local variable
- `get_local(name)`: Get a local variable

### Control Flow

- `with If(condition):`: Start an if block
- `with Else():`: Start an else block
- `with loop_times(n):`: Loop n times
- `with loop_players():`: Loop over all players

## License

MIT

## Contributing

Contributions are welcome! Please submit a Pull Request.
