import os
import sys
import time
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from typing import List

from gemstone.specs import Specs
from gemstone.params import Params, handle_missing_param_file
from gemstone.stageflows import Flows, handle_missing_stageflows_file
from gemstone.jobid import set_job_id, get_job_id
from gemstone.paths import Paths, make_input_symlinks # stage-specific
import gemstone.dir as Dir  # global

def make_python38_init_files():
    """Create __init__.py in each stage's runtime dir if using Python < 3.10."""
    if sys.version_info >= (3, 10):
        return

    stages_dir = Path("stages")
    for stage_dir in stages_dir.iterdir():
        runtime_dir = stage_dir / "runtime"
        if runtime_dir.is_dir():
            init_file = runtime_dir / "__init__.py"
            if not init_file.exists():
                init_file.touch()

def load_run_function(stage: str, test_mode: bool = False):
    """Dynamically load the run() function from the given stage's run.py."""
    import importlib
    try:
        mod = importlib.import_module(f"stages.{stage}.run")
        if test_mode:
            from gemstone.stage import Stage
            stage_obj = Stage(name=stage, directory=stage)
            return stage_obj.build_test_runner()
        return mod.run
    except Exception as e:
        raise ImportError(f"Could not load run() for stage '{stage}': {e}")

def handle_missing_stageflows_file_fallback():
    """
    Try to generate a draft stageflows.txt if missing.
    """
    if not Flows.stageflows_file_exists():        
        stage_dirs = [
            os.path.join(Dir.stages, d)
            for d in os.listdir(Dir.stages)
            if os.path.isdir(os.path.join(Dir.stages, d))
        ]
        handle_missing_stageflows_file(stage_dirs)
   
def run_pipeline(param_file_path, jobid_override=None, test_mode=False):
    """Main entry point."""
    make_python38_init_files()

    # --- Initialize Job ID
    set_job_id(jobid_override)
    job_id = get_job_id()
    logging.info(f"STARTING job {job_id}...")
    job_start = time.time()
    
    # --- Ensure configuration files exist
    handle_missing_stageflows_file_fallback()

    # --- Parse flows and determine involved stages
    flows = Flows.parse()
    stage_dirs = flows.get_all_stage_dirs(Dir.root)

    # --- Ensure params file exists
    handle_missing_param_file(param_file_path, stage_dirs)

    # --- Parse and validate configuration files
    specs = read_all_specs(stage_dirs)
    params = Params(param_file_path, specs)


    # --- Validate job structure
    flows.validate_against_iofiles()
    flows.validate_iofile_standards(os.path.join(Dir.stages, "standards.txt"))  # new step
    flows.validate_flow_standards()

    # --- Prepare inputs
    make_input_symlinks(params, specs, flows)
    # --- Execute stages
    run_blocks = flows.to_run_blocks()
    run_run_blocks(run_blocks, params, flows, job_id, test_mode=test_mode)

    # --- Wrap up
    elapsed = time.time() - job_start
    logging.info(f"COMPLETED job {job_id} in {format_elapsed(elapsed)}.")



def read_all_specs(stage_dirs: List) -> Specs:
    """Collect, validate, and coalesce specs from specs.txt files in the given stage directories."""
    all_specs = Specs()  # Create a Specs instance to hold all validated specs

    for stage_dir in stage_dirs:
        specs_file = os.path.join(stage_dir, "specs.txt")
        if not os.path.exists(specs_file):
            logging.warning(f"No specs file found in: {stage_dir}. Skipping.")
            continue  # Skip directories without a specs file

        logging.debug(f"Reading specs from: {specs_file}")
        stage_specs = Specs()
        stage_specs.load_from_file(specs_file)  # Load and validate specs from the file

        for key, spec in stage_specs.specs.items():
            if key in all_specs.specs:
                existing_spec = all_specs.specs[key]

                # Handle shared keys
                if spec.shared and existing_spec.shared:
                    if spec != existing_spec:
                        raise ValueError(
                            f"Conflicting attributes for shared spec key '{key}'. "
                            f"Existing: {existing_spec}, New: {spec}"
                        )
                else:
                    raise ValueError(
                        f"Duplicate spec key '{key}' found in stage '{stage_dir}' during coalescing without 'shared' attribute."
                    )
            all_specs.specs[key] = spec  # Add or update the spec in the master dictionary

    logging.debug(f"Coalesced specs: {all_specs.specs}")
    return all_specs
        

def format_elapsed(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{int(h)}:{int(m):02}:{s:05.2f}" if h else f"{int(m)}:{s:05.2f}"


def get_run_function(stage: str, paths: Paths, test_mode: bool = False):
    """
    Loads the run function for a stage, optionally wrapping it in test_mode.
    """
    if test_mode:
        from gemstone.stage import Stage
        stage_obj = Stage(name=stage, directory=stage)
        test_runner = stage_obj.build_test_runner()
        return lambda params, paths: test_runner(params, paths)

    from gemstone.generic_helpers import import_from_subdir
    return import_from_subdir(paths.stage_dir_path, "run", "run")


def run_run_blocks(run_blocks: List[List[str]], params: Params, flows: Flows, jobid: str, test_mode: bool = False):
    """Run the job stages based on dependency-ordered run blocks."""
    STAGE_PAD = 12  # width for aligned stage names

    for block in run_blocks:
        if len(block) == 1:
            # -------- single-stage block --------
            stage = block[0]
            logging.info(f"{stage:<{STAGE_PAD}} Starting")

            start = time.time()
            paths = Paths(stage, jobid=jobid, flows=flows)
            run_fn = get_run_function(stage, paths, test_mode)

            run_fn(params, paths)

            elapsed = time.time() - start
            logging.info(f"{stage:<{STAGE_PAD}} Finished in {format_elapsed(elapsed)}")

        else:
            # -------- parallel block --------
            logging.info(f"Parallel      Starting {len(block)} stages")

            with ThreadPoolExecutor() as executor:
                futures = {}
                for stage in block:
                    paths = Paths(stage, jobid=jobid, flows=flows)
                    run_fn = get_run_function(stage, paths, test_mode)

                    start = time.time()
                    future = executor.submit(run_fn, params, paths)
                    futures[future] = (stage, start)

                for future, (stage, start) in futures.items():
                    try:
                        future.result()
                        elapsed = time.time() - start
                        logging.info(f"{stage:<{STAGE_PAD}} Finished in {format_elapsed(elapsed)}")
                    except Exception as e:
                        logging.error(f"{stage:<{STAGE_PAD}} FAILED: {e}")
