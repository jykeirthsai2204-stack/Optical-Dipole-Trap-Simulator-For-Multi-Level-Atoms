import sys
import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow, QSlider, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt

class SineWaveApp(QMainWindow): 
     
    def __init__(self):
        super().__init__()

        self.x = np.linspace(1,100,1000)

        main_layout = QVBoxLayout()
        container =QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.win = pg.GraphicsLayoutWidget()
        self.plot1 = self.win.addPlot(row =0,col =0)
        self.plot2 = self.win.addPlot(row =0,col =1)       
        self.curve1 =self.plot1.plot(pen='y')
        self.curve2 =self.plot2.plot(pen ='b')
        main_layout.addWidget(self.win)
        self.plot1.setXRange(1,100)
        self.plot2.setXRange(1,100)
        self.plot1.setYRange(-20,20)
        self.plot2.setYRange(-20,20)

        slider_layout = QVBoxLayout()
        main_layout.addLayout(slider_layout)
        self.freq_slider = QSlider(Qt.Orientation.Vertical)
        self.amp_slider = QSlider(Qt.Orientation.Vertical)
        self.freq_slider.setMinimum(1)
        self.freq_slider.setMaximum(50)
        self.freq_slider.setMaximumHeight(100)
        self.freq_slider.valueChanged.connect(self.Update)

        self.amp_slider.setMinimum(1)
        self.amp_slider.setMaximum(20)
        self.amp_slider.setMaximumHeight(100)
        self.amp_slider.valueChanged.connect(self.Update)

        slider_layout.addWidget(QLabel("F"))
        slider_layout.addWidget(self.freq_slider)
        
        slider_layout.addWidget(QLabel("Amp"))
        slider_layout.addWidget(self.amp_slider)


        self.coor_label =QLabel("x: ,y: ")
        main_layout.addWidget(self.coor_label)

        self.plot1.scene().sigMouseMoved.connect(self.mouse_moved)
        self.plot2.scene().sigMouseMoved.connect(self.mouse_moved)
        self.Update
        self.mouse_moved

        self.vline=pg.InfiniteLine(angle =90,movable=False)
        self.hline=pg.InfiniteLine(angle =0,movable=False)
        self.plot1.addItem(self.vline)
        self.plot1.addItem(self.hline)
        
        self.vline1=pg.InfiniteLine(angle =90,movable=False)
        self.hline1=pg.InfiniteLine(angle =0,movable=False)
        self.plot2.addItem(self.vline1)
        self.plot2.addItem(self.hline1)



    def Update(self):
        freq = self.freq_slider.value()
        amp = self.amp_slider.value()
        y1 =np.cos(2*np.pi*freq*self.x)
        y2 =amp*np.sin(2*np.pi*freq*self.x)

        self.curve1.setData(self.x,y1)
        self.curve2.setData(self.x,y2)

    def mouse_moved(self,pos):
        for plot,vline,hline in [(self.plot1,self.vline,self.hline),(self.plot2,self.vline1,self.hline1)]:
            if plot.sceneBoundingRect().contains(pos):
                mouse_cord =plot.vb.mapSceneToView(pos)
                x =mouse_cord.x()
                y =mouse_cord.y()
                self.vline.setPos(x)
                self.hline.setPos(y)
                self.vline1.setPos(x)
                self.hline1.setPos(y)
                self.coor_label.setText(f"x: {x:.3f}   y: {y:.3f}")








app = QApplication(sys.argv)
window = SineWaveApp()
window.show()
app.exec()
