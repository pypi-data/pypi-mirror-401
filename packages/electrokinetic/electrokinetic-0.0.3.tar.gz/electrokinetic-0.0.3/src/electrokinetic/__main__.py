from electrokinetic.application import MainWindow

print(f"executing {__file__}")
from electrokinetic.application import *

app = QApplication(sys.argv)
app.setApplicationName('IVP Control')
window = MainWindow(sys.argv[1:])
window.setWindowTitle(app.applicationName())
window.show()
app.exec()