import os
import subprocess
from loguru import logger
from rich.console import Console

console = Console()


# def run_command(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:

#     try:
#         cp = subprocess.run(cmd, check=True, **kwargs)
#     except subprocess.CalledProcessError as e:
#         log_and_print(f"Error running command: {cmd}, {e}")
#         raise e
# return cp


def run_command(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    """
    Run a command in the shell.
    Args:
        - cmd: command to run
    """
    try:
        cp = subprocess.run(cmd, check=True, text=True, capture_output=True, **kwargs)
        return cp.stdout.strip()
    except subprocess.CalledProcessError as e:
        log_and_print(f"Error executing command {cmd}: {e}")
        # log_and_print(f"Command output: {e.output}")
        # log_and_print(f"Return code: {e.returncode}")
        exit(1)


def is_git_repo() -> bool:
    """
    Check if the current directory is a git repo.
    """
    git_dir = ".git"
    return os.path.isdir(git_dir)


def initialize_git_repo_and_commit(project_dir, logger=None):
    """
    Initialize the current directory as a git repository and make an initial commit.
    """
    os.chdir(project_dir)
    # Check if this is a valid Git repository

    if not os.path.exists(os.path.join(project_dir, ".git")):
        print(
            f"The directory {project_dir} is not a Git repository, initiliazing a new one ."
        )
        run_command(["git", "init"])

    # Run the Git commands
    try:
        run_command(["git", "status"])

        # Add changes
        run_command(["git", "add", "."])

        # Check for changes to commit
        status_output = run_command(["git", "status", "--porcelain"])

        if status_output:
            # Commit changes if there are any
            run_command(["git", "commit", "-m", "Initial commit"])
        else:
            print("No changes to commit.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)


def repo_commit_current_changes(project_dir, logger=None):
    """
    Commit the current active changes so that it's safer to do git reset later on.
    Use case: for storing the changes made in pre_install and test_patch in a commit.
    """
    if not os.path.exists(os.path.join(project_dir, ".git")):
        print(
            f"The directory {project_dir} is not a Git repository, initiliazing a new one ."
        )
        run_command(["git", "init"])

    # Run the Git commands
    try:
        run_command(["git", "status"])

        # Add changes
        run_command(["git", "add", "."])

        # Check for changes to commit
        status_output = run_command(["git", "status", "--porcelain"])

        if status_output:
            # Commit changes if there are any
            run_command(["git", "commit", "-m", "Automated commit"])
        else:
            print("No changes to commit.")

    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)


def log_and_print(msg):
    logger.info(msg)
    console.print(msg)


import docker
import os

client = docker.from_env()


# Function to stop and remove running containers
def stop_running_containers():
    try:
        for container in client.containers.list():
            print(f"Stopping container {container.id}...")
            container.stop()
            print(f"Removing container {container.id}...")
            container.remove()
    except Exception as e:
        print(f"Error stopping/removing container: {e}")
        exit(1)
