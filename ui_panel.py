
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLineEdit, QStackedWidget, QLabel,QSlider)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator
import pyqtgraph as pg
import numpy as np
import pyqtgraph.opengl as gl



class Panel(QWidget):

    def __init__(self,min,max,curves,curves_name,call_back_calculation):
        super().__init__()
        
        self.main_layout = QHBoxLayout(self)
        self.left_panel_layout = QVBoxLayout()
        self.left_container = QWidget()
        self.left_container.setMaximumWidth(330)
        self.left_container.setLayout(self.left_panel_layout)

        self.slider_layout = QVBoxLayout()
    
        self.ultimateMenuLayout= QVBoxLayout()
        self.menuLayout = QHBoxLayout()
        self.menuLayout2 = QHBoxLayout()
        self.outputLayout = QHBoxLayout()

        self.Calculation_Widget = QWidget()
        self.Calculation_layout = QVBoxLayout(self.Calculation_Widget)
        self.reversecalcWidget = QWidget()
        self.reversecalcLayout = QVBoxLayout(self.reversecalcWidget)

        self.Calculator_btn=QPushButton("Trap Depth/Power")
        self.reverse_btn=QPushButton("Power")
        self.menuLayout.addWidget(self.Calculator_btn)
        self.menuLayout.addWidget(self.reverse_btn)

        self.coord_label = QLabel("Hover over graph for coordinates")
        self.coord_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Calculation_layout.addWidget(self.coord_label)

        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.Shape.VLine)
        self.divider.setStyleSheet("border: 1px solid #171616;")

        self.Plotter(min,max,curves,curves_name)
        self.action(call_back_calculation)


    def Plotter(self,min,max,curves,curves_name):

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setYRange(min,max)
        my_legend=self.plot_widget.addLegend()
        my_legend.anchor((1,1),(1,1))
        self.curve_list = []
        for color,name in zip(curves,curves_name):
            curve =self.plot_widget.plot(pen=color,name=name) 
            self.curve_list.append(curve)
        

    def three_dimensional_Plotter(self,X,Y,Z,button1_name,button2_name):

        self.view = gl.GLViewWidget()
        self.plotting_stack= QStackedWidget()

        self.button1 =QPushButton(button1_name)
        self.button2 =QPushButton(button2_name)

        self.button1.clicked.connect(lambda:self.plotting_stack.setCurrentIndex(0))
        self.button2.clicked.connect(lambda:self.plotting_stack.setCurrentIndex(1))

        x_max = np.max(np.abs(X)) if X is not None else 1
        y_max = np.max(np.abs(Y)) if Y is not None else 1
        z_max = np.max(np.abs(Z)) if Z is not None else 1

        grid_xy = gl.GLGridItem()
        grid_xy = gl.GLGridItem(color=(255, 255, 255, 150))
        grid_xy.setSize(x_max * 2, y_max * 2, z_max * 2)
        grid_xy.setSpacing(x_max / 5, y_max / 5, z_max / 5)
        self.view.addItem(grid_xy)

        grid_zx = gl.GLGridItem()
        grid_zx = gl.GLGridItem(color=(255, 255, 255, 150))
        grid_zx.setSize(x_max * 2, y_max * 2, z_max * 2) 
        grid_zx.setSpacing(x_max / 5, y_max / 5, z_max / 5)

        grid_zx.rotate(90, 1, 0, 0)
        self.view.addItem(grid_zx)

        x_axis = gl.GLLinePlotItem(pos=np.array([[-1*x_max,0,0], [x_max,0,0]]), color=(1.0, 0.2, 0.2, 1.0), width=3)
        y_axis = gl.GLLinePlotItem(pos=np.array([[0,-1*y_max,0], [0,y_max,0]]), color=(0.2, 1.0, 0.2, 1.0), width=3)
        z_axis = gl.GLLinePlotItem(pos=np.array([[0,0,-1*z_max], [0,0,z_max]]), color=(207/255, 204/255, 31/255, 1.0), width=3)
        
        self.view.addItem(x_axis)
        self.view.addItem(y_axis)
        self.view.addItem(z_axis)
        self.view.setCameraPosition(distance=300e-6, elevation=30, azimuth=45)

        z_max = np.max(Z)
        z_min =np.min(Z)

        if z_max<z_min:
            colour_math = (z_max-Z)/(z_max-z_min)
        else:
            colour_math = np.zeros_like(Z)

        surface_colours =pg.colormap.get('viridis').map(colour_math) 
        self.surface_plot =gl.GLSurfacePlotItem(x=X,y=Y,z=Z,shader='shaded',colors = surface_colours ) 
        

        self.plotting_stack.addWidget(self.plot_widget)
        self.plotting_stack.addWidget(self.view)
        self.menuLayout2.addWidget(self.button1)
        self.menuLayout2.addWidget(self.button2)
        self.view.addItem(self.surface_plot)
        self.main_layout.addWidget(self.plotting_stack)

        
    
    def action(self,call_back_calculation):

        stack =QStackedWidget()

        self.init_value = QLineEdit()
        self.final_value = QLineEdit()

        self.init_value.setPlaceholderText("Min")
        self.final_value.setPlaceholderText("Max")

        number_validator = QDoubleValidator()

        self.init_value.setValidator(number_validator)
        self.final_value.setValidator(number_validator)    

        self.result_button = QPushButton("Calculate")
        self.result_button.clicked.connect(call_back_calculation)
        self.result_label1= QLabel("")
        self.result_label2 =QLabel("")

        self.reversecalcLayout.addWidget(self.init_value)
        self.reversecalcLayout.addWidget(self.final_value)
        self.reversecalcLayout.addWidget(self.result_button)
        self.reversecalcLayout.addWidget(self.result_label1)
        self.reversecalcLayout.addWidget(self.result_label2)

        stack.addWidget(self.Calculation_Widget)
        stack.addWidget(self.reversecalcWidget)
        self.outputLayout.addWidget(stack)

        self.Calculator_btn.clicked.connect(lambda:stack.setCurrentIndex(0))
        self.reverse_btn.clicked.connect(lambda:stack.setCurrentIndex(1))

        self.ultimateMenuLayout.addLayout(self.menuLayout)
        self.ultimateMenuLayout.addLayout(self.menuLayout2)

        self.left_panel_layout.addLayout(self.slider_layout)
        self.left_panel_layout.addLayout(self.ultimateMenuLayout)
        self.left_panel_layout.addLayout(self.outputLayout)

        self.main_layout.addWidget(self.left_container)
        self.main_layout.addWidget(self.divider)
        

        
    def add_slider(self,minimum,maximum,singleIncrement,call_back_function,upper_label,lower_label):

        slider = QSlider(Qt.Orientation.Horizontal)
        individual_slider_layout = QHBoxLayout()

        slider.setMinimum(minimum)
        slider.setMaximum(maximum)

        slider_Upper_label = QLabel(str(upper_label))
        slider_Lower_label = QLabel(str(lower_label))

        if singleIncrement:            
            slider.setSingleStep(1)
            slider.setPageStep(1)
            slider.setTickPosition(QSlider.TickPosition.TicksRight)
            slider.setTickInterval(1)

        slider.valueChanged.connect(call_back_function)

        slider_Upper_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        individual_slider_layout.addWidget(slider_Upper_label)

        individual_slider_layout.addWidget(slider,alignment=Qt.AlignmentFlag.AlignHCenter)

        individual_slider_layout.addWidget(slider_Lower_label)
        slider_Lower_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.slider_layout.addLayout(individual_slider_layout)

        return slider, slider_Lower_label






