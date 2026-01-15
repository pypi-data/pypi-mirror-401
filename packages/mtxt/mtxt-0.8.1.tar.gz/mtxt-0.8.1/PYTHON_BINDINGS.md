# MTXT Python Bindings

High-performance Python bindings for the MTXT Music Text Format library, built with PyO3 and Maturin.

## Features

- 🚀 **High Performance**: Rust-powered parsing and conversion
- 🎵 **Full MTXT Support**: Parse and generate MTXT files
- 🎹 **MIDI Conversion**: Bidirectional conversion between MTXT and MIDI
- 🔍 **Type Safe**: Complete type hints (.pyi stubs) for mypy and IDE support
- 🛡️ **Robust Error Handling**: Meaningful Python exceptions, not panics
- 📦 **Easy to Use**: Pythonic API with classes and methods

## Installation

### From Source (Development)

```bash
# Install maturin (the build tool)
pip install maturin

# Build and install in development mode
maturin develop --features python,midi

# Or for release mode (optimized)
maturin develop --release --features python,midi
```

### Building a Wheel

```bash
# Build a wheel for distribution
maturin build --release --features python,midi

# The wheel will be in target/wheels/
pip install target/wheels/mtxt-*.whl
```

## Quick Start

### Parsing MTXT Files

```python
import mtxt

# Parse from string
content = """mtxt v1
meta global title "My Song"
meta global composer "Me"
0 tempo 120
0 timesig 4/4
0 note C4 dur=1 vel=100
1 note D4 dur=1 vel=100
2 note E4 dur=1 vel=100
"""

file = mtxt.parse(content)
print(f"Version: {file.version}")
print(f"Duration: {file.duration} beats")
print(f"Records: {len(file)}")
```

### Loading from File

```python
import mtxt

# Load from disk
file = mtxt.load("song.mtxt")

# Or use the class method
file = mtxt.MtxtFile.from_file("song.mtxt")

# Save to disk
file.save("output.mtxt")
```

### Working with Metadata

```python
import mtxt

file = mtxt.parse("""mtxt v1
meta global title "Test"
meta global artist "Artist"
""")

# Get all metadata as a list of tuples
for key, value in file.metadata:
    print(f"{key}: {value}")

# Get a specific metadata value
title = file.get_meta("title")
print(f"Title: {title}")

# Set metadata
file.set_metadata("composer", '"John Doe"')
```

### MIDI Conversion

```python
import mtxt

# Convert MIDI to MTXT
file = mtxt.midi_to_mtxt("input.mid", verbose=True)
file.save("output.mtxt")

# Convert MTXT to MIDI
file = mtxt.load("input.mtxt")
file.to_midi("output.mid", verbose=True)

# Or use the convenience function
mtxt.mtxt_to_midi("input.mtxt", "output.mid")
```

## API Reference

### `MtxtFile` Class

The main class representing an MTXT file.

#### Constructor

```python
file = mtxt.MtxtFile()  # Create empty file
```

#### Class Methods

- `parse(content: str) -> MtxtFile`: Parse MTXT from string
- `from_file(path: str) -> MtxtFile`: Load MTXT from file
- `from_midi(path: str, verbose: bool = False) -> MtxtFile`: Convert MIDI to MTXT

#### Instance Methods

- `save(path: str)`: Save MTXT to file
- `to_midi(path: str, verbose: bool = False)`: Convert to MIDI file
- `get_meta(key: str) -> Optional[str]`: Get metadata value
- `set_metadata(key: str, value: str)`: Set metadata value

#### Properties

- `version: Optional[str]`: MTXT version from header
- `metadata: List[Tuple[str, str]]`: All global metadata
- `duration: Optional[float]`: Duration in beats

#### Special Methods

- `__len__() -> int`: Number of records
- `__str__() -> str`: MTXT content as string
- `__repr__() -> str`: Debug representation

### Module Functions

```python
# Parse from string
file = mtxt.parse(content: str) -> MtxtFile

# Load from file
file = mtxt.load(path: str) -> MtxtFile

# MIDI conversions
file = mtxt.midi_to_mtxt(midi_path: str, verbose: bool = False) -> MtxtFile
mtxt.mtxt_to_midi(mtxt_path: str, midi_path: str, verbose: bool = False)
```

### Exceptions

- `mtxt.ParseError`: Raised when MTXT content cannot be parsed (subclass of `ValueError`)
- `mtxt.ConversionError`: Raised when conversion fails (subclass of `RuntimeError`)
- Standard Python exceptions: `IOError`, etc.

## Type Hints and IDE Support

The package includes complete type hints in `mtxt.pyi`. This enables:

- **mypy** static type checking
- **IDE autocompletion** (VSCode, PyCharm, etc.)
- **Better documentation** in your editor

```python
import mtxt

# Your IDE will provide autocompletion and type checking
file: mtxt.MtxtFile = mtxt.parse("mtxt v1\n0 note C4")
duration: float = file.duration  # Type-safe
```

## Error Handling

The bindings translate Rust errors into appropriate Python exceptions:

```python
import mtxt

# Parse errors
try:
    file = mtxt.parse("invalid content")
except mtxt.ParseError as e:
    print(f"Parse error: {e}")

# I/O errors
try:
    file = mtxt.load("/nonexistent/file.mtxt")
except IOError as e:
    print(f"File error: {e}")

# Conversion errors
try:
    file.to_midi("/invalid/path.mid")
except mtxt.ConversionError as e:
    print(f"Conversion error: {e}")
```

## Performance

The Python bindings are built on top of the high-performance Rust library, providing:

- Fast parsing (typically 10-100x faster than pure Python)
- Efficient memory usage
- Zero-copy string operations where possible
- Parallel processing capabilities (in Rust layer)

## Testing

Run the test suite to verify the bindings work correctly:

```bash
# Build in development mode
maturin develop --features python,midi

# Run tests
python test_python.py
```

## Development

### Project Structure

```
mtxt/
├── src/
│   ├── python.rs          # PyO3 bindings
│   ├── lib.rs             # Rust library
│   └── ...
├── python/
│   └── mtxt/
│       └── __init__.pyi   # Type stubs
├── pyproject.toml         # Python package configuration
├── Cargo.toml             # Rust configuration
└── test_python.py         # Python tests
```

### Building

```bash
# Development build (faster compile, slower runtime)
maturin develop --features python,midi

# Release build (slower compile, faster runtime)
maturin develop --release --features python,midi

# Build wheel for distribution
maturin build --release --features python,midi
```

### Features

The Python bindings support these Cargo features:

- `python`: Enables PyO3 bindings (required)
- `midi`: Enables MIDI conversion (optional but recommended)

## Publishing

To publish to PyPI:

```bash
# Build wheels for all platforms (requires Docker for Linux)
maturin build --release --features python,midi

# Upload to PyPI
maturin publish --features python,midi
```

## Architecture

### Design Principles

1. **Type Safety**: Full type hints, no "stringly-typed" API
2. **Meaningful Errors**: Rust errors map to appropriate Python exceptions
3. **Pythonic API**: Classes and methods, not just functions
4. **Zero Overhead**: Minimal wrapper layer over Rust code
5. **Memory Safe**: Rust's ownership model prevents memory errors

### The `MtxtFile` Class

The `MtxtFile` class wraps the Rust `MtxtFile` struct, allowing Python users to:

- Inspect parsed MTXT data
- Access metadata programmatically
- Convert between formats
- Serialize back to MTXT

This is much better than a simple "string in, string out" API because it enables:

- Data manipulation before conversion
- Inspection and validation
- Building MTXT files programmatically

## Examples

### Creating MTXT Programmatically

```python
import mtxt

# Create an empty file
file = mtxt.MtxtFile()

# Add metadata
file.set_metadata("title", '"Generated Song"')
file.set_metadata("composer", '"Python Script"')

# Note: Direct record manipulation is not yet exposed,
# but you can parse and manipulate via strings
content = str(file)
# ... modify content ...
file = mtxt.parse(content)
```

### Batch Processing

```python
import mtxt
from pathlib import Path

# Convert all MIDI files in a directory
for midi_file in Path("midi_files").glob("*.mid"):
    mtxt_file = mtxt.midi_to_mtxt(str(midi_file))
    output = midi_file.with_suffix(".mtxt")
    mtxt_file.save(str(output))
    print(f"Converted {midi_file} -> {output}")
```

### Integration with Data Analysis

```python
import mtxt
import pandas as pd
from pathlib import Path

# Collect metadata from multiple files
data = []
for file_path in Path("songs").glob("*.mtxt"):
    file = mtxt.load(str(file_path))
    data.append({
        "filename": file_path.name,
        "title": file.get_meta("title"),
        "composer": file.get_meta("composer"),
        "duration": file.duration,
        "records": len(file),
    })

df = pd.DataFrame(data)
print(df)
```

## Troubleshooting

### Build Errors

**Error: `pyo3` not found**

Make sure you've added the `python` feature:

```bash
maturin develop --features python,midi
```

**Error: Python version mismatch**

Ensure your Python version is >= 3.8:

```bash
python --version
```

### Runtime Errors

**ImportError: cannot import name 'mtxt'**

Make sure you've built the module:

```bash
maturin develop --features python,midi
```

**Module has no attribute 'midi_to_mtxt'**

The MIDI feature is not enabled. Rebuild with:

```bash
maturin develop --features python,midi
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please:

1. Add tests for new functionality
2. Update type stubs (`.pyi` files)
3. Follow existing code style
4. Ensure all tests pass

## Credits

- Built with [PyO3](https://pyo3.rs/) - Rust bindings for Python
- Built with [Maturin](https://www.maturin.rs/) - Build system for Rust-Python projects
