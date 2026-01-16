import os
import fcntl
from datetime import datetime
from gemstone import dir as Dir

JOB_COUNTER_FILE = os.path.join(Dir.output, "jobid.txt")

jobid = None  # Initially unset

def generate_job_id():
    """Generates a unique job ID using YYMMDD-XXX convention with file locking."""
    today = datetime.now().strftime("%y%m%d")
    os.makedirs(Dir.output, exist_ok=True)

    if not os.path.exists(JOB_COUNTER_FILE):
        with open(JOB_COUNTER_FILE, "w") as f:
            f.write("")

    with open(JOB_COUNTER_FILE, "r+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)  # Lock file for concurrency safety
        lines = f.readlines()
        last_id = lines[-1].strip() if lines else None

        if last_id and last_id.startswith(today):
            last_date, last_num = last_id.split("-")
            new_num = int(last_num) + 1
        else:
            new_num = 1  # First ID of the day

        new_id = f"{today}-{new_num:03d}"
        f.write(new_id + "\n")
        fcntl.flock(f, fcntl.LOCK_UN)  # Unlock file

    return new_id

def set_job_id(override=None):
    """Ensures job ID is only generated once and remains persistent."""
    global jobid
    if jobid is None:
        jobid = override if override else generate_job_id()

def get_job_id():
    """Returns the current job ID, generating one if none exists yet."""
    global jobid
    if jobid is None:
        jobid = generate_job_id()
    return jobid
