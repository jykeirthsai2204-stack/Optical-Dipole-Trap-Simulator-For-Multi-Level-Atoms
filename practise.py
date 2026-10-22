import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QSlider,QPushButton,QComboBox
import pyqtgraph as pg
import numpy as np
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WAVES")
        self.resize(600, 400)
        

        self.layout1 =QVBoxLayout()
        container = QWidget()
        container.setLayout(self.layout1)
        self.setCentralWidget(container)

        self.atom_data = {"Rubidium-87":{"mass":1.45e-25,"Polarizability":5.3e-39},
                          "sodium-23":{"mass":3.8192e-26,"Polarizability":2.4e-39},
                          "potassium-40":{"mass":6.6422e-26,"Polarizability":3.8e-39}}
        
        self.drop_down =QComboBox()
        self.drop_down.addItems(list(self.atom_data.keys()))
        self.drop_down.currentIndexChanged.connect(self.Update)
        self.drop_down.setMinimumWidth(120)
        self.drop_down.setMaximumWidth(300)
        self.layout1.addWidget(self.drop_down)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setYRange(0,5.3e-37)
        self.curve = self.plot_widget.plot(pen="y")
        self.layout1.addWidget(self.plot_widget)

        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.layout1.addWidget(self.slider)
        self.slider.valueChanged.connect(self.Update)
        self.layout1.addWidget(self.slider)

        self.button = QPushButton("Reset")
        self.button.clicked.connect(self.Reset)
        self.button.setFixedSize(80, 30)
        self.layout1.addWidget(self.button)


        self.Update()
        self.Reset()

    def Update(self):
        key = self.drop_down.currentText()
        polarizability= self.atom_data[key]["Polarizability"]
        self.max_power = self.slider.value()
        power_array = np.linspace(0,self.max_power,200)
        trap_depth = power_array*polarizability
        self.curve.setData(power_array,trap_depth)

    def Reset(self):
        self.slider.setValue(1)
        


        



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()