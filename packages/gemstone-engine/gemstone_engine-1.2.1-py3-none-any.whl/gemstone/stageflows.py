# stageflows.py
import os
import re
import sys
import logging
from typing import Optional, Tuple, List, Dict

import gemstone.dir as Dir
from gemstone.generic_helpers import write_to_file, read_lines_strip_comments_numbered
from gemstone.iofile import parse_iofiles_txt, IOFile
from gemstone.stage import Stage
from gemstone.standards import Standards

import logging
logger = logging.getLogger(__name__)


class Flow:
	def __init__(self, source_stage: str, source_output: IOFile, dest_input: IOFile, dest_stage: str):
		self.source_stage = source_stage
		self.source_output = source_output  # IOFile
		self.dest_input = dest_input        # IOFile
		self.dest_stage = dest_stage

	def __repr__(self):
		return f"{self.source_stage}.{self.source_output.name} → {self.dest_stage}.{self.dest_input.name}"

class Flows:
	VIRTUAL_STAGES = {"params"}
	
	def __init__(self, flows: List[Flow], iofiles_by_stage: Dict[str, List[IOFile]]):
		self._flows = flows
		self._iofiles_by_stage = iofiles_by_stage

	def __iter__(self):
		return iter(self._flows)

	def __len__(self):
		return len(self._flows)

	@staticmethod
	def stageflows_file_exists(stageflows_path: str = "") -> bool:
		if not stageflows_path:
			stageflows_path = os.path.join(Dir.stages, "stageflows.txt")
		return os.path.isfile(stageflows_path)

	@classmethod
	def parse(cls, stageflows_path: Optional[str] = None, iofiles_by_stage: Optional[Dict[str, List[IOFile]]] = None) -> "Flows":
		if stageflows_path is None:
			stageflows_path = os.path.join(Dir.stages, "stageflows.txt")

		# Discover iofiles if not given
		if iofiles_by_stage is None:
			app_dir = Dir.stages
			stage_dirs = [d for d in os.listdir(app_dir)
						  if os.path.isdir(os.path.join(app_dir, d))]
			iofiles_by_stage = {}
			for stage in stage_dirs:
				iofile_path = os.path.join(app_dir, stage, "iofiles.txt")
				if os.path.isfile(iofile_path):
					iofiles_by_stage[stage] = parse_iofiles_txt(stage, iofile_path)

		# Parse flows.txt
		try:
			numbered_lines = read_lines_strip_comments_numbered(stageflows_path)
			flows = []
			flows_instance = cls([], iofiles_by_stage)
			for lineno, line in numbered_lines:
				try:
					flow = flows_instance._parse_line(line)
					flows.append(flow)
				except Exception as e:
					raise ValueError(f"Parse error at line {lineno} in stageflows.txt:\n  {line}\n→ {e}")
			return cls(flows, iofiles_by_stage)
		except Exception as e:
			raise RuntimeError(f"Failed to parse stageflows.txt at {stageflows_path} — {e}")

	def _parse_line(self, line: str) -> Flow:
		src, dst = [x.strip() for x in line.split(":")]
		src_stage, src_iofile_name = src.split(".")
		dst_stage, dst_iofile_name = dst.split(".")

		# Validate stage names early
		if not Stage.is_valid_stage_name(src_stage) and src_stage not in self.VIRTUAL_STAGES:
			raise RuntimeError(f"Invalid source stage name: '{src_stage}' in stageflows.txt")
		if not Stage.is_valid_stage_name(dst_stage):
			raise RuntimeError(f"Invalid destination stage name: '{dst_stage}' in stageflows.txt")

		# if "params" is the source
		if src_stage in self.VIRTUAL_STAGES:
			src_iofile = IOFile(
				name=src_iofile_name,
				ext="",              # unknown for params
				direction="out",     # treat as a "virtual output"
				standard="dummy",		 # not applicable for params ?
				stage=src_stage
			)
		else:
			try:
				src_iofile = next(f for f in self._iofiles_by_stage[src_stage]
								if f.name == src_iofile_name and f.direction == "out")
			except (KeyError, StopIteration):
				raise RuntimeError(f"Output '{src_iofile_name}' not found in stage '{src_stage}'")

		try:
			dst_iofile = next(f for f in self._iofiles_by_stage[dst_stage]
							if f.name == dst_iofile_name and f.direction == "in")
		except (KeyError, StopIteration):
			raise RuntimeError(f"Input '{dst_iofile_name}' not found in stage '{dst_stage}'")

		return Flow(src_stage, src_iofile, dst_iofile, dst_stage)

	def get_all_iofiles(self) -> List:
		"""Return all IOFile objects from all non-virtual stages in this flow."""
		return [
			f for stage, files in self._iofiles_by_stage.items()
			if stage not in self.VIRTUAL_STAGES
			for f in files
		]

	def get_iofiles(self, direction: str, stage: str) -> List[IOFile]:
		"""
		Return all IOFiles for the given direction ('in' or 'out') and stage.
		"""
		if stage not in self._iofiles_by_stage:
			raise ValueError(f"Stage '{stage}' not found in iofiles_by_stage.")
		return [f for f in self._iofiles_by_stage[stage] if f.direction == direction]

	def get_output_iofile(self, stage: str, name: str) -> IOFile:
		for f in self.get_iofiles("out", stage):
			if f.name == name:
				return f
		raise ValueError(f"Output iofile '{name}' not found in stage '{stage}'")

	def get_output_ext(self, stage: str, iofile_name: str) -> str:
		outputs = self.get_iofiles("out", stage)
		match = next((f for f in outputs if f.name == iofile_name), None)
		if not match:
			raise ValueError(f"IOFile '{iofile_name}' not found in source stage '{stage}'")
		return match.ext

	def get_source_for_input(self, dest_stage: str, dest_input_name: str) -> Tuple[str, IOFile]:
		"""
		Given a destination stage and input iofile name, return (source_stage, source_output: IOFile).
		"""
		for flow in self._flows:
			if flow.dest_stage == dest_stage and flow.dest_input.name == dest_input_name:
				return (flow.source_stage, flow.source_output)
		raise ValueError(f"No source found in stageflows.txt for input '{dest_input_name}' of stage '{dest_stage}'")


	def get_all_stage_dirs(self, root_abs_path) -> List:
		all_stages = {
			s for f in self._flows
			for s in (f.source_stage, f.dest_stage)
			if s not in self.VIRTUAL_STAGES
		}
		return [os.path.join(root_abs_path, "stages", stage) for stage in sorted(all_stages)]

	def validate_against_iofiles(self, verbose=True):
		"""Validate that all flows match declared inputs/outputs in iofiles_by_stage."""
		iofile_lookup = {
			(f.stage, f.name, f.direction): f
			for files in self._iofiles_by_stage.values()
			for f in files
		}
		used = set()
		issues = []
		notes = []

		for flow in self._flows:
			if flow.source_stage not in self.VIRTUAL_STAGES:
				key = (flow.source_stage, flow.source_output.name, "out")
				if key not in iofile_lookup:
					issues.append(f"{flow.source_stage} does not declare output '{flow.source_output.name}'")
				else:
					used.add(key)

			key = (flow.dest_stage, flow.dest_input.name, "in")
			if key not in iofile_lookup and flow.dest_stage not in self.VIRTUAL_STAGES:
				issues.append(f"{flow.dest_stage} does not declare input '{flow.dest_input.name}'")
			else:
				used.add(key)

		for files in self._iofiles_by_stage.values():
			for f in files:
				key = (f.stage, f.name, f.direction)
				if key not in used:
					if f.direction == "in":
						notes.append(f"{f.stage} input '{f.name}' has no source in stageflows.txt")
					# elif f.direction == "out":
					#	notes.append(f"{f.stage} output '{f.name}' has no destination in stageflows.txt")

		if issues or notes:
			with open("flows_report.txt", "w") as f:
				if issues:
					f.write("Flows:\n" + "\n".join(issues) + "\n\n")
				if notes:
					f.write("Stages (iofiles.txt):\n" + "\n".join(notes) + "\n")
			logger.warning("⚠️  Validation completed with issues. See flows_report.txt.")

	def validate_iofile_standards(self, standards_path: str):
		"""
		Cross-check each IOFile.standard against standards.txt.
		- Errors if a listed standard is undefined.
		- Warnings for missing or empty standards.
		"""
		if not os.path.exists(standards_path):
			logger.warning(f"No standards.txt found at {standards_path}; skipping standards validation.")
			return

		standards = Standards(standards_path)

		for stage, iofiles in self._iofiles_by_stage.items():
			for iofile in iofiles:
				std = iofile.standard.strip()
				if not std:
					logger.warning(f"{stage}/{iofile.name}: no standard specified.")
					continue

				if not standards.is_standard(std):
					raise ValueError(
						f"Undefined standard '{std}' in stage '{stage}' ({iofile.name}) "
						f"— must be listed in {os.path.basename(standards_path)}."
					)

		logger.info(f"Standards validation passed for {len(self._iofiles_by_stage)} stages.")

	def validate_flow_standards(self):
		"""
		Verify that connected flows use matching standards.

		Rules:
		- If both source and destination define a standard → must match (else error).
		- If either side is missing → warning.
		- Skip validation if source is a virtual stage (e.g., 'params').
		"""
		if not hasattr(self, "_flows") or not self._flows:
			logger.warning("No flows defined; skipping standard compatibility validation.")
			return

		for flow in self._flows:
			if flow.source_stage in self.VIRTUAL_STAGES:
				continue  # skip virtual sources like 'params'

			src = flow.source_output  # IOFile
			dst = flow.dest_input     # IOFile
			s_std = src.standard.strip()
			d_std = dst.standard.strip()

			if not s_std or not d_std:
				missing = []
				if not s_std:
					missing.append(f"{flow.source_stage}.{src.name}")
				if not d_std:
					missing.append(f"{flow.dest_stage}.{dst.name}")

				logger.warning(
					f"Flow {flow.source_stage}.{src.name} → {flow.dest_stage}.{dst.name}: "
					f"missing standard in {', '.join(missing)} "
					f"(src='{s_std or '∅'}', dst='{d_std or '∅'}')."
				)
				continue

			if s_std.lower() != d_std.lower():
				raise ValueError(
					f"Mismatched standards in flow {flow.source_stage}.{src.name} ('{s_std}') → "
					f"{flow.dest_stage}.{dst.name} ('{d_std}'). Files must use the same standard."
				)

		logger.info(f"Standards validation passed for {len(self._flows)} flows.")



	def to_run_blocks(self) -> List[List[str]]:
		"""
		Returns a list of run blocks. Each block is a list of stage names
		that can be run in parallel, based on dependency ordering.
		Virtual stages like 'params' are excluded from run blocks.
		"""
		from collections import defaultdict, deque

		# Dependency graph
		deps = defaultdict(set)    # stage -> prerequisite stages
		rdeps = defaultdict(set)   # stage -> dependent stages
		real_stages = set()

		for flow in self._flows:
			if flow.source_stage not in self.VIRTUAL_STAGES:
				deps[flow.dest_stage].add(flow.source_stage)
				rdeps[flow.source_stage].add(flow.dest_stage)
				real_stages.add(flow.source_stage)
			real_stages.add(flow.dest_stage)

		# Initialize in-degrees for topological sort
		in_degree = {stage: len(deps[stage]) for stage in real_stages if stage not in self.VIRTUAL_STAGES}

		# Kahn’s algorithm for topological sort with block grouping
		run_blocks = []
		ready = deque([s for s in in_degree if in_degree[s] == 0])

		while ready:
			block = sorted(list(ready))
			run_blocks.append(block)
			next_ready = deque()

			while ready:
				stage = ready.popleft()
				for dependent in rdeps[stage]:
					if dependent in in_degree:
						in_degree[dependent] -= 1
						if in_degree[dependent] == 0:
							next_ready.append(dependent)

			ready = next_ready

		if any(in_degree[s] > 0 for s in in_degree):
			raise RuntimeError("Cycle detected in stageflows dependencies")

		return run_blocks


def handle_missing_stageflows_file(stage_dirs: List):
	"""
	Check if stageflows.txt exists in Dir.stages. If not, draft and exit.
	"""
	stageflows_txt_path = os.path.join(Dir.stages, "stageflows.txt")

	if not os.path.exists(stageflows_txt_path):
		logging.error("stageflows.txt file missing. Creating draft from iofiles.txt in each stage.")
		try:
			flows_draft = draft_stageflows_txt_structure(stage_dirs)
			write_to_file(stageflows_txt_path, flows_draft)
			logging.error(f"Draft written to: {stageflows_txt_path}. Please edit to complete the flow specification.")
			sys.exit(98)
		except Exception as e:
			logging.error(f"Error creating stageflows.txt draft: {e}")
			sys.exit(1)

def draft_stageflows_txt_structure(stage_dirs_or_root) -> str:
    """Return a draft stageflows.txt with placeholder flows for each input/output."""
    # Resolve list of stage dirs
    if isinstance(stage_dirs_or_root, str):
        stage_dirs = [
            os.path.join(stage_dirs_or_root, d)
            for d in os.listdir(stage_dirs_or_root)
            if os.path.isdir(os.path.join(stage_dirs_or_root, d))
        ]
    else:
        stage_dirs = stage_dirs_or_root

    lines = [
        "# Draft stageflows.txt — connect outputs to inputs using 'stage.iofile : stage.iofile'",
        "# Example: scan.projections : recon.scan_input",
        ""
    ]

    for stage_dir in sorted(stage_dirs):
        stage_name = os.path.basename(stage_dir)
        iofiles_txt = os.path.join(stage_dir, "iofiles.txt")
        if not os.path.exists(iofiles_txt):
            continue

        iofiles = parse_iofiles_txt(stage_dir, iofiles_txt)

        for iofile in iofiles:
            if iofile.direction == "in":
                lines.append(f"??? : {stage_name}.{iofile.name}")
            elif iofile.direction == "out":
                lines.append(f"{stage_name}.{iofile.name} : ???")

        lines.append("")

    return "\n".join(lines)

