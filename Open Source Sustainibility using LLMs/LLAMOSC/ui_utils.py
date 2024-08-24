import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
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
from PyQt5.QtWidgets import QWidget, QVBoxLayout
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
        self.timer.start(1000)  # Move figures every 1 second

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
