## Name
DukeSim 3 (provisional name)

## Purpose (objectives & intended audience/users)
This provides a generic, extensible framework for running very loosely coupled software components as a pipeline.
It provides an engine for modular orchestration, and an app library containing templates and a sample application

## OS Platform, Language, dependencies
The software runs on Linux and is written in Python.  

## How to build, install and/or publish
Use directly from a clone of the repo. There is no build or publishing procedure.  
To reset or switch the active pipeline, rerun `use_app_stages.py` with a new app name.

## User Documentation

**For full instructions and detailed information, see:**  

### `src/USERGUIDE.md`  

---

### Quick Overview (For Reference Only):  

#### Summary:  
- `src/app_library`: Holds the catalog of pipelines.  
- `src/stages`: Holds the working copy of the active app.  
- `src/params`: Holds parameter files.  
- `stages.py` and `dirs.py` (at app level): Define a pipeline.  
- `specs.txt` and `run.py` (in each component): Define the parameters and launch interface.  
- `src/engine`: *Must not* be modified by the user.  

#### Common Commands:  
- **Select an app to activate:**  
    ```bash
    python3 src/use_app_stages.py <app_name>  # App name is the directory in app_library
    ```
- **Run the numerous unit tests in `src/tests`:**  
    ```bash
    src/do_tests.sh
    ```
- **Run a pipeline from the command line:**  
    ```bash
    python3 run.py params/<param_file_name>
    # Optional: override auto-generated Job ID
    python3 run.py params/<param_file_name> <jobid_override>
    ```

- **Activate app and run pipeline in one step (convenience wrapper):**  
    ```bash
    ./run_app.sh <app_name> <param_file> [jobid_override] [--testmode]
    ```
## App directory structure
App Repos Will:

- Be Git repos named like G-Recon, G-VIT, etc.
- Be self-contained, not installed via pip, but invoked from repo root.
- Use the name stages/ for the directory containing stage code.
- Place stageflows.txt inside the stages/ directory.
- Place params_example.txt and run_app.py at the repo root.
- Place job outputs in output/ (created by the engine), located at the repo root.

## Packaging the engine and building apps
App Dev with GEMSTONe Clone on Same Server
- git clone git@gitlab.com:gemstone-world/GEMSTONe.git
- cd GEMSTONe
- pip install -e .

- cd ~/repos
- git clone git@gitlab.com:gemstone-world/G-Recon.git
- cd G-Recon
- python run_app.py params_example.txt

    To update engine:
        cd ~/repos/GEMSTONe
        git pull

App Dev in the Field (pip install only)
- pip install gemstone_engine

- cd ~/repos
- git clone git@gitlab.com:gemstone-world/G-Recon.git
- cd G-Recon
- python run_app.py params_example.txt

    To update engine:
        pip install --upgrade gemstone_engine

Engine Publishing (per release)
- cd GEMSTONe
- git pull
- (bump version in pyproject.toml)
- python -m build
- twine upload dist/*

    Then users can do:
        pip install gemstone_engine
        pip install --upgrade gemstone_engine

## License details
No licensing has been considered yet.
