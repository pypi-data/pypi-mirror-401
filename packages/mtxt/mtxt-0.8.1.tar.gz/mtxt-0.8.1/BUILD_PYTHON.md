# Building MTXT Python Bindings

Quick guide to build and test the Python bindings.

## Prerequisites

```bash
# Install Rust (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install maturin
pip install maturin
```

## Development Build

```bash
# Build and install in development mode (fast iteration)
maturin develop --features python,midi

# The module will be installed in your current Python environment
python -c "import mtxt; print(mtxt.__version__)"
```

## Release Build

```bash
# Build optimized version
maturin develop --release --features python,midi
```

## Testing

```bash
# Run the test suite
python test_python.py
```

## Building Wheels for Distribution

```bash
# Build a wheel
maturin build --release --features python,midi

# Install the wheel
pip install target/wheels/mtxt-*.whl
```

## Quick Test

```python
import mtxt

# Parse MTXT
content = """mtxt v1
0 tempo 120
0 note C4 dur=1
"""

file = mtxt.parse(content)
print(f"Version: {file.version}")
print(f"Duration: {file.duration} beats")
print(f"Records: {len(file)}")

# Save to file
file.save("test.mtxt")

# Convert to MIDI
file.to_midi("test.mid")

print("Success!")
```

## Troubleshooting

### Build fails with pyo3 errors

Make sure you're enabling the python feature:
```bash
maturin develop --features python,midi
```

### Import error

Make sure you've run `maturin develop`:
```bash
maturin develop --features python,midi
python -c "import mtxt"
```

### MIDI functions not available

Make sure the midi feature is enabled:
```bash
maturin develop --features python,midi
```

## Documentation

See [PYTHON_BINDINGS.md](PYTHON_BINDINGS.md) for comprehensive documentation.
