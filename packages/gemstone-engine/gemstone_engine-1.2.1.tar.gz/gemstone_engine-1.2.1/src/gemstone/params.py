import logging
import inspect
import os
import sys
from gemstone.generic_helpers import err_if_file_not_exist
from gemstone.specs import Specs, Spec, write_param_template_file
from typing import Tuple

def clean_line(line: str) -> str:
	"""Cleans a line by stripping whitespace and removing comments, returning an empty string if blank or a comment."""
	return line.split('#', 1)[0].strip()

def parse_line(line: str, strict_mode=True) -> Tuple:
	"""Parses a line into a (key, value) pair, raising ValueError if invalid in strict_mode, else returning None."""
	parts = line.split(':', 1)
	if len(parts) != 2 or not parts[0].strip() or not parts[1].strip():
		if strict_mode:
			logging.error(f"Malformed line: '{line}'")
			raise ValueError(f"Invalid param: '{line}'")
		else:
			logging.warning(f"Ignoring malformed line: '{line}'")
			return None, None

	return parts[0].strip(), parts[1].strip()

def read_lines_with_includes(filepath: str) -> list:
	"""Expands #include directives in a file and returns all lines."""
	logging.debug(f"*** Reading lines from: {filepath}")

	# Check if the current file exists
	err_if_file_not_exist(filepath)

	lines = []
	base_dir = os.path.dirname(filepath)  # Base directory for relative paths

	with open(filepath, 'r') as f:
		for line in f:
			line = line.strip()
			if line.startswith('#include'):
				included_file = line.split('#include', 1)[1].strip()

				# Attempt to resolve the included file
				candidate_paths = [
					os.path.join(base_dir, included_file),  # Relative to the current file
					included_file                          # Relative to current working dir
				]

				for path in candidate_paths:
					if os.path.exists(path):
						logging.debug(f"*** Including file: {path}")
						err_if_file_not_exist(path)
						lines.extend(read_lines_with_includes(path))
						break
				else:
					# If no valid path found
					raise FileNotFoundError(f"Included file not found: {included_file}")

			else:
				lines.append(line)
	return lines

def parse_param_file(filepath: str, strict_mode=True) -> dict:
	"""Parses a param file into a dictionary, raising errors or skipping malformed lines based on strict_mode."""
	params_dict = {}
	lines = read_lines_with_includes(filepath)

	for line in lines:
		try:
			cleaned_line = clean_line(line)
			if not cleaned_line:
				continue

			key, value = parse_line(cleaned_line, strict_mode)
			if key and value:
				params_dict[key] = value
		except ValueError as e:
			if strict_mode:
				raise
			else:
				logging.warning(f"Skipping line due to error: {e}")

	return params_dict

def validate_params(params_dict: dict, specs: Specs, param_file_path: str) -> dict:
	"""Validates params based on their specifications and returns validated params."""
	return {
		key: validate_single_param(key, params_dict.get(key, spec.default), spec, param_file_path)
		for key, spec in specs.items()
	}

def validate_single_param(key, value, spec: Spec, filepath):
	if spec.required and value is None and not spec.is_input():
		raise ValueError(f"Missing required param: '{key}', in file {filepath}, for stage {spec.source_modules}")
	
	if value is not None:
		# --- Type coercion ---
		try:
			if spec.type == Spec.INT:
				value = int(value)
			elif spec.type == Spec.FLOAT:
				value = float(value)
			elif spec.type in {Spec.PATH, Spec.FILE}:
				value = value.strip()
		except Exception as e:
			raise ValueError(f"param {key} must be of type {spec.type}, in file {filepath}. Error: {e}")

		# --- Constraint validation ---
		if spec.constraint_type == Spec.OPTIONS:
			if value not in spec.options:
				raise ValueError(f"Invalid option for {key}: {value}, in file {filepath}")

		if spec.constraint_type == Spec.RANGE:
			try:
				fval = float(value)
			except (TypeError, ValueError):
				raise ValueError(f"Value for {key} must be a number, in file {filepath}")

			min_ok = spec.range_min is None or fval >= spec.range_min
			max_ok = spec.range_max is None or fval <= spec.range_max
			if not (min_ok and max_ok):
				raise ValueError(
					f"Value for {key} must be in range ({spec.range_min}-{spec.range_max}), in file {filepath}"
				)

		if spec.type == Spec.PATH:
			if spec.constraint_type == Spec.MUST_EXIST and not os.path.exists(str(value)):
				raise ValueError(f"Path {value} does not exist for param: {key}, in file {filepath}")
			elif spec.constraint_type == Spec.CREATE and not os.path.exists(str(value)):
				os.makedirs(str(value), exist_ok=True)

		if spec.type == Spec.FILE:
			if spec.constraint_type == Spec.MUST_EXIST and not os.path.isfile(str(value)):
				raise FileNotFoundError(f"File {value} does not exist for param: {key}, in file {filepath}")
			elif spec.constraint_type == Spec.CREATE and not os.path.isfile(str(value)):
				open(str(value), 'w').close()

	return value

class Params:
	"""
	Stores parameter values, controls write access.
	
	- Only parameters declared 'writable' in specs.txt can be modified.
	- Writable params are initialized the same way as any other param.
	- Supports both attribute-style (params.key) and dictionary-style (params["key"]) access.
	"""
   
	def __init__(self, param_file_path: str, specs: Specs):
		self._param_file_path = param_file_path  # 🔹 Store for debugging
		self._specs = specs  # ✅ Needed for is_input checks
		params_dict = parse_param_file(param_file_path)
		self._params = validate_params(params_dict, specs, param_file_path)
		self._writable_keys = {k for k, spec in specs.items() if spec.writable}  # ✅ Fast lookups

	def read(self, key, defaultvalue=None):
		"""
		Reads the value of a parameter.
		
		- If key exists, returns its value.
		- If key does not exist, raises a KeyError.
		- If the value is blank (None), returns the provided defaultvalue.
		"""
		if key in self._params:
			return self._params[key] if self._params[key] is not None else defaultvalue
		raise KeyError(
			f"Attempted to read non-existent param named '{key}' in file '{self._param_file_path}'"
		)
	

	def write(self, key, value):
		"""Writes a value to a writable or INPUT parameter, enforcing type safety and logging changes."""
		spec = self._specs[key]
		if key not in self._writable_keys and not (spec and spec.is_input()):
			raise PermissionError(f"Cannot modify '{key}', not writable and not INPUT")

		expected_type = type(self._params[key])
		if not isinstance(value, expected_type):
			raise TypeError(
				f"Type mismatch: Attempted to write '{value}' ({type(value).__name__}) to param '{key}' of type '{expected_type.__name__}'"
			)

		self._params[key] = value
		self._log_write(key, value)

	def _log_write(self, key, value):
		"""
		Logs a write operation with the calling module name.
		"""
		caller = inspect.stack()[1].filename
		logging.debug(f"{caller} wrote to writable param '{key}': {value}")

	def __getattr__(self, key):
		"""
		Enables attribute-style access (params.key).
		"""
		if key.startswith("_"):
			return super().__getattribute__(key)
		try:
			return self.read(key)
		except KeyError:
			raise AttributeError(f"'Params' object has no attribute '{key}'")

	def __getitem__(self, key):
		"""
		Enables dictionary-style access (params["key"]).
		"""
		return self.read(key)

	def __setattr__(self, key, value):
		"""
		Prevents direct attribute modification, enforcing use of write().
		"""
		if key in {"_params", "_writable_keys", "_specs", "_param_file_path"}:
			super().__setattr__(key, value)
		else:
			self.write(key, value)

	def __setitem__(self, key, value):
		"""
		Prevents dictionary-style modification, enforcing use of write().
		"""
		self.write(key, value)

	def __iter__(self):
		return iter(self._params)

	def keys(self):
		return self._params.keys()

	def items(self):
		return self._params.items()

	def values(self):
		return self._params.values()

	def get(self, key, default=None):
		if key not in self._params:
			return default
		return self.read(key, default)
	
	def copy(self):
		"""Returns a copy of the parameter dictionary."""
		return self._params.copy()  # Shallow copy of stored params

def handle_missing_param_file(param_file_path, stage_dirs: list) -> None:
	"""
	Check if the param file exists. If not, create a template and raise an error.
	"""
	if not param_file_path or not os.path.exists(param_file_path):
		# Define default output path for the template
		default_template_path = "params_template.txt"
		output_path = param_file_path if param_file_path else default_template_path
		
		try:
			# Write the parameter template file
			write_param_template_file(stage_dirs, output_path)

			# lLog and exit gracefully
			logging.error(
				f"No param file found. A template has been written to: {output_path}. "
				"Please use or copy the template to provide a valid param file."
			)
			sys.exit(99)
		except Exception as e:
			# Raise a runtime error for unexpected issues
			logging.error(f"Error creating param template: {e}")
			sys.exit(1)
