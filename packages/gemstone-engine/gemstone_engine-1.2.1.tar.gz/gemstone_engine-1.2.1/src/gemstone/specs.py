# specs.py
"""
This module reads and validates specs to define param attributes.

Spec file syntax:
- Key-value pairs: key: specification
- Specification components:
    - requirement: required, optional, shared
    - default: default(value)
    - options: options(option1,option2)
    - range: range(min-max)
    - type: int, float, string, path, file
    - path validation: exists, create

Example:
    input_data_path: path required exists
    color: string options(red,green,blue) default(green)

For more details, see the user guide.
"""

import logging
import os
import re
from gemstone.generic_helpers import parse_string_to_list, parse_string_to_range


class Spec:
    """Represents a single param specification."""
    
    # Constraint types
    NONE = "none"
    RANGE = "range"
    OPTIONS = "options"
    CREATE = "create"
    MUST_EXIST = "must_exist"

    # Valid param types
    INT = "int"
    FLOAT = "float"
    STRING = "string"
    PATH = "path"
    FILE = "file"

    def __init__(self, key):
        """Initialize the Spec instance with default attributes."""
        self.key = key
        self.type = None
        self.required = False
        self.shared = False
        self.writable = False
        self.default = None
        self.constraint_type = Spec.NONE
        self.options = []
        self.source_modules = []
        self.range_min = -999999
        self.range_max = 999999
        self.INPUT = False
        
    def is_input(self) -> bool:
        return self.INPUT

    @classmethod
    def parse(cls, line: str, source_module: str = 'unit_test', *, filepath: str = "", line_number: int = -1):
        """Parse a single spec line into a Spec object, with optional error context."""
        try:
            # Remove comments
            line_clean = line.split("#", 1)[0].strip()
            if not line_clean:
                return None  # Skip blank lines

            if ":" not in line_clean:
                raise ValueError("Missing colon")

            key, value = line_clean.split(":", 1)

            spec = cls(key.strip())    
            spec._parse_value(value.strip())
            spec._validate_spec()
            spec.source_modules = [source_module]
            return spec

        except Exception as e:
            context = f" (line {line_number})" if line_number is not None else ""
            context += f" in file '{filepath}'" if filepath else ""
            raise ValueError(
                f"Error parsing spec line{context}:\n  {line.strip()}\n  Reason: {e}"
            ) from e

    def _validate_token_conflict(self, new_token: str):
        """
        Check whether a new token conflicts with existing settings.
        Raise a ValueError if a conflict is detected.
        """
        if new_token == "required":
            if self.required:
                raise ValueError(f"Duplicate token 'required' for key: {self.key}")
            if self.default is not None:
                raise ValueError(f"'required' conflicts with 'default' for key: {self.key}")
        elif new_token == "optional":
            if self.required:
                raise ValueError(f"Conflicting 'required' and 'optional' for key: {self.key}")
            if self.required:
                raise ValueError(f"'shared' token conflicts with 'required' for key: {self.key}")
        elif new_token == "shared":
            if self.shared:
                raise ValueError(f"Duplicate token 'shared' for key: {self.key}")
        elif new_token == "writable":
            if self.writable:
                raise ValueError(f"Duplicate token 'writable' for key: {self.key}")
        elif new_token in {"int", "float", "string", "path", "file"}:
            if self.type is not None and self.type != new_token:
                raise ValueError(f"Conflicting type tokens '{self.type}' and '{new_token}' for key: {self.key}")
            if self.constraint_type in {Spec.MUST_EXIST, Spec.CREATE} and new_token not in {"path", "file"}:
                raise ValueError(f"Type '{new_token}' conflicts with constraint '{self.constraint_type}' for key: {self.key}")
        elif new_token in {"exists", "create"}:
            if self.constraint_type is not None and self.constraint_type != Spec.NONE:
                raise ValueError(f"Conflicting constraints '{self.constraint_type}' and '{new_token}' for key: {self.key}")
            if self.type not in {"path", "file"}:
                raise ValueError(f"Constraint '{new_token}' requires type 'path' or 'file' for key: {self.key}")
        elif new_token.startswith("default("):
            if self.default is not None:
                raise ValueError(f"Duplicate 'default' token for key: {self.key}")
            if self.required:
                raise ValueError(f"'default' conflicts with 'required' for key: {self.key}")
        elif new_token.startswith("options("):
            if self.constraint_type in {Spec.OPTIONS}:
                raise ValueError(f"Multiple 'options' specified for key: {self.key}")
            if self.constraint_type in {Spec.RANGE}:
                raise ValueError(f"Conflicting 'options' and 'range' for key: {self.key}")
        elif new_token.startswith("range("):
            if self.constraint_type in {Spec.RANGE}:
                raise ValueError(f"Multiple 'range' specified for key: {self.key}")
            if self.constraint_type in {Spec.OPTIONS}:
                raise ValueError(f"Conflicting constraint types 'options' and 'range' for key: {self.key}")
        elif new_token == "INPUT":
            if self.INPUT:
                raise ValueError(f"Duplicate token 'INPUT' for key: {self.key}")
            if self.default is not None:
                raise ValueError(f"'INPUT' conflicts with 'default' for key: {self.key}")
            
        else:
            raise ValueError(f"Unknown token: {new_token}")

    def _parse_value(self, value: str):
        """Parse tokens and assign attributes based on specification patterns."""
        patterns = {
            "range": r"range\(([^)]+)\)",
            "options": r"options\(([^)]+)\)",
            "default": r"default\(([^)]+)\)",
        }

        # Extract and process patterns
        for spec_type, pattern in patterns.items():
            match = re.search(pattern, value)
            if match:
                content = match.group(1).strip()
                value = value.replace(match.group(0), "").strip()

                if spec_type == "range":
                    try:
                        min_val, max_val = map(float, parse_string_to_range(content))
                        self.range_min = min_val
                        self.range_max = max_val
                        self.constraint_type = Spec.RANGE
                    except ValueError as e:
                        raise ValueError(f"Invalid range syntax: {content}. Error: {e}")
                elif spec_type == "options":
                    delimiters = [","," ", "-"]
                    self.options = parse_string_to_list(content, delimiters)
                    self.constraint_type = Spec.OPTIONS
                elif spec_type == "default":
                    self.default = content

        # Parse remaining tokens
        tokens = value.split()
        for token in tokens:
            self._validate_token_conflict(token)            
            if token == "required":
                self.required = True
            elif token == "optional":
                self.required = False
            elif token == "INPUT":
                self.INPUT = True    
            elif token == "shared":
                self.shared = True
            elif token == "writable":
                self.writable = True
            elif token == "int":
                self.type = Spec.INT
            elif token == "float":
                self.type = Spec.FLOAT
            elif token == "string":
                self.type = Spec.STRING
            elif token == "path":
                self.type = Spec.PATH
            elif token == "file":
                self.type = Spec.FILE
            elif token == "exists":
                if Spec.CREATE == self.constraint_type:
                    raise ValueError(f"Conflicting constraints for key: {self.key}. Both 'exists' and 'create' cannot be specified.")
                self.constraint_type = Spec.MUST_EXIST
            elif token == "create":
                if Spec.MUST_EXIST == self.constraint_type:
                    raise ValueError(f"Conflicting constraints for key: {self.key}. Both 'exists' and 'create' cannot be specified.")
                self.constraint_type = Spec.CREATE
            else:
                raise ValueError(f"Unknown token: {token}")
            
        # --- Post-processing: cast options and default to declared type ---
        if self.type == Spec.INT:
            if self.constraint_type == Spec.OPTIONS:
                self.options = [int(x) for x in self.options]
            if self.default is not None:
                self.default = int(self.default)

        elif self.type == Spec.FLOAT:
            if self.constraint_type == Spec.OPTIONS:
                self.options = [float(x) for x in self.options]
            if self.default is not None:
                self.default = float(self.default)

        elif self.type in (Spec.PATH, Spec.FILE, Spec.STRING):
            # Just ensure it's stripped and string
            if self.default is not None:
                self.default = str(self.default).strip()


    def _validate_spec(self):
        """Validate parsed attributes for logical consistency."""
        # Ensure type is specified
        if not self.type:
            raise ValueError(f"Missing type for spec key: {self.key}")

        # Ensure valid constraint type
        if self.constraint_type == Spec.RANGE and (self.range_min is None or self.range_max is None):
            raise ValueError(f"Range must specify both min and max values for key: {self.key}")
        
        # options
        if self.constraint_type == Spec.OPTIONS and not self.options:
            raise ValueError(f"Options must specify at least one option for key: {self.key}")

        if self.constraint_type == Spec.OPTIONS:
            if len(self.options) != len(set(self.options)):
                raise ValueError(f"Duplicate options found for key: {self.key}. Options must be unique.")

        # Ensure default is valid for constraints
        if self.default:
            if self.constraint_type == Spec.RANGE:
                if not (self.range_min <= float(self.default) <= self.range_max):
                    raise ValueError(f"Default value {self.default} is outside range for key: {self.key}")
            elif self.constraint_type == Spec.OPTIONS:
                if self.default not in self.options:
                    raise ValueError(f"Default value {self.default} is not in options for key: {self.key}")

        # Ensure path constraints require type 'path'
        if self.constraint_type in {Spec.MUST_EXIST, Spec.CREATE} and not (self.type in {Spec.FILE, Spec.PATH}):
            raise ValueError(f"Existence and creation constraints require type 'path' or 'file' for key: {self.key}")
        
        # INPUT must be provided path or file
        if self.INPUT:
            if self.default is not None:
                raise ValueError(f"'INPUT' param cannot have a default: {self.key}")
            if self.type not in {Spec.PATH, Spec.FILE}:
                raise ValueError(f"'INPUT' param must have type 'path' or 'file': {self.key}")


    def __repr__(self):
        return (f"Spec(key={self.key}, type={self.type}, required={self.required}, "
                f"shared={self.shared}, writable={self.writable}, default={self.default}, "
                f"constraint_type={self.constraint_type}, options={self.options}, "
                f"range={self.range_min} to {self.range_max})")

    def __eq__(self, other):
        if not isinstance(other, Spec):
            return False
        return (
            self.key == other.key and
            self.type == other.type and
            self.required == other.required and
            self.shared == other.shared and
            # self.writable == other.writable not included as same param me be writable some places only
            self.default == other.default and
            self.constraint_type == other.constraint_type and
            self.options == other.options and
            self.range_min == other.range_min and
            self.range_max == other.range_max and
            self.INPUT == other.INPUT
        )
class Specs:
    """Manages a collection of validated Spec instances."""

    def __init__(self):
        """Initialize an empty Specs collection."""
        self.specs = {}  # Dictionary mapping key -> Spec instance

    def load_from_file(self, filepath: str):
        """
        Load and parse a specs file.

        Args:
            filepath (str): Path to the specs.txt file.

        Raises:
            ValueError: If duplicate or invalid keys are detected.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Specs file not found: {filepath}")

        source_module = os.path.basename(os.path.dirname(filepath))
        with open(filepath, 'r') as file:
            for i, line in enumerate(file, 1):
                self.add_line(line, source_module, filepath, i)

        return self

    def add_line(self, line: str, source_module: str, filepath: str = "", line_number: int = -1):
        """
        Add a line from the specs file to the collection.

        Args:
            line (str): A single line from the specs file.
            filepath (str): Path to the specs file for context in error messages.
            line_number (int): Number of the line being processed

        Raises:
            ValueError: If the line contains invalid data or conflicts.
        """
        spec = Spec.parse(line, source_module, filepath=filepath, line_number=line_number)

        if not spec:
            return  # Skip blank lines

        if spec.key in self.specs:
            existing_spec = self.specs[spec.key]
            if spec.shared and existing_spec.shared:
                if spec != existing_spec:
                    raise ValueError(
                        f"Conflicting attributes for key '{spec.key}'. "
                        f"Existing: {existing_spec}, New: {spec}"
                    )
                else:
                    # ✅ merge source modules into the existing spec
                    existing_spec.source_modules.extend(spec.source_modules)
                return  # ✅ don’t overwrite the existing spec
            else:
                raise ValueError(f"Duplicate key '{spec.key}' without valid shared attribute.")

        # ✅ brand new key
        self.specs[spec.key] = spec

    def validate(self):
        """
        Perform any additional validation on the collection.

        Raises:
            ValueError: If any inconsistencies are found.
        """
        for spec in self.specs.values():
            if spec.shared and not spec.required:
                logging.warning(f"Shared key '{spec.key}' is not marked as required.")

    def items(self):
        return self.specs.items()  # Allow iteration like a dictionary

    def __getitem__(self, key):
        """
        Allow dictionary-style access to specs.
        
        Args:
            key (str): The key of the spec to retrieve.

        Returns:
            Spec: The corresponding Spec instance.
        """
        return self.specs[key]

    def __iter__(self):
        """Iterate over the keys in the specs collection."""
        return iter(self.specs)

    def __repr__(self):
        return f"Specs({self.specs})"

def write_param_template_file_from_specs(specs, out_file, stage_name):
    """Write param template entries for a single Specs object."""
    placeholder_map = {
        "int": "9999",
        "float": "99.99",
        "string": "zzzz",
        "path": "/x/y/z"
    }

    out_file.write(f"# {stage_name} params\n\n")


    for key, spec in specs.items():
        if spec.key.startswith("#") or not spec.key.strip():
            continue  # Skip comments or blanks if any remain

        placeholder = placeholder_map.get(spec.type if spec.type else "string", "zzzz")
        source = ' '.join(spec.source_modules)
        out_file.write(f"{spec.key}: {placeholder}   # {spec.type} in {source}\n")


    out_file.write("\n")


def write_param_template_file(stage_dirs, out_path):
    """Generate param template file using all stage specs."""
    try:
        with open(out_path, 'w') as out_file:
            for stage_dir in stage_dirs:
                specs_path = os.path.join(stage_dir, "specs.txt")
                if not os.path.exists(specs_path):
                    raise FileNotFoundError(f"Spec file '{specs_path}' not found")

                specs = Specs()
                specs.load_from_file(specs_path)
                write_param_template_file_from_specs(specs, out_file, stage_dir)

    except FileNotFoundError:
        raise
    except Exception as e:
        raise IOError(f"Error writing to output file '{out_path}': {e}")
