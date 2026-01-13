
# https://coderscratchpad.com/pyqt6-handling-command-line-arguments/

import sys
import argparse
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self, args):
        super().__init__()
        self.setWindowTitle("Advanced Command Line Arguments")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Display parsed command line arguments
        label = QLabel(f"Arguments: {args}", self)
        layout.addWidget(label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

def parse_args():
    parser = argparse.ArgumentParser(description="PyQt6 Application with Command Line Arguments")
    parser.add_argument("--debug", action="store_true", help="Enable debugging mode")
    parser.add_argument("--config", type=str, help="Path to configuration file")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    app = QApplication(sys.argv)

    # Pass parsed arguments to the main window
    window = MainWindow(vars(args))
    window.show()

    sys.exit(app.exec())