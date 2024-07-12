import os


def create_calculator_project_directory():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    calculator_project_path = os.path.join(base_dir, "calculator_project")

    if not os.path.exists(calculator_project_path):
        os.makedirs(calculator_project_path)
        print(f"Created {calculator_project_path} directory")
    else:
        print(f"{calculator_project_path} directory already exists")


if __name__ == "__main__":
    create_calculator_project_directory()
