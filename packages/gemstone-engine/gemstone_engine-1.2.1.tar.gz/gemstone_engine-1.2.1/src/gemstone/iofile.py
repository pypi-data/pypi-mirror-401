# iofile.py
import os
from dataclasses import dataclass
from gemstone.generic_helpers import read_lines_strip_comments
import re
from typing import Dict, Tuple, Set, List

import logging
logger = logging.getLogger(__name__)


from dataclasses import dataclass, field

@dataclass
class IOFile:
    IN_STRINGS = ["input", "in"]
    OUT_STRINGS = ["output", "out"]

    name: str
    ext: str
    direction: str  # in/out
    stage: str      # module it belongs to
    standard: str = field(default="")  # refers to entry in standards.txt

    @property
    def parts(self):
        # Parse self.name as path, split on /
        return self.name.split("/")
    
    @property
    def variables(self):
        # Return variables like <id> or {id} as ['id']
        import re
        return re.findall(r"[<{]([a-zA-Z0-9_]+)[>}]?", self.name)
    
    @property
    def has_variable(self) -> bool:
        return any(self.is_variable(p) for p in self.parts)

    @property
    def base(self):
        """First part of the iofile path (top-level group/filename)."""
        return self.parts[0]

    @property
    def subparts(self):
        """All parts after the first (subdirectories etc)."""
        return self.parts[1:]

    @staticmethod
    def strip_variable_markers(part: str) -> str:
        return part.lstrip('<{').rstrip('>}')

    def is_variable(self, part: str) -> bool:
        return (part.startswith('<') and part.endswith('>')) or \
            (part.startswith('{') and part.endswith('}'))
    
    def get_concrete_name(self, mapping: dict) -> str:
        # Replace <var> or {var} in self.name with mapping[var]
        result = self.name
        for var in self.variables:
            val = mapping.get(var)
            if val is None:
                raise ValueError(f"Missing variable for '{var}'")
            result = result.replace(f"<{var}>", str(val)).replace(f"{{{var}}}", str(val))
        return result

    def __post_init__(self):
        self._validate_name(self.name)
        self.ext = self.ext.lstrip(".")
        self.direction = self._normalize_direction(self.direction)

    def _normalize_direction(self, direction: str) -> str:
        """
        Normalize IOFile direction strings to 'in' or 'out'.
        Raises ValueError if not recognized.
        """
        d = direction.strip().lower()
        if d in self.IN_STRINGS:
            return "in"
        elif d in self.OUT_STRINGS:
            return "out"
        raise ValueError(f"Invalid direction: '{direction}' (expected 'in'/'out'/'input'/'output')")


    def is_input(self) -> bool:
        return self.direction.lower() in self.IN_STRINGS

    def is_output(self) -> bool:
        return self.direction.lower() in self.OUT_STRINGS

    @staticmethod
    def _validate_name(name: str):
        if not isinstance(name, str) or not name:
            raise ValueError("IOFile.name must be a non-empty string")

        if '.' in name:
            raise ValueError(f"IOFile.name '{name}' must not contain '.'")

        if name.startswith('/') or name.endswith('/'):
            raise ValueError(f"IOFile.name '{name}' must not start or end with '/'")

        parts = name.split('/')
        for part in parts:
            if not part:
                raise ValueError(f"IOFile.name '{name}' contains consecutive or empty '/' segments")

            # Accept mixed literal and placeholder segments like out_<id>_chunk
            token_pattern = r'(?:[a-zA-Z0-9_-]+|<[^>]+>|{[^}]+})+'
            if not re.fullmatch(token_pattern, part):
                raise ValueError(f"IOFile.name '{name}' has invalid characters in part '{part}'")
          
def parse_iofiles_txt(stage_name: str, iofiles_path: str) -> List[IOFile]:
    """
    Parse iofiles.txt and return a list of IOFile objects (direction is a field).
    Allows tab, comma, or whitespace as delimiters.
    Supports optional 'standard' column (warns if missing).
    """
    lines = read_lines_strip_comments(iofiles_path)

    if not lines:
        raise ValueError(f"{iofiles_path} is empty or contains only comments.")

    # --- Parse header
    header = re.split(r"[\t, ]+", lines[0].strip())
    header = [h.lower() for h in header if h.strip()]
    expected_min = ["direction", "name", "ext"]
    expected_full = ["direction", "name", "ext", "standard"]

    # detect header type
    if header == expected_full:
        has_standard = True
    elif header == expected_min:
        has_standard = False
        logger.warning(f"{iofiles_path}: missing 'standard' column (legacy format).")
    else:
        raise ValueError(
            f"{iofiles_path}: header must contain either "
            f"{' '.join(expected_full)} or {' '.join(expected_min)}"
        )

    # --- Parse lines
    iofiles = []
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = re.split(r"[\t, ]+", line.strip())
        parts = [p for p in parts if p != ""]

        # handle missing column
        if has_standard and len(parts) != 4:
            raise ValueError(f"{iofiles_path}: line must have 4 fields when 'standard' column is present: {line}")
        if not has_standard and len(parts) != 3:
            raise ValueError(f"{iofiles_path}: line must have 3 fields (direction, file, ext): {line}")

        if has_standard:
            direction, name, ext, standard = parts
        else:
            direction, name, ext = parts
            standard = ""

        iofiles.append(IOFile(
            name=name,
            ext=ext,
            direction=direction,
            stage=stage_name,
            standard=standard
        ))

    if not iofiles:
        raise ValueError(f"{iofiles_path} contains no valid file entries.")

    return iofiles
