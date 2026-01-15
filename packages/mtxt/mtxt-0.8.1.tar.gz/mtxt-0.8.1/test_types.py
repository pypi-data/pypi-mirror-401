"""Type checking test for mtxt bindings"""
import mtxt

# Test static type checking
file: mtxt.MtxtFile = mtxt.parse("mtxt 1.0\n0 note C4")
version: str | None = file.version
duration: float | None = file.duration
metadata: list[tuple[str, str]] = file.metadata

# Test method signatures
file.save("output.mtxt")
file.to_midi("output.mid", verbose=True)
meta_value: str | None = file.get_meta("title")
file.set_metadata("key", "value")

# Test module functions
file2: mtxt.MtxtFile = mtxt.load("input.mtxt")
file3: mtxt.MtxtFile = mtxt.midi_to_mtxt("input.mid")
mtxt.mtxt_to_midi("input.mtxt", "output.mid")

# Test exceptions
try:
    mtxt.parse("invalid")
except mtxt.ParseError as e:
    error_msg: str = str(e)

try:
    file.to_midi("/invalid/path.mid")
except mtxt.ConversionError as e:
    error_msg2: str = str(e)

print("Type annotations are correct!")
