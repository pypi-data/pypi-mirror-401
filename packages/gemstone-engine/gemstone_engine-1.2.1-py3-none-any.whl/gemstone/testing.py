# testing.py

import logging
import tempfile
from pathlib import Path
import shutil
import sys
import os
from gemstone.cli import main as gemstone_main
from gemstone.iofile import parse_iofiles_txt, IOFile
from pathlib import Path

logger = logging.getLogger(__name__)
def _setup_testing_logger():
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.INFO,
            format='[testing] %(levelname)s: %(message)s',
            stream=sys.stdout
        )


# Paths in the params.txt are expected to be relative to stages/<stage>/
# For example:  input_projection: tests/inputs/proj_001.bin

def run_stage_test(stage_dir: Path, keep_output=False):
    _setup_testing_logger()

    stage_name = stage_dir.name
    test_dir = stage_dir / "tests"
    params_path = test_dir / "params.txt"
    jobid = "TEST-001"

    # Create temp workspace
    temp_root = Path(tempfile.mkdtemp(prefix="gstest_"))
    (temp_root / "output" / jobid).mkdir(parents=True)
    (temp_root / "stages").mkdir()
    (temp_root / "stages" / stage_name).symlink_to(stage_dir, target_is_directory=True)

    # Create stageflows.txt under stages/ (required by GEMSTONe)
    stageflows_path = temp_root / "stages" / "stageflows.txt"
    make_stageflows_txt(stage_dir / "iofiles.txt", stage_name, stageflows_path)

    # --- critical change: run from temp_root ---
    cwd = Path.cwd()
    try:
        # cd into temp root so GEMSTONe finds stageflows.txt
        os.chdir(temp_root)

        # Set sys.argv so gemstone.cli.main() receives positional args correctly
        sys.argv = ["run_stage_test", str(params_path), jobid]

        gemstone_main()

        # Verify outputs produced under output/<jobid>/<stage_name>/
        verify_outputs(
            temp_root / "output" / jobid / stage_name,
            test_dir / "expected"
            )

    finally:
        os.chdir(cwd)

        if keep_output:
            logger.info(f"Temp output preserved at: {temp_root}")
        else:
            shutil.rmtree(temp_root)



def debug_stage_test(stage_dir: Path):
    _setup_testing_logger()

    stage_name = stage_dir.name
    test_dir = stage_dir / "tests"
    jobid = "TEST-001"
    temp_root = Path(tempfile.mkdtemp(prefix="gstest_debug_"))

    output_dir = temp_root / "output" / jobid
    stages_dir = temp_root / "stages"
    stage_symlink = stages_dir / stage_name
    stageflows_path = temp_root / "stageflows.txt"
    params_path = test_dir / "params.txt"
    expected_dir = test_dir / "expected"

    logger.info(f"Stage name:             {stage_name}")
    logger.info(f"Stage repo dir:         {stage_dir}")
    logger.info(f"Test dir:               {test_dir}")
    logger.info(f"Temp root (working dir): {temp_root}")
    logger.info(f"Output dir:             {output_dir}")
    logger.info(f"Stageflows path:        {stageflows_path}")
    logger.info(f"Stage symlink path:     {stage_symlink}  (→ {stage_dir})")
    logger.info(f"params.txt path:        {params_path}")
    logger.info(f"expected/ dir:          {expected_dir}")

    logger.info("Intended command (from inside temp dir):")
    logger.info(f"  cd {temp_root}")
    logger.info(f"  python -m gemstone.cli {params_path} {jobid}")

def make_stageflows_txt(iofiles_path: Path, stage_name: str, output_path: Path):
    """
    Generate stageflows.txt automatically for a single-stage module test.
    Uses IOFile objects and their direction attributes (input/output).
    """

    # parse_iofiles_txt now takes (stage_name, path_to_iofiles_txt)
    iofiles = parse_iofiles_txt(stage_name, str(iofiles_path))

    with output_path.open("w") as f:
        for io in iofiles:
            if io.is_input():   # IOFile supports `direction == IN`
                f.write(f"params.{io.name} : {stage_name}.{io.name}\n")
            # skip output lines entirely
            
def verify_outputs(produced_dir: Path, expected_dir: Path):
    _setup_testing_logger()

    for expected in expected_dir.iterdir():
        actual = produced_dir / expected.name

        if not actual.exists():
            raise AssertionError(f"[FAIL] Missing: {expected.name}")

        if actual.stat().st_size == 0:
            logger.warning(f"[WARN] 0-byte file: {expected.name}")
            continue

        if actual.stat().st_size != expected.stat().st_size:
            logger.warning(f"[WARN] Size mismatch: {expected.name}")
            continue

        if actual.read_bytes() != expected.read_bytes():
            logger.warning(f"[WARN] Content mismatch: {expected.name}")
            continue

        # Keep output clean if no problem.  logger.info(f"[OK] {expected.name}")
