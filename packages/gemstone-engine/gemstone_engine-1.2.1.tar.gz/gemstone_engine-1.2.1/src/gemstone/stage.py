import os
import logging
from importlib import import_module


class Stage:
    def __init__(self, name, directory):
        if not isinstance(name, str):
            raise ValueError("Stage 'name' must be a string.")
        if not isinstance(directory, str):
            raise ValueError("Stage 'directory' must be a string.")

        from gemstone import dir as Dir
        stage_path = os.path.join(Dir.stages, directory)

        if not os.path.exists(stage_path):
            raise FileNotFoundError(f"Stage directory '{stage_path}' does not exist.")

        self.name = name
        self.directory = directory

    def __repr__(self):
        return f"Stage({self.name}, dir={self.directory})"

    @staticmethod
    def is_valid_stage_name(name: str) -> bool:
        # Only allow a-z, A-Z, 0-9, _ and -
        import re
        return bool(re.fullmatch(r'[a-zA-Z0-9_-]+', name))

    def build_test_runner(self):
        from gemstone.iofile import parse_iofiles_txt
        from gemstone.stageflows import Flows
        from gemstone.paths import Paths
        import gemstone.dir as Dir

        def test_runner(params, paths):
            jobid = getattr(params, "jobid", "TESTJOB")
            flows = getattr(params, "flows", None) or Flows.parse()

            stage_name = self.name
            stage_dir = os.path.join(Dir.stages, stage_name)
            iofiles_path = os.path.join(stage_dir, "iofiles.txt")
            iofiles = parse_iofiles_txt(stage_name, iofiles_path)

            for f in iofiles:
                if f.direction == "in":
                    try:
                        input_path = paths.get_input_path(f.name)
                        if not os.path.exists(input_path):
                            logging.warning(f"[TEST MODE] Missing input: {f.name} → {input_path}")
                        else:
                            logging.info(f"[TEST MODE] Found input: {f.name} → {input_path}")
                    except Exception as e:
                        logging.warning(f"[TEST MODE] Could not resolve input '{f.name}': {e}")

            for f in iofiles:
                if f.direction == "out":
                    try:
                        output_path = paths.get_output_path(f.name)
                        os.makedirs(os.path.dirname(output_path), exist_ok=True)
                        with open(output_path, "a"):
                            pass
                        logging.info(f"[TEST MODE] Created fake output: {f.name} → {output_path}")
                    except Exception as e:
                        logging.error(f"[TEST MODE] Failed to create output '{f.name}': {e}")

            marker_path = os.path.join(paths.output_for_job_stage, "TEST_MODE.txt")
            with open(marker_path, "w") as f:
                f.write(
                    "This directory was created in TEST MODE.\n"
                    "No real computation was performed.\n"
                )
            logging.info(f"[TEST MODE] Created marker file: {marker_path}")

        return test_runner

    def load_run_function(self, test_mode=False):
        try:
            module = import_module(f"stages.{self.directory}.run")
            if test_mode:
                return self.build_test_runner()
            return module.run
        except (ModuleNotFoundError, AttributeError) as e:
            raise ImportError(f"Error loading run function for stage '{self.name}': {e}")
