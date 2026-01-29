import argparse
import logging
import os
import shutil
import subprocess
import sys
from typing import List


# --- Configuration ---
class AnsiColors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


# Define the required packages for the scans.
REQUIRED_PACKAGES = [
    "bandit",
    "yamllint",
    "flake8",
    "mypy",
    "types-PyYAML",
    "pandas-stubs"
]

logger = logging.getLogger("scan_helper")
logger.setLevel(logging.INFO)


# --- Helper Functions ---

def _setup_logger(log_file: str):
    """Configures the logger to output to both console and a file."""
    if logger.hasHandlers():
        logger.handlers.clear()

    # Formatter for the logs
    formatter = logging.Formatter('%(message)s')

    # Handler for writing to the specified log file
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Handler for printing to the console (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def _check_and_install_packages(packages: List[str]) -> bool:
    """
    Checks if required packages are installed and installs any that are missing.
    Returns True on success, False on failure.
    """
    logger.info("Checking for required packages...")
    missing_packages = [pkg for pkg in packages if not shutil.which(pkg.split('-')[0])]

    if not missing_packages:
        logger.info("--> All required packages are already installed.")
        return True

    logger.info(
        f"{AnsiColors.YELLOW}--> Attempting to install missing packages: {', '.join(missing_packages)}{AnsiColors.ENDC}")

    # Command to install packages using pip
    install_command = [
                          sys.executable, "-m", "pip", "install",
                          "--quiet", "--root-user-action=ignore", "--disable-pip-version-check"
                      ] + missing_packages

    try:
        # Execute the installation command
        subprocess.run(install_command, check=True, capture_output=True, text=True)
        logger.info(f"{AnsiColors.GREEN}--> All missing packages were installed successfully.{AnsiColors.ENDC}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"{AnsiColors.RED}Error: Failed to install packages.{AnsiColors.ENDC}")
        logger.error(f"Pip stderr: {e.stderr}")
        return False


def _find_files(root: str, extensions: List[str], exclude_dirs: List[str]) -> List[str]:
    """Finds all files with given extensions, excluding specified directories."""
    found_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Remove excluded directories from the list to prevent `os.walk` from traversing them
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                found_files.append(os.path.join(dirpath, filename))
    return found_files


def _run_scan(command: List[str], description: str) -> bool:
    """Runs a generic scan command and logs the outcome."""
    header = f"--- {description} ---"
    logger.info(f"\n{AnsiColors.BLUE}{header}{AnsiColors.ENDC}")

    try:
        # Run the command, capturing output and checking for errors
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if result.stdout:
            logger.info(result.stdout)
        logger.info(f"{AnsiColors.GREEN}✅ Passed{AnsiColors.ENDC}")
        return True
    except subprocess.CalledProcessError as e:
        # If the command returns a non-zero exit code, it's a failure
        logger.error(f"{AnsiColors.RED}❌ Failed with exit code {e.returncode}{AnsiColors.ENDC}")
        if e.stdout:
            logger.error(f"--- STDOUT ---\n{e.stdout}")
        if e.stderr:
            logger.error(f"--- STDERR ---\n{e.stderr}")
        return False


# --- Main Function ---

def run_scans(target_directory: str = '.', venv_name: str = 'venv', log_file: str = 'lint-output.txt') -> bool:
    """
    Runs a series of code quality and security scans on a target directory.

    This function performs the following checks:
    1.  **Dependency Check**: Ensures flake8, mypy, bandit, and yamllint are installed.
    2.  **Flake8**: Lints all Python files.
    3.  **MyPy**: Performs static type checking on all Python files.
    4.  **Bandit**: Scans for common security vulnerabilities in Python code.
    5.  **YAML Lint**: Lints all YAML files in the 'config/' subdirectory.

    Args:
        target_directory (str): The path to the code repository to scan. Defaults to the current directory.
        venv_name (str): The name of the virtual environment directory to exclude from scans. Defaults to 'venv'.
        log_file (str): The path to the output file for scan results. Defaults to 'lint-output.txt'.

    Returns:
        bool: True if all scans pass, False otherwise.
    """
    abs_target_dir = os.path.abspath(target_directory)
    abs_log_file = os.path.join(abs_target_dir, log_file)

    _setup_logger(abs_log_file)

    if not os.path.isdir(abs_target_dir):
        logger.error(f"{AnsiColors.RED}Error: Target directory '{abs_target_dir}' does not exist.{AnsiColors.ENDC}")
        return False

    # Change to the target directory to run commands from the correct context
    original_dir = os.getcwd()
    os.chdir(abs_target_dir)

    # A list to track the success of each scan
    results = []

    try:
        # 1. Check and install dependencies
        if not _check_and_install_packages(REQUIRED_PACKAGES):
            return False  # Exit early if dependencies can't be installed

        # 2. Find files to be scanned
        py_files = _find_files('.', ['.py'], exclude_dirs=[venv_name])
        yaml_files = _find_files('config', ['.yml', '.yaml'], exclude_dirs=[])

        # 3. Run scans
        if py_files:
            results.append(_run_scan(['flake8'] + py_files, "flake8 linting"))
            results.append(_run_scan(['mypy', '--follow-untyped-imports'] + py_files, "mypy type annotation check"))
        else:
            logger.info("\nNo Python files found to scan.")

        # Bandit runs on the directory itself
        results.append(
            _run_scan(['bandit', '.', '-r', '-s', 'B413,B101,B608', '-x', f'./{venv_name}'], "🛡️ bandit security scan"))

        if yaml_files:
            results.append(_run_scan(['yamllint'] + yaml_files, "📄 yaml linting"))
        else:
            logger.info("\nNo YAML files found in 'config/' directory to scan.")

    finally:
        # Ensure we always change back to the original directory
        os.chdir(original_dir)

    # 4. Final summary
    overall_success = all(results)
    if overall_success:
        logger.info(f"\n------------------ {AnsiColors.GREEN}All checks passed!{AnsiColors.ENDC} ------------------\n")
    else:
        logger.error(
            f"\n------------------ {AnsiColors.RED}FAILING BUILD DUE TO SCRIPT ERRORS{AnsiColors.ENDC} ------------------\n")

    return overall_success


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run code quality and security scans on a Python project."
    )
    parser.add_argument(
        "target_directory",
        nargs='?',
        default='.',
        help="The path to the project directory to scan (default: current directory)."
    )
    parser.add_argument(
        "--venv-name",
        default="venv",
        help="The name of the virtual environment directory to exclude (default: venv)."
    )
    parser.add_argument(
        "--log-file",
        default="lint-output.txt",
        help="The name of the file to save the scan output (default: lint-output.txt)."
    )

    args = parser.parse_args()

    # Call the main function with the arguments from the command line
    success = run_scans(
        target_directory=args.target_directory,
        venv_name=args.venv_name,
        log_file=args.log_file
    )

    # Exit with a status code to indicate success or failure for CI/CD pipelines
    if not success:
        sys.exit(1)
