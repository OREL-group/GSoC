import os
import subprocess
from loguru import logger
from rich.console import Console
from langchain_community.llms import Ollama

console = Console()


def query_ollama(prompt):
    llm = Ollama(model="llama3")
    res = llm.invoke(prompt, stop=["<|eot_id|>"])
    # print(f"OLLAMA response: {res}")
    return res


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
        log_and_print(f"Command output: {e.output}")
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
        log(
            f"The directory {project_dir} is not a Git repository, initiliazing a new one ."
        )
        run_command(["git", "init"])

        # Run the Git commands
        try:
            # print("Running command `git status` \n", run_command(["git", "status"]))

            # Add changes
            print("\nRunning command `git add .` \n", run_command(["git", "add", "."]))

            # Check for changes to commit
            status_output = run_command(["git", "status", "--porcelain"])

            if status_output:
                # Commit changes if there are any
                log_and_print(
                    run_command(["git", "commit", "-m", "Initial commit"]),
                )
            else:
                log_and_print("No changes to commit.")
        except Exception as e:
            log(f"Unexpected error: {e}")
            exit(1)


def repo_commit_current_changes(project_dir, logger=None):
    """
    Commit the current active changes so that it's safer to do git reset later on.
    Use case: for storing the changes made in pre_install and test_patch in a commit.
    """
    prev_path = os.getcwd()
    os.chdir(project_dir)
    if not os.path.exists(os.path.join(project_dir, ".git")):
        log(
            f"The directory {project_dir} is not a Git repository, initiliazing a new one ."
        )
        run_command(["git", "init"])

    # Run the Git commands
    try:
        run_command(["git", "add", "."])

        # Check for changes to commit
        status_output = run_command(["git", "status", "--porcelain"])
        if status_output:
            # Commit changes if there are any
            log_and_print(
                run_command(["git", "commit", "-m", "Automated commit"]),
            )
        else:
            log("No changes to commit.")

        os.chdir(prev_path)

    except Exception as e:
        log(f"Unexpected error: {e}")
        os.chdir(prev_path)
        exit(1)


def repo_apply_diff_and_commit(project_dir, diff_file_path, logger=None):
    """
    Apply a git diff from a file to the repository.
    Use case: for applying patches to the repository.
    """
    if not os.path.exists(os.path.join(project_dir, ".git")):
        log(f"The directory {project_dir} is not a Git repository.")
        exit(1)

    # Check if the diff file exists
    if not os.path.exists(diff_file_path):
        log(f"The diff file {diff_file_path} does not exist.")
        exit(1)

    # check if the diff file is empty (ie not use_acr mode), just skip aplying the diff
    if os.stat(diff_file_path).st_size == 0:
        return

    # Ensure we are in the correct directory
    os.chdir(project_dir)

    # Run the Git commands to apply the diff
    try:
        run_command(["git", "status"])

        # Apply the diff
        run_command(["git", "apply", diff_file_path])

        # Check for changes to commit
        status_output = run_command(["git", "status", "--porcelain"])

        if status_output:
            # Commit changes if there are any
            run_command(["git", "add", "."])
            run_command(["git", "commit", "-m", "Applied diff from file"])
        else:
            log("No changes to commit after applying the diff.")

    except Exception as e:
        log(f"Unexpected error: {e}")
        exit(1)


def log(msg):
    logger.info(msg)


def log_and_print(msg):
    # logger.info(msg)
    console.print(msg)
    console.print(".")


# change this to later make for any metric  by CTRL+Fing all this code

# # Initialize dictionary to store experience over time for each contributor
# experience_over_time = {contributor.name: [] for contributor in contributors}


# # Function to store experience data
# def store_experience(contributors):
#     for contributor in contributors:
#         experience_over_time[contributor.name].append(contributor.experience)


# # Function to update experience
# def update_experience(contributors):
#     global time
#     log_and_print(f"\nTime Step: {time}\n")
#     log_and_print("Experience of all contributors:")
#     log_and_print(
#         [(contributor.name, contributor.experience) for contributor in contributors]
#     )

#     # Store the experience data at the current time step
#     store_experience(contributors)

#     # Simulate some experience increase for a random contributor
#     selected_contributor = random.choice(contributors)
#     selected_contributor.experience += random.randint(1, 3)

#     time += 1


# # Function to update the plot
# def update_plot(frame):
#     update_experience()

#     plt.clf()
#     for name, experiences in experience_over_time.items():
#         plt.plot(range(len(experiences)), experiences, label=name)

#     plt.xlabel("Time Steps")
#     plt.ylabel("Experience")
#     plt.title("Experience of Contributors Over Time")
#     plt.legend()


def docker_necessary_imports():
    import docker
    import os

    client = docker.from_env()
    return client


# Function to stop and remove running containers
def stop_running_containers():
    client = docker_necessary_imports()
    try:
        for container in client.containers.list():
            # print(f"Stopping container {container.id}...")
            container.stop()
            # print(f"Removing container {container.id}...")
            container.remove()
    except Exception as e:
        log(f"Error stopping/removing container: {e}")
        exit(1)
