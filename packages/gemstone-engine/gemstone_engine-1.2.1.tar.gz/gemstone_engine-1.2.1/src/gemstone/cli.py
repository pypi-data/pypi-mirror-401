import argparse
import os
import sys
import logging
import subprocess
from datetime import datetime
from importlib.metadata import version as pkg_version, PackageNotFoundError
from gemstone.pipeliner import run_pipeline
import gemstone.dir as Dir

class ExitCode:
    """Standardized exit codes for pipeline errors."""
    MISSING_FILE = 99
    CONFIG_ERROR = 2
    PERMISSION_ERROR = 3
    KEY_ERROR = 4
    RUNTIME_ERROR = 1
    UNKNOWN_ERROR = 100

def get_version() -> str:
    """Returns GEMSTONe version from package metadata (installed) or git (dev)."""
    try:
        return pkg_version("gemstone_engine")  # Use actual package name
    except PackageNotFoundError:
        try:
            return subprocess.check_output(
                ["git", "describe", "--tags", "--dirty", "--always"],
                stderr=subprocess.DEVNULL,
            ).decode().strip()
        except Exception:
            return "unknown"

def display_version(terse:bool = False):
    """Displays the pipeline version (from git describe)."""
    version = get_version()

    if terse:
        print(f" GEMSTONe {version}")
    else:
        print('===========================')
        print(f" GEMSTONe {version}")
        print('===========================')

def show_error(msg, exit_code):
    """Prints and logs an error message, then exits."""
    print(msg)
    logging.error(msg)
    sys.exit(exit_code)

def main():
    """Entry point to start the pipeline."""
    parser = argparse.ArgumentParser(description="Run a GEMSTONe pipeline.")
    parser.add_argument(
        "params",
        type=str,
        nargs="?",  # Make this argument optional
        help="Path to the param file."
    )
    parser.add_argument(
        "jobid_override",
        type=str,
        nargs="?",  # Optional positional
        help="Optional: override the auto-generated job ID, e.g. to restart a job."
    )
    parser.add_argument(
        "--test_mode",
        action="store_true",
        help="Optional: run in test mode (create outputs without executing real code)."
    )
    parser.add_argument(
        "--version", 
        action="store_true", 
        help="Display GEMSTONe version and exit.")

    args = parser.parse_args()
    if args.version:
        display_version(True)
        return
    
    display_version(False)
    setup_logging()

    if args.test_mode:
        logging.warning("TEST MODE ENABLED — no real execution will occur.")

    try:
        Dir.set_root(os.getcwd())
        run_pipeline(args.params, args.jobid_override, test_mode=args.test_mode)

    except FileNotFoundError as e:
        show_error(f"Error: {e}", ExitCode.MISSING_FILE)

    except ValueError as e:
        show_error(f"Configuration error: {e}", ExitCode.CONFIG_ERROR)

    except PermissionError as e:
        show_error(f"Permission error: {e}", ExitCode.PERMISSION_ERROR)

    except RuntimeError as e:
        show_error(f"Runtime error: {e}", ExitCode.RUNTIME_ERROR)

    except KeyError as e:
        show_error(f"Param key error: {e}", ExitCode.KEY_ERROR)

    except Exception as e:
        logging.exception("Unexpected error:")
        show_error("An unexpected error occurred. Check the log for details.", ExitCode.UNKNOWN_ERROR)

class DotMillisecondsFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        t = datetime.fromtimestamp(record.created)
        return t.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Keep milliseconds only

def setup_logging():
    """Set up logging with consistent format and millisecond timestamps."""
    log_file = "GEMSTONe.log"

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Remove any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    formatter = DotMillisecondsFormatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Ensure submodules propagate to root
    logging.getLogger('subprocess').propagate = True
    logging.getLogger('gemstone').propagate = True
    logging.getLogger('stages').propagate = True

    logging.info(f"Logging to file: {log_file}")


if __name__ == "__main__":
    main()
