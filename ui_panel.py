
import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import  QSlider, QVBoxLayout, QWidget, QLabel,QTabWidget,QHBoxLayout,QFrame,QPushButton,QLineEdit,QStackedWidget
from PyQt6.QtCore import Qt
from scipy import constants
from PyQt6.QtGui import QDoubleValidator
 

def Panel(self,curves,curves_name,Sliders,min,max,call_back_calculation):
        
    curvelist =[]
    Sliders_list = []
    Lower_label_list=[]
    Power_values_list=[]
    result_labels_list = []
        

    self.main_layout = QHBoxLayout()
    self.container = QWidget()
    self.container.setLayout(self.main_layout)

    self.left_panel_layout = QVBoxLayout()
    left_container = QWidget()
    left_container.setMaximumWidth(330)
    left_container.setLayout(self.left_panel_layout)

    self.slider_layout = QVBoxLayout()
    self.menuLayout = QHBoxLayout()
    self.outputLayout = QHBoxLayout()

    self.Calculation_Widget = QWidget()
    self.Calculation_layout = QVBoxLayout(self.Calculation_Widget)
    self.reversecalcWidget = QWidget()
    self.reversecalcLayout = QVBoxLayout(self.reversecalcWidget)
        

    self.plot_widget = pg.PlotWidget()
    self.plot_widget.setYRange(min,max)
    my_legend=self.plot_widget.addLegend()
    my_legend.anchor((1,1),(1,1))

    Calculator_btn=QPushButton("Trap Depth/Power")
    reverse_btn=QPushButton("Power")
    self.menuLayout.addWidget(Calculator_btn)
    self.menuLayout.addWidget(reverse_btn)
    
    coord_label = QLabel("Hover over graph for coordinates")
    coord_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.Calculation_layout.addWidget(coord_label)

    divider = QFrame()
    divider.setFrameShape(QFrame.Shape.VLine)
    divider.setStyleSheet("border: 1px solid #171616;")

    stack =QStackedWidget()

    init_value = QLineEdit()
    final_value = QLineEdit()
    init_value.setPlaceholderText("Min")
    final_value.setPlaceholderText("Max")
    number_validator = QDoubleValidator()
    init_value.setValidator(number_validator)
    final_value.setValidator(number_validator)

    Power_values_list.append(init_value)
    Power_values_list.append(final_value)

    self.result_button = QPushButton("Calculate")
    self.result_button.clicked.connect(call_back_calculation)
    result_label1= QLabel("")
    result_label2 =QLabel("")


    self.reversecalcLayout.addWidget(init_value)
    self.reversecalcLayout.addWidget(final_value)
    self.reversecalcLayout.addWidget(self.result_button)
    self.reversecalcLayout.addWidget(result_label1)
    self.reversecalcLayout.addWidget(result_label2)

    result_labels_list.append(result_label1)
    result_labels_list.append(result_label2)

    stack.addWidget(self.Calculation_Widget)
    stack.addWidget(self.reversecalcWidget)
    self.outputLayout.addWidget(stack)

    Calculator_btn.clicked.connect(lambda:stack.setCurrentIndex(0))
    reverse_btn.clicked.connect(lambda:stack.setCurrentIndex(1))



    self.left_panel_layout.addLayout(self.slider_layout)
    self.left_panel_layout.addLayout(self.menuLayout)
    self.left_panel_layout.addLayout(self.outputLayout)

    self.main_layout.addWidget(left_container)
    self.main_layout.addWidget(divider)
    self.main_layout.addWidget(self.plot_widget)

    for color,name in zip(curves,curves_name):
        curve =self.plot_widget.plot(pen=color,name=name) 
        curvelist.append(curve)


    for config in Sliders:
        minimum,maximum,singleIncrement,call_back_funcion,upper_label,lower_label=config

        slider = QSlider(Qt.Orientation.Horizontal)
        indvidual_slider_layout= QHBoxLayout()
        self.slider_layout.addLayout(indvidual_slider_layout)

        slider.setMinimum(minimum)
        slider.setMaximum(maximum)

        Upper_label = QLabel(str(upper_label))
        Lower_label= QLabel(str(lower_label))

        if singleIncrement:
            slider.setSingleStep(1)
            slider.setPageStep(1)
            slider.setTickPosition(QSlider.TickPosition.TicksRight)
            slider.setTickInterval(1)

        slider.valueChanged.connect(call_back_funcion)

        Upper_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        indvidual_slider_layout.addWidget(Upper_label)

        indvidual_slider_layout.addWidget(slider,alignment=Qt.AlignmentFlag.AlignHCenter)

        Lower_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        indvidual_slider_layout.addWidget(Lower_label)

        Lower_label_list.append(Lower_label)
        Sliders_list.append(slider)

    

    return self.container,curvelist,Sliders_list,Lower_label_list,self.plot_widget,coord_label,Power_values_list,result_labels_list



