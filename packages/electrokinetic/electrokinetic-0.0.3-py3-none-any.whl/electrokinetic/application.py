
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QVBoxLayout,
                               QGraphicsView, QGraphicsScene,
                               QButtonGroup)
from PySide6.QtCore import Qt

from electrokinetic.gui.ui_mainwindow import Ui_MainWindow
# from electrokinetic.classes.segmentdialog import SegmentDialog

# from electrokinetic.classes.heatnet import *
# from electrokinetic.classes.tables.shtable import SHTable
# from electrokinetic.classes.views.heatview import ViewWidget, HeatView
# from electrokinetic.classes.scenes.basicscene import BasicScene
# from electrokinetic.classes.scenes.poly_scene import PolyScene

import logging
# https://coderscratchpad.com/pyqt6-handling-command-line-arguments/


class MainWindow(QMainWindow):
    def __init__(self, args):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.modegroup = QButtonGroup(self)
        self.modegroup.addButton(self.ui.rbLOPF, 0)
        self.modegroup.addButton(self.ui.rbLPF, 1)
        self.modegroup.addButton(self.ui.rbPF, 2)
        self.modegroup.setExclusive(True)
        self.modegroup.idClicked.connect(self.set_mode)
        self.ui.rbLOPF.click()
        print(f"Mode: {self.mode}")
        self.ui.label.setText(f"Arguments: {args}")

        # self.setWindowTitle("Basic Command Line Arguments")
        # self.setGeometry(100, 100, 400, 300)
        # layout = QVBoxLayout()

        # Display command line arguments
        # label = QLabel(f"Arguments: {args}", self)
        # layout.addWidget(label)

        # container = QWidget()
        # container.setLayout(layout)
        # self.setCentralWidget(container)

    # mode commands
    def set_mode(self, button_id):
        match button_id:
            case 0:
                print("Setting mode to Linear Optimal Power Flow (LOPF)")
                self.mode = "LOPF"
            case 1:
                print("Setting mode to Linear Power Flow (LPF)")
                self.mode = "LPF"
            case 2:
                print("Setting mode to Power Flow (PF)")
                self.mode = "PF"
            case _:
                print("Mode is not defined")

    def closeEvent(self, event):
        logging.info("Closing application")
        event.accept()
        qApp.closeAllWindows()
        # sys.exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('IVP Control')
    # Pass command line arguments to the main window
    window = MainWindow(sys.argv[1:])
    window.setWindowTitle(app.applicationName())
    window.show()
    sys.exit(app.exec())

