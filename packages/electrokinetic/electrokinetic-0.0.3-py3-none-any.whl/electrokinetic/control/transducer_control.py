
import sys

import pyvisa.constants
from PySide6.QtWidgets import (QApplication, QFrame, QMainWindow, QLabel,
                               QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout, QWidget, QStyleFactory, QPushButton)
from PySide6.QtGui import QFont, QColor, Qt
from PySide6.QtCore import QTimer
from pyqt_advanced_slider.advanced_slider import Slider
from siglent import SiglentAWG, create_rm, open_res


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        self.awg = None
        self.setWindowTitle("Transducer Control")
        serifFont = QFont("Times", 10, QFont.Bold)
        sansFont = QFont("Helvetica [Cronyx]", 12)
        main_font = QFont('Segoe UI', 12, QFont.Bold)
        # main_font.setBold(True)
        self.setFont(main_font)

        # frequency slider
        self.sliderFreq = Slider(self)
        self.sliderFreq.setRange(900.0, 1100.0)
        self.sliderFreq.setValue(1000.0)
        self.sliderFreq.setFloat(True)
        self.sliderFreq.setDecimals(0)
        self.sliderFreq.setSuffix(" kHz")
        self.sliderFreq.setSingleStep(10)
        self.sliderFreq.setPageStep(50)
        self.sliderFreq.valueChanged.connect(self.change_frequency)

        # frequency display
        ssLabel = ("QLabel { background-color: rgb(0, 0, 0); "
                   "color: rgb(84, 211, 103);"
                   "font: 700 16pt 'Segoe UI';      }")
        self.lblFreq = QLabel(self)
        self.lblFreq.setStyleSheet(ssLabel)

        # amplitude slider
        self.sliderAmp = Slider(self)
        self.sliderAmp.setRange(0.0, 1000.0)
        self.sliderAmp.setValue(10.0)
        self.sliderAmp.setFloat(True)
        self.sliderAmp.setDecimals(0)
        self.sliderAmp.setSuffix(" mV")
        self.sliderAmp.setSingleStep(10)
        self.sliderAmp.setPageStep(50)
        self.sliderAmp.valueChanged.connect(self.change_amplitude)

        # amplitude display
        self.lblAmp = QLabel(self)
        self.lblAmp.setStyleSheet(ssLabel)

        # cycles slider
        self.sliderCyc = Slider(self)
        self.sliderCyc.setRange(0, 20)
        self.sliderCyc.setValue(10)
        self.sliderCyc.setFloat(False)
        # self.sliderCyc.setDecimals(0)
        self.sliderCyc.setSuffix(" cycles")
        self.sliderCyc.setSingleStep(1)
        self.sliderCyc.setPageStep(5)
        self.sliderCyc.valueChanged.connect(self.change_cycles)

        # cycles display
        self.lblCyc = QLabel(self)
        self.lblCyc.setStyleSheet(ssLabel)

        # repetition slider
        self.sliderRep = Slider(self)
        self.sliderRep.setRange(0, 100)
        self.sliderRep.setValue(10)
        self.sliderRep.setFloat(False)
        # self.sliderRep.setDecimals(0)
        self.sliderRep.setSuffix(" Hz")
        self.sliderRep.setSingleStep(1)
        self.sliderRep.setPageStep(5)
        self.sliderRep.valueChanged.connect(self.change_reprate)

        # repetition display
        self.lblRep = QLabel(self)
        self.lblRep.setStyleSheet(ssLabel)

        # power display
        self.lblPower = QLabel(self)
        self.lblPower.setStyleSheet(ssLabel)

        # buttons
        self.btnConnect = QPushButton("Connect")
        self.btnConnect.pressed.connect(self.connect_awg)

        self.btnDefault = QPushButton("Default")
        self.btnDefault.pressed.connect(self.set_default)
        self.btnOnOff = QPushButton("On")
        self.btnOnOff.pressed.connect(self.switch_on_off)

        # Set slider widths and heights
        self.sliderFreq.setMinimumWidth(240)
        self.sliderFreq.setFixedHeight(24)
        self.lblFreq.setMinimumWidth(160)
        self.lblFreq.setFixedHeight(24)
        self.sliderAmp.setMinimumWidth(240)
        self.sliderAmp.setFixedHeight(24)
        self.lblAmp.setMinimumWidth(160)
        self.lblAmp.setFixedHeight(24)
        self.sliderCyc.setMinimumWidth(240)
        self.sliderCyc.setFixedHeight(24)
        self.lblCyc.setMinimumWidth(160)
        self.lblCyc.setFixedHeight(24)
        self.sliderRep.setMinimumWidth(240)
        self.sliderRep.setFixedHeight(24)
        self.lblRep.setMinimumWidth(160)
        self.lblRep.setFixedHeight(24)

        # grid layout
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(20, 20, 20, 20)
        grid_layout.setSpacing(20)

        grid_layout.addWidget(self.btnConnect, 0, 0)

        grid_layout.addWidget(QLabel("Amplitude"), 1, 0)
        grid_layout.addWidget(self.sliderAmp, 1, 1)
        grid_layout.addWidget(self.lblAmp, 1, 2)

        grid_layout.addWidget(QLabel("Frequency"), 2, 0)
        grid_layout.addWidget(self.sliderFreq, 2, 1)
        grid_layout.addWidget(self.lblFreq, 2, 2)

        grid_layout.addWidget(QLabel("# Cycles"), 3, 0)
        grid_layout.addWidget(self.sliderCyc, 3, 1)
        grid_layout.addWidget(self.lblCyc, 3, 2)

        grid_layout.addWidget(QLabel("Rep. rate"), 4, 0)
        grid_layout.addWidget(self.sliderRep, 4, 1)
        grid_layout.addWidget(self.lblRep, 4, 2)

        grid_layout.addWidget(self.lblPower, 5, 2)
        grid_layout.addWidget(self.btnDefault, 6, 0)
        grid_layout.addWidget(self.btnOnOff, 6, 2)

        # set central widget and layout
        central_widget = QWidget()
        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)

        # self.awg = SiglentAWG()

        self.timer = QTimer()
        # self.timer.timeout.connect(self.awg.query_burst())
        self.timer.setInterval(1000)

    def change_frequency(self, value):
        # Called when sliderFreq value changes
        self.lblFreq.setText(f" {value} kHz")
        self.calc_power()

    def change_amplitude(self, value):
        # Called when sliderAmp value changes
        self.lblAmp.setText(f" {value} mV")
        self.calc_power()

    def change_cycles(self, value):
        # Called when sliderAmp value changes
        self.lblCyc.setText(f" {value} cycles")
        self.calc_power()

    def change_reprate(self, value):
        # Called when sliderAmp value changes
        self.lblRep.setText(f" {value} Hz")
        self.calc_power()

    def calc_power(self):
        p = 125.0
        self.lblPower.setText(f" {p} mW")

    def connect_awg(self):
        self.rm, self.res_list = create_rm()
        for i, r in enumerate(self.res_list):
            print(f"{i}: {r}")
        open_res()
        # self.btnConnect.setAutoFillBa(Qt.GlobalColor.green)
        self.btnConnect.setStyleSheet("background-color: rgb(255, 0, 0);")

    def set_default(self):
        # self.awg.set_default_burst()
        self.sliderAmp.setValue(10.0)     # 10 mV
        # self.sliderFreq.setValue(1000.0)  # 1000 kHz
        # self.sliderCyc.setValue(10)       # 10 cycles
        # self.sliderRep.setValue(10)       # Hz

    def switch_on_off(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()