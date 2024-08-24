from datetime import time
import sys
import os
from PyQt5.QtWidgets import (
    QLineEdit,
    QCheckBox,
    QComboBox,
    QProgressBar,
    QPushButton,
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QPlainTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QFileDialog,
)
from PyQt5.QtCore import pyqtSignal, QObject, QTimer, Qt, QSize
from PyQt5.QtGui import QPainter, QBrush, QColor, QTextCursor, QPixmap, QFont
from PyQt5 import QtTest

import shutil
import random

from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Rectangle

import numpy as np
from rich.console import Console

from LLAMOSC.agents.contributor import ContributorAgent
from LLAMOSC.agents.maintainer import MaintainerAgent
from LLAMOSC.agents.issue_creator import IssueCreatorAgent
from LLAMOSC.simulation.issue import Issue
from LLAMOSC.simulation.sim import Simulation

from LLAMOSC.utils import (
    repo_commit_current_changes,
    repo_apply_diff_and_commit,
    query_ollama,
    run_command,
    stop_running_containers,
    init_plot,
    log_and_print,
)
from LLAMOSC.ui_utils import *
from frontend import *

import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import time


class WorkerSignals(QObject):
    update_log = pyqtSignal(str)


class SimulationApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("LLAMOSC Simulation")

        layout = QVBoxLayout()

        # Contributors input
        layout.addWidget(QLabel("Number of Contributors:"))
        self.contributors_input = QLineEdit()
        self.contributors_input.setText("5")  # Default value
        layout.addWidget(self.contributors_input)

        # Maintainers input
        layout.addWidget(QLabel("Number of Maintainers:"))
        self.maintainers_input = QLineEdit()
        self.maintainers_input.setText("3")  # Default value
        layout.addWidget(self.maintainers_input)

        # Issues input
        layout.addWidget(QLabel("Number of Issues:"))
        self.issues_input = QLineEdit()
        self.issues_input.setText("5")  # Default value
        layout.addWidget(self.issues_input)

        # Use ACR checkbox
        self.acr_checkbox = QCheckBox("Use ACR")
        layout.addWidget(self.acr_checkbox)

        # Use ACR checkbox
        self.test_checkbox = QCheckBox("Testing mode")
        self.test_checkbox.setChecked(True)  # Set default to True
        layout.addWidget(self.test_checkbox)

        # Algorithm selection
        layout.addWidget(QLabel("Decision Making Algorithm:"))
        self.algorithm_selection = QComboBox()
        self.algorithm_selection.addItems(["a (Authoritarian)", "d (Decentralized)"])
        layout.addWidget(self.algorithm_selection)

        # Issue path selection
        layout.addWidget(QLabel("Select Issues Path:"))
        self.issues_path_button = QPushButton("Select Path")
        self.issues_path_button.clicked.connect(self.select_issues_path)
        layout.addWidget(self.issues_path_button)
        self.issues_path_label = QLabel("No path selected")
        layout.addWidget(self.issues_path_label)

        # Start simulation button
        self.start_button = QPushButton("Start Simulation")
        layout.addWidget(self.start_button)
        self.start_button.clicked.connect(self.start_simulation)

        # Log output
        self.log_output = QLabel("Logs will be displayed here.")
        layout.addWidget(self.log_output)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Adjust layout stretch factors
        layout.setStretchFactor(self.contributors_input, 1)
        layout.setStretchFactor(self.maintainers_input, 1)
        layout.setStretchFactor(self.issues_input, 1)
        layout.setStretchFactor(self.acr_checkbox, 0)
        layout.setStretchFactor(self.algorithm_selection, 1)
        layout.setStretchFactor(self.issues_path_button, 0)
        layout.setStretchFactor(self.issues_path_label, 1)
        layout.setStretchFactor(self.start_button, 0)
        layout.setStretchFactor(self.log_output, 1)
        layout.setStretchFactor(self.progress_bar, 0)

        # Set minimum size to ensure widgets are properly visible
        self.setMinimumSize(400, 300)

        # Set layout and show window
        self.setLayout(layout)
        self.show()

    def select_issues_path(self):
        issues_path = QFileDialog.getExistingDirectory(self, "Select Issues Directory")
        if issues_path:
            self.issues_path_label.setText(issues_path)
            self.issues_path = issues_path

    def update_log_output(self, message):
        current_text = self.log_output.text()
        new_text = current_text + "\n" + message
        self.log_output.setText(new_text)
        self.adjustSize()  # Adjust the window size to fit the new text

    def update_progress_bar(self, current, total):
        progress = int((current / total) * 100)
        self.progress_bar.setValue(progress)

    def start_simulation(self):
        # Retrieve values from UI
        n_contributors = int(self.contributors_input.text())
        n_maintainers = int(self.maintainers_input.text())
        n_issues = int(self.issues_input.text())
        use_acr = self.acr_checkbox.isChecked()
        test = self.test_checkbox.isChecked()
        algorithm = self.algorithm_selection.currentText()[0]

        current_folder = os.path.dirname(os.path.abspath(__file__))
        self.project_dir = getattr(self, "issues_path", None)
        if not self.project_dir:  # If the user didn't select a path, use the default.
            self.project_dir = os.path.join(
                current_folder, "..", "..", "..", "..", "calculator_project"
            )

        # testing
        other = os.path.join(
            current_folder, "..", "..", "..", "..", "calculator_project"
        )
        self.progress_bar.setValue(0)
        self.log_output.setText(
            "Starting simulation with the following parameters:\n"
            f"Contributors: {n_contributors}\n"
            f"Maintainers: {n_maintainers}\n"
            f"Issues: {n_issues}\n"
            f"Use ACR: {use_acr}\n"
            f"Algorithm: {algorithm}\n"
            f"Issues Path: {self.project_dir}"
        )

        self.progress_bar.setValue(100)

        console = Console()

        def log_and_print(message):
            # special function to log and print messages in UI directly
            console.print(message)
            self.log_output.setText(message)
            self.adjustSize()  # Adjust the window size to fit the new text

        # Clear the project directory
        repo_commit_current_changes(self.project_dir)

        # Get the path to the issues folder
        # current folder
        issues_parent_folder = os.path.join(self.project_dir, "issues")
        issues_folder = os.path.join(issues_parent_folder, "pending")
        # Loop through all the files in the issues folder
        self.progress_bar.setValue(10)
        # log_and_print("Reading existing issues from the issues folder...")
        issues = []
        total_files = len(os.listdir(issues_folder))
        index = 0
        issue_id = 1
        for index, filename in enumerate(os.listdir(issues_folder)):
            # Create the file path
            file_path = os.path.join(issues_folder, filename)

            # Extract the issue id from the filename
            issue_id = int(filename.split("_")[1].split(".")[0])

            # Create the issue object
            # TODO: Better way to get issue difficulty
            issue = Issue(issue_id, (issue_id + 1) % 5, file_path)

            # Add the issue to the issues list
            issues.append(issue)

            # Update progress
            self.update_progress_bar(index + 1, total_files)

        if len(issues) < n_issues:
            self.progress_bar.setValue(10)
            log_and_print("IssueCreatorAgent creating new issues...")

            issue_creator = IssueCreatorAgent(name="Issue Creator")
            existing_code = """"""

            for root, _, files in os.walk(self.project_dir):
                for file in files:
                    if file.endswith(".py"):
                        with open(os.path.join(root, file), "r") as code_file:
                            existing_code += code_file.read() + "\n"

            # create the required number of issues
            for i in range(len(issues) + 1, n_issues + 1):
                if test:
                    issue_filename = f"task_{len(issues) + 1}.md"
                    final_issue_string = """Issue 1: Add Trigonometry Functionality
                        Title: Feature Request: Implement Trigonometry Functions in Calculator
                        Checked Other Resources: Yes"""
                    with open(
                        os.path.join(issues_folder, issue_filename), "w"
                    ) as issue_file:
                        issue_file.write(final_issue_string)
                    issue = Issue(
                        len(issues) + 1,
                        (issue_id + 1) % 5,
                        os.path.join(issues_folder, issue_filename),
                    )
                else:
                    issue = issue_creator.create_issue(
                        issues, existing_code, issues_folder
                    )
                issues.append(issue)
                # Update progress
                self.update_progress_bar(
                    i - total_files + 1, n_issues - total_files + 1
                )

        # Create required agents
        self.progress_bar.setValue(10)
        log_and_print("Creating required agents...")
        self.contributors = [
            ContributorAgent(i, random.randint(1, 4), f"Contributor_{i}", test)
            for i in range(n_contributors)  # 5 contributors by default
        ]
        self.progress_bar.setValue(70)
        self.maintainers = [
            MaintainerAgent(i, random.randint(4, 5), f"Maintainer_{i}")
            for i in range(n_maintainers)  # 3 maintainers by default
        ]

        self.progress_bar.setValue(100)
        log_and_print(
            f"\nStarting simulation with {len(issues)} issues and {len(self.contributors)} contributors with ACR : {use_acr} and Algorithm : {algorithm}.\n"
        )

        self.issues_history = {
            "pending": {"moon_shot": 0, "earth_shot": 0, "mars_shot": 0},
            "solved": {"moon_shot": 0, "earth_shot": 0, "mars_shot": 0},
        }

        for iss in issues:
            if iss.difficulty < 2:
                self.issues_history["pending"]["moon_shot"] += 1
            elif iss.difficulty < 4:
                self.issues_history["pending"]["earth_shot"] += 1
            else:
                self.issues_history["pending"]["mars_shot"] += 1

        # time.sleep(5)

        # Remove old widgets
        for widget in self.findChildren(QWidget):
            widget.deleteLater()

        # log_and_print(f"Created agents: contributors and maintainers")
        # time.sleep(2)

        self.sim = Simulation(self.contributors)

        # Initialize time and experience history
        global timestep
        timestep = 0
        self.experience_history = {
            contributor.name: [contributor.experience]
            for contributor in self.contributors
        }
        self.motivation_history = {
            contributor.name: [contributor.motivation_level]
            for contributor in self.contributors
        }
        self.code_qal_history = [2.5]  # just a basic average to start with
        self.code_qal_curr_history = [2.5]  # just a basic average to start with
        self.time_history = [0]

        self.fig_cont_exp, self.ax_cont_exp = plt.subplots()
        self.fig_code_qal, self.ax_code_qal = plt.subplots()
        self.fig_cont_mot, self.ax_cont_mot = plt.subplots()

        # init metrics 1 plot
        init_plot(
            axis=self.ax_cont_exp,
            x_label="Time Step",
            y_label="Contributor Experience",
            x_max=len(issues),
            y_max=5,
            title="Contributor Experience Metric",
        )

        init_plot(
            axis=self.ax_cont_mot,
            x_label="Time Step",
            y_label="Contributor Motivation",
            x_max=len(issues),
            y_max=10,
            title="Contributor Motivation Metric",
        )

        init_plot(
            axis=self.ax_code_qal,
            x_label="Time Step",
            y_label="Code Quality",
            x_max=len(issues),
            y_max=5,
            title="Simulation Average Code Quality Metric",
        )

        # Close older window for taking input
        self.close()

        # Create new layout and widgets for detailed simulation
        self.simulation_window = MyMainWindow(
            self.fig_cont_exp,
            self.fig_code_qal,
            self.fig_cont_mot,
            self.ax_cont_exp,
            self.ax_code_qal,
            self.ax_cont_mot,
            self.contributors,
        )
        self.simulation_window.showMaximized()

        # updating issues status for the first time
        for category in self.simulation_window.pending_labels.keys():
            self.simulation_window.pending_labels[category].setText(
                f"{category.replace('_', ' ').title()}: {self.issues_history['pending'][category]}"
            )
            self.simulation_window.solved_labels[category].setText(
                f"{category.replace('_', ' ').title()}: {self.issues_history['solved'][category]}"
            )

        for issue in issues:
            timestep += 1
            self.update(
                test,
                timestep,
                issues,
                issues_parent_folder,
                issue,
            )
            # Print a separator for better readability
            print("\n", "-" * 100, "\n")

    def update(
        self,
        is_test,
        timestep,
        issues,
        issues_parent_folder,
        issue,
    ):
        # Update the timestep counter
        self.simulation_window.timestep_counter.setText(str(timestep))

        # Example of updating logs or other UI elements
        self.simulation_window.log.setText(f"Simulation timestep: {timestep}")

        issues_folder = os.path.join(issues_parent_folder, "pending")
        issues_pending = len(os.listdir(issues_folder))
        if os.path.exists(os.path.join(issues_parent_folder, "solved")):
            issues_solved = len(
                os.listdir(os.path.join(issues_parent_folder, "solved"))
            )
        else:
            issues_solved = 0

        # Current issue
        issue_description = open(issue.filepath).read()
        issue_title = issue_description.split("\n")[0]
        self.simulation_window.log.setText(
            self.simulation_window.log.text()
            + "\n"
            + f"Current Issue #{issue.id} (Difficulty ({issue.difficulty})): {issue_title}\n"
        )

        # from the maintainers, select the maintainer who will be responsible for the issue by random from avilable & eligible maintainers
        selected_maintainer = random.choice(
            [
                maintainer
                for maintainer in self.maintainers
                if maintainer.eligible_for_issue(issue)
            ]
        )
        selected_maintainer.allot_task(issue)

        if is_test:
            selected_contributor = random.choice(
                [
                    maintainer
                    for maintainer in self.contributors
                    if maintainer.eligible_for_issue(issue)
                ]
            )
            self.simulation_window.log.setText(
                self.simulation_window.log.text()
                + "\n"
                + f"Selected contributor {selected_contributor.name} by bidding among all contributors in a decentralized manner."
            )
        else:
            if self.algorithm_selection == "d":
                selected_contributor = self.sim.select_contributor_decentralized(issue)
                self.simulation_window.log.setText(
                    self.simulation_window.log.text()
                    + "\n"
                    + f"Selected contributor {selected_contributor.name} by bidding among all contributors in a decentralized manner."
                )
            else:
                selected_contributor = self.sim.select_contributor_authoritarian(
                    selected_maintainer
                )
                self.simulation_window.log.setText(
                    self.simulation_window.log.text()
                    + "\n"
                    + f"Selected contributor {selected_contributor.name} by maintainer rating all contributors in an authoritarian manner."
                )

        for other_contributor in self.contributors:
            if other_contributor.id == selected_contributor.id:
                continue
            elif not other_contributor.eligible_for_issue(issue):
                continue
            if is_test:
                other_contributor.motivation_level = (
                    other_contributor.motivation_level - 0.5
                ) % 10
                continue
            other_contributor.update_motivation_level(bid_selected=False)

        selected_contributor.assign_issue(issue)
        task_solved = (
            selected_contributor.solve_issue(self.project_dir)
            if self.acr_checkbox and not is_test
            else selected_contributor.solve_issue_without_acr(self.project_dir, is_test)
        )

        pull_requests_dir = os.path.join(self.project_dir, "pull_requests")
        if task_solved:

            # Find the most recent pull request for the given task_id
            task_id = issue.id
            pull_request_dirs = [
                f
                for f in os.listdir(pull_requests_dir)
                if f.startswith(f"pull_request_{task_id}")
            ]
            if len(pull_request_dirs) == 0:
                log_and_print(f"No pull requests found for task ID: {task_id}")
                return

            log_and_print("Solved the assigned issue")
            pull_request_dirs.sort(key=lambda x: int(x.split("_v")[-1]))
            most_recent_pull_request = pull_request_dirs[-1]
            pull_request_dir = os.path.join(pull_requests_dir, most_recent_pull_request)

            if is_test:
                pr_accepted = random.randint(2, 5)
                selected_maintainer.unassign_task()
            else:
                selected_maintainer.review_pull_request(
                    pull_request_dir, self.project_dir
                )

            if pr_accepted:
                message = f"Maintainer {selected_maintainer.name} has merged pull request for Issue #{issue.id}.\n"
                self.simulation_window.log.setText(
                    self.simulation_window.log.text() + "\n" + message
                )
                # increase experience of the contributor
                selected_contributor.increase_experience(1, issue.difficulty)
                # increase no of pull requests and calculate new average code quality of the simulation
                try:
                    self.sim.update_code_quality(pr_accepted)
                except:
                    pr_accepted = self.sim.update_code_quality(random.randint(1, 3))

                # update number of pending and solved issues
                if issue.difficulty < 2:
                    self.issues_history["pending"]["moon_shot"] -= 1
                    self.issues_history["solved"]["moon_shot"] += 1
                elif issue.difficulty < 4:
                    self.issues_history["pending"]["earth_shot"] -= 1
                    self.issues_history["solved"]["earth_shot"] += 1
                else:
                    self.issues_history["pending"]["mars_shot"] -= 1
                    self.issues_history["solved"]["mars_shot"] += 1

                for category in self.simulation_window.pending_labels.keys():
                    self.simulation_window.pending_labels[category].setText(
                        f"{category.replace('_', ' ').title()}: {self.issues_history['pending'][category]}"
                    )
                    self.simulation_window.solved_labels[category].setText(
                        f"{category.replace('_', ' ').title()}: {self.issues_history['solved'][category]}"
                    )

                # make a "merged" folder in the pull_requests folder and move the merged pull request there
                merged_dir = os.path.join(self.project_dir, "pull_requests", "merged")
                os.makedirs(merged_dir, exist_ok=True)
                merged_pull_request_dir = os.path.join(
                    merged_dir, most_recent_pull_request
                )
                os.rename(pull_request_dir, merged_pull_request_dir)
                # delete the other versions of the pull request for the same task_id
                for pr_dir in pull_request_dirs:
                    if pr_dir == most_recent_pull_request:
                        continue
                    if pr_dir.startswith(f"pull_request_{task_id}"):
                        pr_dir_path = os.path.join(pull_requests_dir, pr_dir)
                        shutil.rmtree(pr_dir_path)

                # make a "solved" folder in the issues folder and move the solved issue there
                solved_dir = os.path.join(self.project_dir, "issues", "solved")
                os.makedirs(solved_dir, exist_ok=True)
                solved_issue_path = os.path.join(solved_dir, f"task_{task_id}.md")
                os.rename(issue.filepath, solved_issue_path)
                repo_commit_current_changes(self.project_dir)

            else:
                log_and_print(
                    f"Maintainer {selected_maintainer.name} has rejected pull request for Issue #{issue.id}.\n"
                )
                # TODO : make a "rejected" folder in the pull_requests folder and move the rejected pull request there

        else:
            log_and_print("Error solving the assigned issue")
            return

        # update selected_contributor motivation level
        if is_test:
            selected_contributor.motivation_level += 0.5
        else:
            selected_contributor.update_motivation_level(
                success=pr_accepted,
                bid_selected=True,
                task_difficulty=issue.difficulty,
                code_quality=pr_accepted if pr_accepted else random.randrange(0, 3),
            )
        # Append new experiences to history
        self.time_history.append(timestep)
        for contributor in self.contributors:
            self.experience_history[contributor.name].append(contributor.experience)
            self.motivation_history[contributor.name].append(
                contributor.motivation_level
            )
        self.code_qal_history.append(self.sim.avg_code_quality)
        (
            self.code_qal_curr_history.append(pr_accepted)
            if pr_accepted
            else self.code_qal_curr_history.append(random.randint(1, 3))
        )
        self.simulation_window.update_axes(
            self.time_history,
            self.experience_history,
            self.contributors,
            self.code_qal_history,
            self.code_qal_curr_history,
            self.motivation_history,
        )

        # Example of updating stick figure positions or other plots
        # This assumes that stick figures or plots have methods to update themselves
        for i in range(self.simulation_window.stick_figure_app.num_stick_figures):
            self.simulation_window.stick_figure_app.set_stick_figure_position(
                i, timestep % len(self.simulation_window.stick_figure_app.rects)
            )

        # Timer to simulate actual working
        QtTest.QTest.qWait(1000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SimulationApp()
    sys.exit(app.exec_())
