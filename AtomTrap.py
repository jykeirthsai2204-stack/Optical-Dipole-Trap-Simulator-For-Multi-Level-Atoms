import sys
import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow, QSlider, QVBoxLayout, QWidget, QLabel,QTabWidget,QHBoxLayout,QFrame,QPushButton,QLineEdit,QStackedWidget
from PyQt6.QtCore import Qt
from scipy import constants
from PyQt6.QtGui import QDoubleValidator

from Physics import Trap_Dept, Scattering_Rate,Power_calculator_function
from ui_panel import Panel

class AtomTrapApp(QMainWindow): 
                    
    def __init__(self):
        super().__init__()
        tabs = QTabWidget()
        self.Power = np.linspace(0,300,300)
        self.Beam_waist = 3e-6
        self.intensity = (2*self.Power*1e-3)/(np.pi*(self.Beam_waist**2))
        self.C = constants.c
        self.ħ= constants.hbar
        self.K_B= constants.k
        

        slider_config = [(700,1064,False,self.Update1,"λ(nm)",700),(-1,1,True,self.Update1,"P",0),(-1,1,True,self.Update1,"F=1",0),(-2,2,True,self.Update1,"F=2",0)]
        slider_config2 = [(700,1064,False,self.Update2,"λ(nm)",700),(-1,1,True,self.Update2,"P",0),(-1,1,True,self.Update2,"F=1",0),(-2,2,True,self.Update2,"F=2",0)]

        container1,curve,sliders1,slider1_lowerlabel,self.plot1,self.coord_label_tab1,Power_values1,label_list1=Panel(self,["b","#66B2FF"],["F=1","F=2"],slider_config,0,5792e-6,self.Power_calculation)
        container2,curve_2,sliders2,slider2_lowerlabel,self.plot2,self.coord_label_tab2,Power_values2,label_list2=Panel(self,["b","#66B2FF"],["F=1","F=2"],slider_config2,0 ,95,self.Power_calculation)

        self.min_power_value= Power_values1[0]
        self.max_power_value= Power_values1[1]

        self.label1 =label_list1[0]
        self.label2 = label_list1[1]       

        self.wavelength_slider = sliders1[0]
        self.wavelength_Lower_label = slider1_lowerlabel[0]

        self.Polarisation_slider = sliders1[1]
        self.Polarisation_Lower_label = slider1_lowerlabel[1]

        self.Mf1_slider = sliders1[2]
        self.Mf1_Lower_label = slider1_lowerlabel[2]

        self.Mf2_slider = sliders1[3]
        self.Mf2_Lower_label = slider1_lowerlabel[3]

        self.curve1 = curve[0]
        self.curve2 = curve[1]

        self.wavelength_slider2 = sliders2[0]
        self.wavelength_Lower_label2 = slider2_lowerlabel[0]

        self.Polarisation_slider2 = sliders2[1]
        self.Polarisation_Lower_label2 = slider2_lowerlabel[1]

        self.Mf1_slider2 = sliders2[2]
        self.Mf1_Lower_label2 = slider2_lowerlabel[2]

        self.Mf2_slider2 = sliders2[3]
        self.Mf2_Lower_label2 = slider2_lowerlabel[3]

        self.curve_SR1 = curve_2[0]
        self.curve_SR2 = curve_2[1]

        self.proxy1 = pg.SignalProxy(self.plot1.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved_tab1)
        self.proxy2 = pg.SignalProxy(self.plot2.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved_tab2)

        tabs.addTab(container1,"Trap Depth")
        tabs.addTab(container2,"Scattering Rate")
        self.setCentralWidget(tabs)
        self.Update1()
        self.Update2()
        self.Power_calculation()


    def Update1(self):
        laser_Polarisation = self.Polarisation_slider.value()
        self.Polarisation_Lower_label.setText(f"{laser_Polarisation}")

        Wavelength = self.wavelength_slider.value()*1e-9
        self.wavelength_Lower_label.setText(f"{self.wavelength_slider.value()}")

        if Wavelength>=780.241*1e-9:
            self.plot1.setYRange(-5792e-6,0)
            self.curve1.setPen('r')
            self.curve2.setPen('#FF7F7F')
        else:
            self.plot1.setYRange(0,5792e-6)
            self.curve1.setPen('b')
            self.curve2.setPen('#66B2FF')

        Mf1 = self.Mf1_slider.value()
        self.Mf1_Lower_label.setText(f"mf={Mf1}")

        Mf2 = self.Mf2_slider.value()
        self.Mf2_Lower_label.setText(f"mf={Mf2}")

        TrapDepth1 = Trap_Dept(3.610e7,3.811e7,2.369e15,2.415e15,laser_Polarisation,-0.5,Mf1,Wavelength,self.intensity)
        TrapDepth2 = Trap_Dept(3.610e7,3.811e7,2.369e15,2.415e15,laser_Polarisation,0.5,Mf2,Wavelength,self.intensity)

        self.curve1.setData(self.Power,TrapDepth1)
        self.curve2.setData(self.Power,TrapDepth2)

    
    def Update2(self):
        laser_Polarisation = self.Polarisation_slider2.value()
        self.Polarisation_Lower_label2.setText(f"{laser_Polarisation}")
        
        Wavelength = self.wavelength_slider2.value()*1e-9
        self.wavelength_Lower_label2.setText(f"{self.wavelength_slider2.value()}")

        if Wavelength>=780.241*1e-9:
            self.curve_SR1.setPen('r')
            self.curve_SR2.setPen('#FF7F7F')
        else:
            self.curve_SR1.setPen('b')
            self.curve_SR2.setPen('#66B2FF')

        Mf1 = self.Mf1_slider2.value()
        self.Mf1_Lower_label2.setText(f"mf={Mf1}")

        Mf2 = self.Mf2_slider2.value()
        self.Mf2_Lower_label2.setText(f"mf={Mf2}")

        ScatteringRate1 = Scattering_Rate(3.610e7,3.811e7,2.369e15,2.415e15,laser_Polarisation,-0.5,Mf1,Wavelength,self.intensity)
        ScatteringRate2 = Scattering_Rate(3.610e7,3.811e7,2.369e15,2.415e15,laser_Polarisation,0.5,Mf2,Wavelength,self.intensity)

        self.curve_SR1.setData(self.Power,ScatteringRate1)
        self.curve_SR2.setData(self.Power,ScatteringRate2)

    def Power_calculation(self):
        laser_Polarisation = self.Polarisation_slider.value()
        Wavelength = self.wavelength_slider.value()*1e-9
        Mf1 = self.Mf1_slider.value()
        Mf2 = self.Mf2_slider.value()
        
        Trap_depth1 = self.min_power_value.text()
        Trap_depth2 = self.max_power_value.text()
        if Trap_depth1 and Trap_depth2:
            min = float(Trap_depth1)
            max = float(Trap_depth2)
            Power_reverse_calculated_value_11= Power_calculator_function(3.610e7,3.811e7,2.369e15,2.415e15,laser_Polarisation,-0.5,Mf1,Wavelength,self.Beam_waist,min)
            Power_reverse_calculated_value_12= Power_calculator_function(3.610e7,3.811e7,2.369e15,2.415e15,laser_Polarisation,-0.5,Mf1,Wavelength,self.Beam_waist,max)

            Power_reverse_calculated_value_21= Power_calculator_function(3.610e7,3.811e7,2.369e15,2.415e15,laser_Polarisation,0.5,Mf2,Wavelength,self.Beam_waist,min)
            Power_reverse_calculated_value_22= Power_calculator_function(3.610e7,3.811e7,2.369e15,2.415e15,laser_Polarisation,0.5,Mf2,Wavelength,self.Beam_waist,max)

            self.label1.setText(f"Power[F=1] : {Power_reverse_calculated_value_11:.3f}(mW) To {Power_reverse_calculated_value_12:.3f}(mW)")
            self.label2.setText(f"Power[F=2] : {Power_reverse_calculated_value_21:.3f}(mW) To {Power_reverse_calculated_value_22:.3f}(mW)")
        else:
            self.label1.setText("Please enter values!")
            self.label2.setText("")



    def mouse_moved_tab1(self, event):
        pos = event[0]  
        
        if self.plot1.sceneBoundingRect().contains(pos):
            
            mouse_point = self.plot1.plotItem.vb.mapSceneToView(pos)
            
            
            self.coord_label_tab1.setText(f"Trap Depth Graph\n | Power: {mouse_point.x():.2f}(mW)| \n | Depth: {mouse_point.y()*1e3:.2f}(mK)|")

    def mouse_moved_tab2(self, event):
        pos = event[0]
        if self.plot2.sceneBoundingRect().contains(pos):
            mouse_point = self.plot2.plotItem.vb.mapSceneToView(pos)
            self.coord_label_tab2.setText(f"Scattering Rate Graph\n | Power: {mouse_point.x():.2f}(mW)|\n | Rate: {mouse_point.y():.2f}|")
                



        


app = QApplication(sys.argv)
window = AtomTrapApp()
window.show()
app.exec()
