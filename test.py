from PyQt5 import QtCore, QtGui,QtWidgets
import sys
from PyQt5.QtChart import QChart, QChartView,QPieSeries
from PyQt5.QtGui import QPainter,QPen
from PyQt5.QtCore import Qt




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(530, 382)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.button1 = QtWidgets.QPushButton(self.centralwidget)
        self.button1.setGeometry(QtCore.QRect(0, 90, 141, 31))
        self.button1.setObjectName("button1")
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(70, 60, 111, 16))
        self.label1.setObjectName("label1")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 530, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button1.setText(_translate("MainWindow", "Press Me"))
        self.label1.setText(_translate("MainWindow", "Hello My Name is Josh"))
        self.button1.clicked.connect(self.clicked)
        self.menuFile.setTitle(_translate("MainWindow", "File"))

    def clicked(self):
        self.label1.setText("you pressed me button sir!")
        self.update()
        print("clicked")

    def update(self):
        self.label1.adjustSize()

    def create_piechart(self):
        series = QPieSeries()
        series.append("Python",80)
        series.append("C++",70)
        series.append("Java",50)
        series.append("C#",80)
        series.append("PHP",70)
        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Programming Pie Chart")
        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(chartview)

         
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.create_piechart()
    MainWindow.show()
    sys.exit(app.exec_())
