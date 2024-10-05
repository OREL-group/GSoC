import sys
import numpy as np
from PyQt5.QtWidgets import (
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
)
from PyQt5.QtCore import QTimer, Qt, QSize
from PyQt5.QtGui import QPainter, QBrush, QColor, QTextCursor, QPixmap, QFont
import random
import os

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Rectangle

import numpy as np


class StickFigure:
    def __init__(self, id, name, plot, current_rect):
        self.id = id
        self.name = name
        self.plot = plot
        self.current_rect = current_rect

    def set_position(self, x, y):
        self.plot.set_position((x, y))


class StickFigureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a Matplotlib figure and axis
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Initialize stick figures
        self.stick_figures = {}
        self.names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
        self.num_stick_figures = len(self.names)

        # Initialize the plot
        self.setup_squares()

        # Setup the timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_stick_figures)
        self.timer.start(100)  # Move figures every 1 second

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.setup_squares()

    def setup_squares(self):
        # Clear existing patches
        self.ax.clear()

        # Get the size of the widget
        widget_width = self.size().width()
        widget_height = self.size().height()

        # Define the large rectangle dimensions
        large_rect_width = widget_width
        large_rect_height = widget_height

        # Define the size and position of each small rectangle
        num_rows = 2
        num_cols = 2
        small_rect_width = large_rect_width / num_cols
        small_rect_height = large_rect_height / num_rows

        colors = ["red", "green", "blue", "yellow"]
        self.labels = ["Available", "Eligible", "Discussion", "Busy"]
        self.rects = []

        # Define the large rectangle
        self.ax.add_patch(
            Rectangle((0, 0), large_rect_width, large_rect_height, fill=False)
        )

        for i, (color, label) in enumerate(zip(colors, self.labels)):
            row = i // num_cols
            col = i % num_cols
            rect_x = col * small_rect_width
            rect_y = row * small_rect_height

            rect = Rectangle(
                (rect_x, rect_y),
                small_rect_width,
                small_rect_height,
                color=color,
                alpha=0.5,
            )
            self.ax.add_patch(rect)
            self.rects.append(rect)
            self.ax.text(
                rect_x + small_rect_width / 2,
                rect_y + small_rect_height / 2,
                label,
                ha="center",
                va="center",
                fontsize=12,
                color="black",
            )

        # Set limits and aspect ratio for better visualization
        self.ax.set_xlim(0, large_rect_width)
        self.ax.set_ylim(0, large_rect_height)
        self.ax.set_aspect("auto")  # Allow automatic aspect ratio adjustment
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()

        self.add_stick_figures()

    def add_stick_figures(self):
        for i in range(self.num_stick_figures):
            x, y = self.random_position(self.rects[i % len(self.rects)])
            stick_figure = StickFigure(
                id=i,
                name=self.names[i],
                plot=self.ax.text(
                    x, y, "😃", fontsize=12, ha="center", va="bottom", color="black"
                ),
                current_rect=self.rects[i % len(self.rects)],
            )
            self.stick_figures[i] = stick_figure
        self.canvas.draw()

    def random_position(self, rect):
        x = np.random.uniform(rect.get_x(), rect.get_x() + rect.get_width())
        y = np.random.uniform(rect.get_y(), rect.get_y() + rect.get_height())
        return x, y

    def get_rect_for_stick_figure(self, index):
        num_rows = 2
        num_cols = 2
        small_rect_width = self.size().width() / num_cols
        small_rect_height = self.size().height() / num_rows
        row = index // num_cols
        col = index % num_cols
        rect_x = col * small_rect_width
        rect_y = row * small_rect_height
        return Rectangle(
            (rect_x, rect_y), small_rect_width, small_rect_height, color="white"
        )

    def move_stick_figures(self):
        for stick_figure in self.stick_figures.values():
            rect = stick_figure.current_rect
            x, y = stick_figure.plot.get_position()
            if x is not None and y is not None:
                # Move stick figure randomly within the current square
                new_x = np.clip(
                    x + np.random.uniform(-0.05, 0.05),
                    rect.get_x(),
                    rect.get_x() + rect.get_width(),
                )
                new_y = np.clip(
                    y + np.random.uniform(-0.05, 0.05),
                    rect.get_y(),
                    rect.get_y() + rect.get_height(),
                )
                stick_figure.set_position(new_x, new_y)

        self.canvas.draw()
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_stick_figures)
        self.timer.start(100)  # Move figures every 0.1 second

        # for i in range(self.num_stick_figures):
        #     self.set_stick_figure_position(i,1)

    def set_stick_figure_position(self, fig_id, square_index):
        if fig_id in self.stick_figures and 0 <= square_index < len(self.rects):
            stick_figure = self.stick_figures[fig_id]
            stick_figure.current_rect = self.rects[square_index]
            x, y = self.random_position(self.rects[square_index])
            stick_figure.set_position(x, y)
            self.canvas.draw()

    def set_stick_figure_name(self, fig_id, name):
        if fig_id in self.stick_figures:
            self.stick_figures[fig_id].name = name

    def get_stick_figure_name(self, fig_id):
        if fig_id in self.stick_figures:
            return self.stick_figures[fig_id].name
        return None


class RichPlainTextEdit(QPlainTextEdit):
    def __init__(self, color="white", font_size=22):
        super().__init__()
        self.setStyleSheet(
            f"background-color: black; color: {color}; font-size: {font_size}px;"
        )
        self.setPlainText("")
        self.setFixedSize(600, 600)

    def append_colored_text(self, text, color):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        format = cursor.charFormat()
        format.setForeground(QColor(color))
        cursor.setCharFormat(format)
        cursor.insertText(text)
        self.ensureCursorVisible()


class AnimatedBox(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 200)
        self.color = QColor(Qt.red)
        self.pos_x = 0
        self.setStyleSheet(f"background-color: {self.color.name()};")
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)
        self.timer.start(50)  # Update every 500ms

    def update_position(self):
        self.pos_x += 2
        if self.pos_x > self.width():
            self.pos_x = 0
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setBrush(QBrush(self.color))
        painter.drawRect(self.pos_x, 0, 20, 20)  # Simple moving box


class MyMainWindow(QMainWindow):
    def __init__(
        self,
        fig_cont_exp,
        fig_code_qal,
        fig_cont_mot,
        ax_cont_exp,
        ax_code_qal,
        ax_cont_mot,
        contributors,
    ):
        super().__init__()

        # Main Widget and Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)

        # Fullscreen Window
        self.setGeometry(100, 100, 1920, 1080)

        # Column 1 and 2 (Left and Center)
        self.left_center_layout = QGridLayout()
        self.layout.addLayout(self.left_center_layout, 0, 0, 1, 2)

        # Issues Bar (Top Row)
        self.issues_bar = QGridLayout()
        self.left_center_layout.addLayout(self.issues_bar, 0, 0, 1, 2)
        self.create_issues_bar()

        # Rich Consoles (Below Issues Bar)
        self.consoles_layout = QGridLayout()
        self.left_center_layout.addLayout(self.consoles_layout, 1, 0, 3, 2)

        self.active_discussion_console = RichPlainTextEdit(color="green", font_size=22)
        self.pull_requests_console = RichPlainTextEdit(color="white", font_size=22)

        self.consoles_layout.addWidget(QLabel("Active Discussion"), 0, 0)
        self.consoles_layout.addWidget(self.active_discussion_console, 1, 0, 3, 1)

        self.consoles_layout.addWidget(QLabel("Pull Requests"), 0, 1)
        self.consoles_layout.addWidget(self.pull_requests_console, 1, 1, 3, 1)

        # Matplotlib Plot for Simulation Metrics
        self.contributors = contributors
        self.experience_history = {
            contributor.name: [contributor.experience]
            for contributor in self.contributors
        }
        self.motivation_history = {
            contributor.name: [contributor.motivation_level]
            for contributor in self.contributors
        }

        # self.active_discussion_console.append_colored_text(
        #     "Initially"
        #     + str(self.experience_history)
        #     + "\n"
        #     + str(self.motivation_history),
        #     "white",
        # )

        self.code_qal_history = [2.5]  # just a basic average to start with
        self.code_qal_curr_history = [2.5]  # just a basic average to start with
        self.time_history = [0]

        self.simulation_metrics_plot = QVBoxLayout()
        self.fig_code_qal = fig_code_qal
        self.ax_code_qal = ax_code_qal
        self.lines_code_qal = {
            "avg": self.ax_code_qal.plot(
                self.time_history,
                self.code_qal_history,
                label="Average Code Quality",
                color="blue",
            )[0],
            "curr": self.ax_code_qal.plot(
                self.time_history,
                self.code_qal_curr_history,
                label="Current Code Quality",
                color="red",
            )[0],
        }
        self.left_center_layout.addLayout(self.simulation_metrics_plot, 4, 0, 1, 2)
        self.simulation_metrics_codeqal = FigureCanvas(fig_code_qal)
        self.simulation_metrics_plot.addWidget(
            QLabel("Simulation Metrics : Code Quality")
        )
        self.simulation_metrics_plot.addWidget(self.simulation_metrics_codeqal)

        # Right Column
        self.right_layout = QVBoxLayout()
        self.layout.addLayout(self.right_layout, 0, 2, 1, 1)

        # Heading
        self.heading_label = QLabel("Contributor Metrics")
        self.heading_label.setStyleSheet("font-size: 24px;")
        self.right_layout.addWidget(self.heading_label)

        # Replace Top One-Third with StickFigureApp
        self.stick_figure_app = StickFigureApp()
        self.right_layout.addWidget(self.stick_figure_app, 1)
        self.stick_figure_app.setMinimumSize(500, 300)  # Example size, adjust as needed

        # Two Metrics Plots Below
        self.lower_plots_layout = QVBoxLayout()
        self.right_layout.addLayout(self.lower_plots_layout)

        self.fig_cont_exp = fig_cont_exp
        self.ax_cont_exp = ax_cont_exp
        self.lines_cont_exp = {
            contributor.name: self.ax_cont_exp.plot(
                self.time_history,
                self.experience_history[contributor.name],
                label=contributor.name,
            )[0]
            for contributor in self.contributors
        }

        self.fig_cont_mot = fig_cont_mot
        self.ax_cont_mot = ax_cont_mot
        self.lines_cont_mot = {
            contributor.name: self.ax_cont_mot.plot(
                self.time_history,
                self.motivation_history[contributor.name],
                label=contributor.name,
            )[0]
            for contributor in self.contributors
        }

        self.plot_cont_exp = FigureCanvas(fig_cont_exp)
        self.plot_cont_motiv = FigureCanvas(fig_cont_mot)  # TODO: change to motiv
        self.lower_plots_layout.addWidget(QLabel("Contributor Experience"))
        self.lower_plots_layout.addWidget(self.plot_cont_exp)
        self.lower_plots_layout.addWidget(QLabel("Contributor Motivation"))
        self.lower_plots_layout.addWidget(self.plot_cont_motiv)

        # Timer for updating layout
        self.timer = QTimer()
        self.timer.timeout.connect(self.stick_figure_app.move_stick_figures)
        self.timer.start(200)  # Update every second

    def create_issues_bar(self):
        # Define colors and icons
        categories = ["moon_shot", "earth_shot", "mars_shot"]
        colors = {"moon_shot": "white", "earth_shot": "cyan", "mars_shot": "red"}
        current_folder = os.path.dirname(os.path.abspath(__file__))
        icons = {
            "moon_shot": os.path.join(
                current_folder, "assets", "moon_shot.png"
            ),  # Replace with actual paths to your icons
            "earth_shot": os.path.join(current_folder, "assets", "earth_shot.png"),
            "mars_shot": os.path.join(current_folder, "assets", "mars_shot.png"),
        }

        # Initialize labels dictionaries
        self.pending_labels = {}
        self.solved_labels = {}

        # Create TimeStep Count
        self.timestep_layout = QGridLayout()
        self.issues_bar.addLayout(self.timestep_layout, 1, 0)

        self.timestep_counter = QLabel("0")
        self.timestep_counter.setStyleSheet(
            "font-size:40px; padding: 10px; text-align: center;"
        )
        self.timestep_label = QLabel("Timestep : ")
        self.timestep_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.timestep_layout.addWidget(self.timestep_label, 0, 0)
        self.timestep_layout.addWidget(self.timestep_counter, 1, 0)

        # Log output
        self.log_label = QLabel("Logs :")
        self.log_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        # self.timestep_layout.addWidget(self.log_label, 0,1)
        self.log = QLabel(
            "Logs of current timestep will be displayed here.Logs of current timestep will be displayed here.Logs of current timestep will be displayed here. \n\n Logs of current timestep will be displayed here.Logs of current timestep will be displayed here.Logs of current timestep will be displayed here. \n\n Logs of current timestep will be displayed here.Logs of current timestep will be displayed here.Logs of current timestep will be displayed here.Logs of current timestep will be displayed here.Logs of current timestep will be displayed here.Logs of current timestep will be displayed here.Logs of current timestep will be displayed here."
        )
        self.log.setStyleSheet("font-size: 20px; padding: 10px; ")
        self.log.setWordWrap(True)
        # Set font to monospaced and style it
        font = QFont("Courier", 12)  # Monospaced font and size
        self.log.setFont(font)
        # Create a QScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # Adjust size to the QLabel's size
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Set the QLabel as the widget of the QScrollArea
        self.scroll_area.setWidget(self.log)
        self.timestep_layout.addWidget(self.scroll_area, 0, 1, 2, 1)

        # Create Issues Bar Layout
        self.issues_layout = QGridLayout()
        self.issues_bar.addLayout(self.issues_layout, 1, 1)

        # Pending Issues
        self.pending_layout = QVBoxLayout()
        self.pending_label = QLabel("Issues Pending")
        self.pending_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; background-color: orange"
        )
        self.issues_layout.addWidget(self.pending_label, 0, 0)

        for category in categories:
            icon = QPixmap(icons[category])
            icon = icon.scaled(
                QSize(24, 24), aspectRatioMode=1
            )  # Aspect ratio mode: 1 means keeping aspect ratio
            icon_label = QLabel()
            icon_label.setPixmap(icon)
            icon_label.setFixedSize(24, 24)
            count_label = QLabel("0")
            count_label.setStyleSheet(
                f"color: {colors[category]}; font-size: 20px; background-color: black"
            )

            h_layout = QHBoxLayout()
            h_layout.addWidget(icon_label)
            h_layout.addWidget(count_label)
            self.pending_layout.addLayout(h_layout)
            self.pending_labels[category] = count_label

        self.issues_layout.addLayout(self.pending_layout, 1, 0)

        # Solved Issues
        self.solved_layout = QVBoxLayout()
        self.solved_label = QLabel("Issues Solved")
        self.solved_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; background-color: green"
        )
        self.issues_layout.addWidget(self.solved_label, 0, 1)

        for category in categories:
            icon = QPixmap(icons[category])
            icon = icon.scaled(
                QSize(24, 24), aspectRatioMode=1
            )  # Aspect ratio mode: 1 means keeping aspect ratio
            icon_label = QLabel()
            icon_label.setPixmap(icon)
            icon_label.setFixedSize(24, 24)
            count_label = QLabel("0")
            count_label.setStyleSheet(
                f"color: {colors[category]}; font-size: 20px; background-color: black"
            )

            h_layout = QHBoxLayout()
            h_layout.addWidget(icon_label)
            h_layout.addWidget(count_label)
            self.solved_layout.addLayout(h_layout)
            self.solved_labels[category] = count_label

        self.issues_layout.addLayout(self.solved_layout, 1, 1)

    # TODO : update stick figures according to the current state of the simulation
    # for i in range(self.stick_figure_app.num_stick_figures):
    #     self.stick_figure_app.set_stick_figure_position(i,1)

    def update_axes(
        self,
        time_history,
        experience_history,
        contributors,
        code_qal_history,
        code_qal_curr_history,
        motivation_history,
    ):
        # updating contributor experience metric data
        for contributor in contributors:
            self.lines_cont_exp[contributor.name].set_data(
                time_history, experience_history[contributor.name]
            )
        self.ax_cont_exp.legend()
        self.fig_cont_exp.tight_layout()
        self.plot_cont_exp.draw()

        # updating contribution motivation metric data
        for contributor in contributors:
            self.lines_cont_mot[contributor.name].set_data(
                time_history, motivation_history[contributor.name]
            )
        self.ax_cont_mot.legend()
        self.fig_cont_mot.tight_layout()
        self.plot_cont_motiv.draw()

        # self.pull_requests_console.append_colored_text(
        #     self.log.text()
        #     + "\n"
        #     + "Finally"
        #     + str(experience_history)
        #     + "\n"
        #     + str(motivation_history),
        #     "green",
        # )

        # Update code_quality metric line data
        self.lines_code_qal["avg"].set_data(time_history, code_qal_history)
        self.lines_code_qal["curr"].set_data(time_history, code_qal_curr_history)
        self.ax_code_qal.legend()
        self.fig_code_qal.tight_layout()
        self.simulation_metrics_codeqal.draw()

    def update_plots(self):
        self.ax_cont_exp.legend()
        self.fig_cont_exp.tight_layout()
        self.plot_cont_exp.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
