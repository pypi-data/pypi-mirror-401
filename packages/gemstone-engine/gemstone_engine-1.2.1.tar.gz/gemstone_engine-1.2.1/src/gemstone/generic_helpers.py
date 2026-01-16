# generic_helpers.py
import os
import logging
import sys
import subprocess
import re
import json
from pathlib import Path
import shutil
from typing import List, Tuple, Iterable, Union, Optional
from types import SimpleNamespace

# CHECKS
def exit_if_error(condition, error_message, err_num:int = 1):
	if condition:
		logging.error(error_message)
		sys.exit(err_num)

def exit_if_done(condition, done_message):
	if condition:
		logging.info(done_message)
		sys.exit(0)

def is_well_formed_path(path: str) -> bool:
	try:
		Path(path)  # If it can be parsed into a Path object, it's likely well-formed
		return True
	except Exception:
		return False

def check_directory_for_files(path, file_extension: str = "*", error_message: str = ""):
	"""Check if a directory exists and contains files with a specific extension or any files."""
	# Exit if directory doesn't exist
	exit_if_error(not os.path.isdir(path), error_message)

	# If extension is '*', match all files
	if file_extension == "*":
		files = [x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))]
	else:
		files = [x for x in os.listdir(path) if x.endswith(file_extension)]

	# Exit if no matched files
	exit_if_error( not files, error_message)

def check_directory_exists(path):
	return os.path.isdir(path)

def ensure_directory_exists(path):
	if not os.path.isdir(path):
		os.makedirs(path)

def err_if_file_not_exist(filepath, errmsg = None):
	if not errmsg:
		errmsg = f"File not found: {filepath}"
	if not os.path.exists(filepath):
		logging.debug(f"File not found: {filepath}")
		raise FileNotFoundError(errmsg)
	
def err_if_dir_not_exist(path_that_may_exist, errmsg = None):
	if not errmsg:
		errmsg = f"Directory not found: {path_that_may_exist}"
	if not os.path.exists(path_that_may_exist):
		logging.debug(f"Directory not found: {path_that_may_exist} - {errmsg}")
		raise NotADirectoryError(errmsg)    

def check_file_exists(filepath:str) -> bool:
	return os.path.exists(filepath)

def get_abs_dir_from_file(file_path: str) -> str:
	"""Returns the absolute directory path for a given file path."""
	return os.path.dirname(os.path.abspath(file_path))

def get_which_exe_path(exe_name: str) -> Optional[Path]:
    """Return absolute Path to the given executable name, or None if not found."""
    path = shutil.which(exe_name)
    return Path(path).resolve() if path else None

# READS
def read_file(file_path: str) -> str:
    """Reads the entire contents of a text file and returns it as a string."""
    err_if_file_not_exist(file_path)
    with open(file_path, "r") as f:
        return f.read()

def read_lines_strip_comments_numbered(file_path: str,
                                       comment_char: str = "#",
                                       strip_inline_comments: bool = True,
                                       strip_blank_lines: bool = True) -> List[Tuple[int, str]]:
    """
    Reads a text file and returns (lineno, cleaned_line) pairs,
    excluding full-line comments and optionally stripping inline comments and blank lines.
    """
    err_if_file_not_exist(file_path)
    return _read_and_clean_lines(file_path, numbered=True,
                                  comment_char=comment_char,
                                  strip_inline_comments=strip_inline_comments,
                                  strip_blank_lines=strip_blank_lines)

def read_lines_strip_comments(file_path: str,
                              comment_char: str = "#",
                              strip_inline_comments: bool = True,
                              strip_blank_lines: bool = True) -> List[str]:
    """
    Same as above, but returns only cleaned lines (no line numbers).
    """
    err_if_file_not_exist(file_path)
    return [
        line for _, line in _read_and_clean_lines(file_path, numbered=True,
                                                  comment_char=comment_char,
                                                  strip_inline_comments=strip_inline_comments,
                                                  strip_blank_lines=strip_blank_lines)
    ]

def _read_and_clean_lines(file_path: str,
                          numbered: bool,
                          comment_char: str,
                          strip_inline_comments: bool,
                          strip_blank_lines: bool) -> List[Tuple[int, str]]:
    cleaned = []
    with open(file_path, "r") as f:
        for lineno, raw_line in enumerate(f, start=1):
            line = raw_line.rstrip("\n")

            if line.strip().startswith(comment_char):
                continue
            if strip_inline_comments and comment_char in line:
                line = line.split(comment_char, 1)[0].rstrip()
            if strip_blank_lines and not line.strip():
                continue

            cleaned.append((lineno, line.rstrip()) if numbered else line.rstrip())
    return cleaned


# TRANSFORMS
def shorten_path(long_path: str, root_to_truncate) -> str:
	"""Replace absolute path prefix with './' relative to project root."""
	try:
		rel = Path(long_path).resolve().relative_to(root_to_truncate)
		return f"./{rel}"
	except ValueError:
		return long_path  # return as-is if outside project

def parse_string_to_list(string_to_parse, delimiters_list):
	""" Parses a string into a list using the first matching delimiter in delimiters_list, or raises ValueError if none found."""
	for delimiter in delimiters_list:
		if delimiter in string_to_parse:
			return [item.strip() for item in string_to_parse.split(delimiter)]
	raise ValueError(f"No valid delimiter found in: {string_to_parse}")

def parse_string_to_range(string_to_parse: str):
	"""
	Parses a string into a range (min, max) or raises an error for invalid formatting.

	Args:
		string_to_parse (str): The string to parse.

	Returns:
		Tuple: (min, max) as floats.

	Raises:
		ValueError: If the range string is malformed.
	"""
	string_to_parse = string_to_parse.strip()

	# Check if the first character indicates a negative number
	if string_to_parse.startswith("-"):
		parts = string_to_parse.split(",", 1)
		if len(parts) == 2:  # Comma-delimited min, max
			try:
				min_val, max_val = map(float, parts)
				return min_val, max_val
			except ValueError:
				raise ValueError(f"Malformed range: {string_to_parse}")
		else:
			# Further split by space or dash
			tokens = string_to_parse.split()
			if len(tokens) == 3 and tokens[1] == "-":
				try:
					min_val, max_val = float(tokens[0]), float(tokens[2])
					return min_val, max_val
				except ValueError:
					raise ValueError(f"Malformed range: {string_to_parse}")
			elif len(tokens) == 2:  # Space-separated min and max
				try:
					min_val, max_val = map(float, tokens)
					return min_val, max_val
				except ValueError:
					raise ValueError(f"Malformed range: {string_to_parse}")
			elif len(tokens) == 1:  # Single token, split by dash
				try:
					min_val, max_val = map(float, tokens[0].split("-", 1))
					return min_val, max_val
				except ValueError:
					raise ValueError(f"Malformed range: {string_to_parse}")
			else:
				raise ValueError(f"Malformed range: {string_to_parse}")
	else:
		# For non-negative ranges, delegate to parse_string_to_list
		delimiters = ["-", ",", " "]
		tokens = parse_string_to_list(string_to_parse, delimiters)
		if len(tokens) == 2:
			try:
				min_val, max_val = map(float, tokens)
				return min_val, max_val
			except ValueError:
				raise ValueError(f"Malformed range: {string_to_parse}")
		else:
			raise ValueError(f"Malformed range: {string_to_parse}")

def get_namespace_from_path(path: str, keys: Iterable[str]) -> SimpleNamespace:
	"""
	Map path components to keys (right-aligned) and return as attributes.

	Example:
		>>> path = "/data/project1/set5/file.txt"
		>>> keys = ["project", "set", "file"]
		>>> ns = get_namespace_from_path(path, keys)
		>>> ns.project  # 'project1'
		>>> ns.set      # 'set5'
		>>> ns.file     # 'file.txt'
	"""
	parts = list(Path(path).parts)
	keys = list(keys)

	if len(parts) < len(keys):
		raise ValueError(f"Path has only {len(parts)} parts but {len(keys)} keys were provided.")

	mapping = dict(zip(keys, parts[-len(keys):]))
	return SimpleNamespace(**mapping)

def get_path_from_namespace(ns: Union[SimpleNamespace, dict], keys: Iterable[str]) -> str:
	"""
	Construct path from namespace or dict, using keys in order.

	Example:
		>>> ns = SimpleNamespace(scanner="w12", batch="b3", file="phantomA.raw")
		>>> keys = ["scanner", "batch", "file"]
		>>> get_path_from_namespace(ns, keys)
		'w12/b3/phantomA.raw'
	"""
	d = ns.__dict__ if isinstance(ns, SimpleNamespace) else ns
	return str(Path(*[d[k] for k in keys]))

def replace_extension(path: str, new_ext: str) -> str:
	"""
	Replace the file extension of a given path. `new_ext` may include or omit leading dot.

	Example:
		>>> replace_extension("phantomA.raw", "bin")
		'phantomA.bin'
	"""
	new_ext = new_ext if new_ext.startswith('.') else '.' + new_ext
	return str(Path(path).with_suffix(new_ext))


# EDITS
def update_setting(file_path: str, key: str, new_value: str, delimiter: str, add_if_missing=False):
	"""Update a key-value setting in a file or append it if missing (optional).

	Args:
		file_path (str): Path to the settings file.
		key (str): The setting key to update or add.
		new_value (str): The new value to set.
		delimiter (str): The delimiter between key and value.
		add_if_missing (bool): Whether to append the key if not found. Default is False.

	Raises:
		KeyError: If the key is not found and add_if_missing is False.
		IOError: If file write fails.
	"""
	updated_lines = []
	found = False

	pattern = re.compile(rf"^(\s*{re.escape(key)}\s*{re.escape(delimiter)}\s*)([^\s#]+)(.*)$")

	try:
		with open(file_path, "r") as f:
			lines = f.readlines()
	except Exception as e:
		raise IOError(f"Failed to read {file_path}: {e}")

	for line in lines:
		match = pattern.match(line)
		if match:
			found = True
			prefix, _, suffix = match.groups()
			updated_line = f"{prefix}{new_value}{suffix}\n"
			updated_lines.append(updated_line)
		else:
			updated_lines.append(line)

	if not found:
		if add_if_missing:
			updated_lines.append(f"{key} {delimiter} {new_value}\n")
		else:
			raise KeyError(f"Key '{key}' not found in {file_path}")

	try:
		with open(file_path, "w") as f:
			f.writelines(updated_lines)
	except Exception as e:
		raise IOError(f"Failed to write to {file_path}: {e}")

def update_settings(path, updates_dict, keymap=None, delimiter='='):
	"""Update multiple keys in an existing file.

	Args:
		path (str): File to update.
		updates_dict (dict): Internal key → value.
		keymap (dict): Optional internal → external key mapping.
		delimiter (str): Key-value delimiter.
	"""
	for key, value in updates_dict.items():
		external_key = keymap[key] if keymap and key in keymap else key
		update_setting(path, external_key, str(value), delimiter, add_if_missing=True)

def write_dict_to_file(dict_to_write, output_path, keymap=None, delimiter='='):
	"""Write a dictionary of key-value pairs to a file.

	Args:
		dict_to_write (dict): Dictionary of keys and values to write.
		path (str): Output file path.
		keymap (dict, optional): Change key name in dict_to_write to another key name for the output file
		delimiter (str): Delimiter between key and value.
	"""
	try:
		with open(output_path, "w") as f:
			for key, val in dict_to_write.items():
				k = keymap[key] if keymap and key in keymap else key
				f.write(f"{k}{delimiter}{val}\n")
	except Exception as e:
		raise IOError(f"Failed to write to {output_path}: {e}")

# ACTIONS
def add_to_syspath(dir_path: str):
    abs_path = os.path.abspath(dir_path)
    if abs_path not in sys.path:
        sys.path.insert(0, abs_path)

def delete_directory(path):
	os.system(f'rm -r {path}')

def copy_file(src: str, dest: str) -> None:
	"""Copies a file to a new location, skipping if src and dest are the same."""
	if os.path.abspath(src) != os.path.abspath(dest):
		shutil.copy(src, dest)

def move_file_or_dir(src: str, dest: str) -> None:
	try:
		os.makedirs(os.path.dirname(dest), exist_ok=True)
		shutil.move(src, dest)
	except shutil.Error as e:
		logging.warning(f"Move failed: {e}")

def shlep_contents(src_dir: str, dest_dir: str):
	"""Move all contents of src_dir into dest_dir."""
	for name in os.listdir(src_dir):
		shutil.move(os.path.join(src_dir, name), os.path.join(dest_dir, name))

def _write(path: str, content: str, mode: str):
	try:
		with open(path, mode) as f:
			f.write(f"{content}\n")
	except OSError as e:
		print(f"Error writing to {path}: {e}")

def write_to_file(path: str, content: str):
	"""Overwrites file with content, creating parent directory if needed."""
	Path(path).parent.mkdir(parents=True, exist_ok=True)
	_write(path, content, "w")

def append_to_file(path: str, content: str):
	"""Appends content to file on a new line."""
	_write(path, content, "a")

def write_json(output_path: str, data: dict, indent: int = 4):
	"""Write a dictionary to a JSON file, ensuring parent directories exist."""
	os.makedirs(os.path.dirname(output_path), exist_ok=True)
	with open(output_path, 'w') as f:
		json.dump(data, f, indent=indent)

def run_process(command_args: str, description: str, env=None):
	try:
		logging.info(f"Starting: {description}")
		subprocess.run(command_args, check=True, env=env)
		logging.info(f"Completed: {description}")
	except subprocess.CalledProcessError as e:
		exit_if_error(True, f"{description} failed with error: {e}")

def run_subprocess_with_logging(
	cmd,
	label="process",
	logger=None,
	check=True,
	return_output=False
):
	"""Run a subprocess with live logging, streaming stdout/stderr, and optional output capture."""
	logger = logger or logging.getLogger(__name__)
	logger.info(f"Running {label} with command: {cmd}")

	process = None  # <- this line prevents UnboundLocalError

	try:
		process = subprocess.Popen(
			cmd,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			text=True,
			bufsize=1,
			universal_newlines=True,
		)

		stdout_lines = []
		stderr_lines = []

		while True:
			stdout_line = process.stdout.readline()
			stderr_line = process.stderr.readline()

			if stdout_line:
				stdout_lines.append(stdout_line)
				logger.info(f"{label} stdout: {stdout_line.rstrip()}")

			if stderr_line:
				stderr_lines.append(stderr_line)
				logger.warning(f"{label} stderr: {stderr_line.rstrip()}")

			if not stdout_line and not stderr_line and process.poll() is not None:
				break

		process.wait()

		if check and process.returncode != 0:
			logger.error(f"{label} failed with return code {process.returncode}")
			raise RuntimeError(f"{label} failed with return code {process.returncode}")

		logger.info(f"{label} completed.")

		if return_output:
			return ''.join(stdout_lines), ''.join(stderr_lines)

	except Exception as e:
		logger.error(f"Unexpected error in {label}: {str(e)}")
		raise RuntimeError(f"{label} encountered an unexpected error") from e

	finally:
		if process:
			if process.stdout:
				process.stdout.close()
			if process.stderr:
				process.stderr.close()


def run_matlab_script(matlab_executable_path: str, matlab_script_path: str):
	"""
	Runs the MATLAB function.
	
	Args:
		matlab_executable_path (str): The path to the MATLAB executable.
		matlab_script_path (str): The path to the MATLAB script file.
	"""
	# Ensure MATLAB can find the script and the .mat file
	matlab_command = f"\"{matlab_executable_path}\" -batch \"run('{matlab_script_path}')\""
	try:
		subprocess.run(matlab_command, check=True, shell=True)
		logging.info("Main executed successfully with params from dictionary.")
	except subprocess.CalledProcessError as e:
		logging.error(f"Execution of Main failed: {e}")

def load_module_from_file(path: str):
	"""Dynamically load a Python module from a file path, unregistered."""
	import importlib.util

	spec = importlib.util.spec_from_file_location("logicalname", path)
	if spec is None or spec.loader is None:
		raise ImportError(f"Could not load spec from {path}")
	mod = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(mod)
	return mod

def import_from_subdir(subdir_absolute_path, module_name, function_name):
    """
    Import a module or specific function from a given subdirectory.
    """
    module_path = os.path.join(subdir_absolute_path, f"{module_name}.py")
    if not os.path.exists(module_path):
        raise FileNotFoundError(f"Module file not found: {module_path}")

    mod = load_module_from_file(module_path)

    if function_name:
        if not hasattr(mod, function_name):
            raise AttributeError(
                f"Function '{function_name}' not found in module '{module_name}' at {module_path}"
            )
        return getattr(mod, function_name)
    else:
        raise ValueError(
            f"'function_name' is required but was not provided in call to import_from_subdir({subdir_absolute_path}, {module_name}, function_name)"
        )

