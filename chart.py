from PyQt5 import QtChart,QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtChart import QChart, QChartView
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
import pprint

pp = pprint.PrettyPrinter(indent=4)



class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQtChart Pie Chart")
        self.setGeometry(20,200, 1120,600)
        self.show()
        self.create_piechart()

    def create_piechart(self):

        data = {
            "Python": (80,QtGui.QColor("red")),
            "C++": (70,QtGui.QColor("orange")),
            "Java": (50,QtGui.QColor("yellow")),
            "C#": (40,QtGui.QColor("green")),
            "PHP": (30,QtGui.QColor("blue")),
        }

        series = QtChart.QPieSeries()
 
        for name, (value,color) in data.items():
            _slice = series.append(name,value)
            _slice.setBrush(color)

        series.setLabelsVisible(True)
        series.setLabelsPosition(QtChart.QPieSlice.LabelOutside)
        for slice in series.slices():
            slice.setLabel("{:.2f}%".format(100 * slice.percentage()))
       
        chart = QChart()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Pie Chart Example")
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        count = 0
        for name, (value,color) in data.items():
            chart.legend().markers(series)[count].setLabel(name)
            count += 1

        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chartview)

App = QApplication(sys.argv)
window = Window()


sys.exit(App.exec_())