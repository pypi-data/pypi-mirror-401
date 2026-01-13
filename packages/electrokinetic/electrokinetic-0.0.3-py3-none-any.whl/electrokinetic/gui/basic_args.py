
# https://coderscratchpad.com/pyqt6-handling-command-line-arguments/

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self, args):
        super().__init__()
        self.setWindowTitle("Basic Command Line Arguments")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Display command line arguments
        label = QLabel(f"Arguments: {args}", self)
        layout.addWidget(label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Pass command line arguments to the main window
    window = MainWindow(sys.argv[1:])
    window.show()

    sys.exit(app.exec())