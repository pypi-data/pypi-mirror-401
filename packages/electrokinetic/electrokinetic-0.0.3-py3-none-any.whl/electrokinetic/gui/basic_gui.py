import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.use("QtAgg")


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("ConSoil")
        self.setGeometry(300, 300, 600, 500)

        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.canvas = MplCanvas(self, width=4, height=3, dpi=100)
        layout.addWidget(self.canvas)
        self.lbl_duration = QLabel("The settling and consolidation time in days : ", self)
        self.lbl_duration.setGeometry(100, 40, 240, 20)
        self.edit_duration = QLineEdit(self)
        self.edit_duration.setGeometry(360, 40, 80, 20)
        self.button = QPushButton("Start", self)
        layout.addWidget(self.button)
        self.button.clicked.connect(self.do_something)

    def do_something(self):
        print(f'Hello world')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
