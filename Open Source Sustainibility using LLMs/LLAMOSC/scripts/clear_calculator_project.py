import os
import shutil

# Step 1: Replace the code in calculator.py
replacementCode = """class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        return a / b"""

current_folder = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(current_folder, "..", "..", "..", "..", "calculator_project")
calculator_file_path = os.path.join(
    project_dir, "calculator", "calculator.py"
)  # Change this path if needed
with open(calculator_file_path, "w") as file:
    file.write(replacementCode)

# # Step 2: Move specified issue files to issues/pending from base_project (Option 1)
# base_project_dir = os.path.join(
#     current_folder, "..", "..", "..", "..", "calculator_project_base_copy"
# )
# base_issues_dir = os.path.join(base_project_dir, "issues")
# # get list of names of all files in issues folder
# source_files = os.listdir(base_issues_dir)
# for file_name in source_files:
#     shutil.copy(
#         os.path.join(base_issues_dir, file_name),
#         os.path.join(project_dir, "issues", "pending", file_name),
#     )

# Step 2: Move specified issue files to issues/pending from whatever is currently in solved (Option 2)
solved_issues_dir = os.path.join(project_dir, "issues", "solved")
if os.path.exists(solved_issues_dir):
    source_files = os.listdir(solved_issues_dir)
    for file_name in source_files:
        shutil.move(
            os.path.join(solved_issues_dir, file_name),
            os.path.join(project_dir, "issues", "pending", file_name),
        )

# Step 3: Remove the issues/solved folder
solved_issues_path = os.path.join(project_dir, "issues", "solved")
if os.path.exists(solved_issues_path):
    shutil.rmtree(solved_issues_path)

# Step 4: Remove all files from pull_requests/merged
merged_pr_path = os.path.join(project_dir, "pull_requests", "merged")
if os.path.exists(merged_pr_path):
    shutil.rmtree(merged_pr_path)
