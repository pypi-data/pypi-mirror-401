# dir.py - absolute path directory layout constants in deployed environment
import os

root = "."
stages = "."
output = "."

def set_root(root_path):
	global root, stages, output
	root = os.path.abspath(root_path)
	stages = os.path.join(root, "stages")
	output = os.path.join(root, "output")

def validate(subdirs=None):
    if root in (".", None):
        raise RuntimeError("Dir.set_root() must be called before validate()")

    check = subdirs or ["stages", "output"]
    for d in check:
        full = os.path.join(root, d)
        if not os.path.isdir(full):
            raise RuntimeError(f"Missing required directory: {full}")
