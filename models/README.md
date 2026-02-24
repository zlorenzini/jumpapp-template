# Model storage
#
# Model files live here, relative to the app root.  Because all paths in
# jumpapp.json are relative, the entire app directory is self-contained and
# can be placed anywhere on a USB drive (or any other storage medium).
#
# Typical USB drive layout (multiple apps are supported out of the box):
#
#   /mnt/<drive>/
#       MyJumpApp/
#           jumpapp.json
#           server/main.py
#           ui/index.html
#           models/        <-- this directory
#           dataset/
#           endpoints/
#       AnotherApp/
#           jumpapp.json
#           ...
#
# The server resolves the app root from its own __file__ path, so no
# configuration is needed when the drive is re-mounted or renamed.
#
# Supported formats:
#   .onnx    — ONNX Runtime
#   .tflite  — TensorFlow Lite
#   .pt      — PyTorch (TorchScript)
#
# Reference the default model in jumpapp.json:
#   "models": { "default": "models/model.onnx" }
#
# The server creates this directory automatically on first startup.
