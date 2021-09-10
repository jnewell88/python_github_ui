from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import os

def window():
	app = QApplication(sys.argv)
	win = QMainWindow()
	#0,0 = top left x,y, width, height
	win.setGeometry(200,200,300,300)
	win.setWindowTitle("Github Analyser")

	label = QtWidgets.QLabel(win)
	label.setText("my first label")
	label.move(50,50)
	os.path.dirname(sys.executable)
	win.show()
	sys.exit(app.exec_())
	
window()