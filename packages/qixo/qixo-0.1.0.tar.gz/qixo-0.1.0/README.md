# qixo

[![PyPI](https://img.shields.io/pypi/v/qixo.svg)](https://pypi.org/project/qixo/)
[![Tests](https://github.com/jeorgexyz/qixo/actions/workflows/test.yml/badge.svg)](https://github.com/jeorgexyz/qixo/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/jeorgexyz/qixo/blob/main/LICENSE)

A lightweight Python library for executing JavaScript in a QuickJS sandbox.

## Why qixo?

- **Fast**: QuickJS starts in milliseconds with minimal memory overhead
- **Safe**: Execute untrusted JavaScript with memory and time limits
- **Simple**: Clean Python API with automatic JSON data exchange
- **Lightweight**: ~700KB QuickJS engine, no heavy dependencies

## Installation

```bash
pip install qixo
```

## Quick Start

```python
from qixo import Qixo

# Basic usage
with Qixo() as box:
    result = box.eval("1 + 1")
    print(result)  # 2
    
    # JSON data exchange
    result = box.eval("({name: 'qixo', version: 1})")
    print(result)  # {'name': 'qixo', 'version': 1}
    
    # State persists between evals
    box.eval("var x = 10")
    box.eval("var y = 20")
    result = box.eval("x + y")
    print(result)  # 30
```

## Features

### Memory and Time Limits

```python
# Limit memory to 10MB and execution time to 1 second
with Qixo(memory_limit_mb=10, timeout_ms=1000) as box:
    result = box.eval("'a'.repeat(1000)")  # Works fine
    
    try:
        # This will raise QixoError due to memory limit
        box.eval("'a'.repeat(100000000)")
    except QixoError as e:
        print(f"Error: {e}")
```

### Error Handling

```python
from qixo import Qixo, QixoError

with Qixo() as box:
    try:
        box.eval("throw new Error('Something went wrong')")
    except QixoError as e:
        print(f"JavaScript error: {e}")
        print(f"Stack trace: {e.stack}")
```

### Working with Functions

```python
with Qixo() as box:
    # Define a function
    box.eval("""
        function fibonacci(n) {
            if (n <= 1) return n;
            return fibonacci(n - 1) + fibonacci(n - 2);
        }
    """)
    
    # Call it
    result = box.eval("fibonacci(10)")
    print(result)  # 55
```

## Development

```bash
# Clone the repository
git clone https://github.com/jeorgexyz/qixo.git
cd qixo

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=qixo --cov-report=html
```

## License

Apache 2.0

## Credits

Built on top of the excellent [quickjs](https://github.com/PetterS/quickjs) Python bindings.
