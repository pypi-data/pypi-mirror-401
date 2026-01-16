# gemstone/paths.py
import os
import logging
from typing import Iterator, Tuple, List
from pathlib import Path
import gemstone.dir as Dir
from gemstone.params import Params
from gemstone.specs import Specs, Spec
from gemstone.jobid import get_job_id
from gemstone.stageflows import Flows

class Paths:
	VIRTUAL_STAGE = "params"
	VIRTUAL_STAGE_OUTPUT_NAME = "INPUT"
	INPUT_SPEC_NAME = "INPUT"

	def __init__(self, stage_dir_name: str, jobid: str, flows: Flows):
		self._jobid = jobid
		self._stage_dir_name = stage_dir_name
		self._flows = flows

		self._src = Dir.root
		self._app_dir = Dir.stages
		self._stage_dir_path = os.path.join(self._app_dir, stage_dir_name)

		self._output_for_job = os.path.join(Dir.output, jobid)
		self._output_for_job_stage = os.path.join(self._output_for_job, stage_dir_name)
		self._runtime = os.path.join(self._stage_dir_path, "runtime")

		os.makedirs(self._output_for_job_stage, exist_ok=True)

	@property
	def jobid(self): return self._jobid

	@property
	def stage_dir_name(self): return self._stage_dir_name

	@property
	def src(self): return self._src

	@property
	def app_dir(self): return self._app_dir

	@property
	def stages(self): return self._app_dir

	@property
	def stage_dir_path(self): return self._stage_dir_path

	@property
	def output_for_job(self): return self._output_for_job

	@property
	def output_for_job_stage(self): return self._output_for_job_stage

	@property
	def runtime(self): return self._runtime

	@property
	def input_dir(self) -> str:
		d = os.path.join(self._output_for_job, "INPUT")
		os.makedirs(d, exist_ok=True)  # <--- Ensure directory
		return d

	def input_symlink_path(self, param_name: str, user_path: str = "") -> str:
		"""
		Returns the full symlink path. Symlink name does NOT encode the user's extension.
		"""
		# Always just INPUT/<param_name>
		return os.path.join(self.input_dir, param_name)

	def is_virtual_stage(self, stage: str) -> bool:
		return stage == self.VIRTUAL_STAGE

	def get_parameter_file_path(self, key: str = "") -> str:
		name = f"parameters_{key}.txt" if key else "parameters.txt"
		return os.path.join(self._output_for_job_stage, name)

	def get_stage_output_dir(self, stage_dir_name: str) -> str:
		return self._get_stage_output_dir(stage_dir_name)

	def _get_stage_output_dir(self, stage: str) -> str:
		subdir = self.VIRTUAL_STAGE_OUTPUT_NAME if self.is_virtual_stage(stage) else stage
		full_path = os.path.join(self._output_for_job, subdir)
		os.makedirs(full_path, exist_ok=True)
		return full_path

	def get_output_dir_for_overrides(self, iofile_name: str) -> str:
		return os.path.dirname(self.get_output_path(iofile_name, "sample"))

	def get_output_path(self, iofile_name: str, override: str = "") -> str:
		iofile = self._flows.get_output_iofile(self._stage_dir_name, iofile_name)
		ext = iofile.ext or ""  # default to empty string if None

		if override:
			filename = f"{override}.{ext}" if ext else override
			return os.path.join(self._output_for_job_stage, iofile_name, filename)
		else:
			filename = f"{iofile_name}.{ext}" if ext else iofile_name
			return os.path.join(self._output_for_job_stage, filename)

	def get_input_path(self, iofile_name: str, override: str = "") -> str:
		dest_stage = self._stage_dir_name
		source_stage, source_iofile = self._flows.get_source_for_input(dest_stage, iofile_name)

		# Start with whatever the flow specifies
		ext = source_iofile.ext or ""

		if self.is_virtual_stage(source_stage):
			# For virtual stages like "params", if the flow didn't specify an ext,
			# infer it from the INPUT symlink target.
			if not ext:
				# Symlink is named after the param (source_iofile.name), possibly with ext
				# Example: <output>/<job>/INPUT/<param_name>.csv
				symlink = os.path.join(self.input_dir, source_iofile.name)

				# Follow symlink to user-supplied file
				realpath = os.path.realpath(symlink)
				ext = os.path.splitext(realpath)[1].lstrip(".")

		# Now build the path in the source stage's output tree
		outdir = self._get_stage_output_dir(source_stage)
		return self._build_input_path(outdir, source_iofile.name, ext, override)

	def get_input_overrides(self, iofile_name: str) -> Iterator[Tuple[str, str]]:
		dest_stage = self._stage_dir_name
		source_stage, source_iofile = self._flows.get_source_for_input(dest_stage, iofile_name)
		ext = source_iofile.ext
		input_dir = Path(self._get_stage_output_dir(source_stage)) / source_iofile.name
		if not input_dir.exists():
			return
		for f in sorted(input_dir.glob(f"*.{ext}")):
			yield f.stem, str(f.resolve())

	def _build_input_path(self, outdir: str, iofile_name: str, ext: str, override: str) -> str:
		# Determine the base filename (with optional extension)
		if override:
			# Use the override value as the base name
			if ext:
				filename = f"{override}.{ext}"
			else:
				filename = override
			# Place inside a subdirectory named after the iofile_name
			return os.path.join(outdir, iofile_name, filename)
		else:
			# Use the iofile_name as the base name
			if ext:
				filename = f"{iofile_name}.{ext}"
			else:
				filename = iofile_name
			return os.path.join(outdir, filename)


	def outputs_are_present(self, iofile_names: List[str]) -> bool:
		return all(os.path.exists(self.get_output_path(name)) for name in iofile_names)
# end class

def is_input_supplied_by_upstream(spec: Spec, flows: Flows) -> bool:
	for stage in spec.source_modules:
		try:
			upstream_stage, _ = flows.get_source_for_input(stage, spec.key)
			if upstream_stage not in flows.VIRTUAL_STAGES:
				return True
		except ValueError:
			# No source listed; treat as not supplied
			pass
	return False

def make_symlink_safely(symlink_path: str, target_path: str):
	os.makedirs(os.path.dirname(symlink_path), exist_ok=True)


#    os.makedirs(os.path.dirname(symlink_path), exist_ok=True)
	if os.path.exists(symlink_path):
		os.remove(symlink_path)
	os.symlink(target_path, symlink_path)

def make_input_symlinks(params: Params, specs: Specs, flows: Flows):
	"""
	For all user-supplied inputs, unless created by an upstream stage, create symlinks in output/<jobid>/INPUT/<param_name>,
	and update the param value to point to the symlink path.
	"""
	job_id = get_job_id()
	for key, spec in specs.items():
		if not spec.is_input():
			continue

		if is_input_supplied_by_upstream(spec, flows):
			continue

		if not hasattr(params, key):
			raise ValueError(f"Missing required input param: {key}")

		user_param_path = getattr(params, key)
		if user_param_path is None:
			raise ValueError(f"Input param '{key}' is None")

		if not os.path.exists(user_param_path):
			raise FileNotFoundError(f"Input param '{key}' path does not exist: {user_param_path}")

		this_module = spec.source_modules[0]
		paths = Paths(this_module, job_id, flows)

		symlink_path = paths.input_symlink_path(key, user_param_path)

		target = os.path.abspath(user_param_path)

		make_symlink_safely(symlink_path, target)

		params.write(key, symlink_path)
		logging.info(f"Created INPUT symlink for '{key}' → {symlink_path}")

