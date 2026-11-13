import sys
import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow, QSlider, QVBoxLayout, QWidget, QLabel,QTabWidget,QHBoxLayout,QFrame,QPushButton,QLineEdit,QStackedWidget
from PyQt6.QtCore import Qt, QTimer
from scipy import constants
from PyQt6.QtGui import QDoubleValidator

from Physics import Trap_Dept, Scattering_Rate,Power_calculator_function, Crossed_Beam_TrapDepth,Intensity
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
        limit = 4*self.Beam_waist

############################################ (Slider creation, Plot creation, Panel creation) ###################################################################################

        slider_config = [(850,1064,False,self.Dual_Update,"λ(nm)",700),(-1,1,True,self.Dual_Update,"P",0),(-1,1,True,self.Dual_Update,"F=1",0),(-2,2,True,self.Dual_Update,"F=2",0),(0,300,False,self.Heavy_math,"Power",0)]
        slider_config2 = [(700,1064,False,self.Update2,"λ(nm)",700),(-1,1,True,self.Update2,"P",0),(-1,1,True,self.Update2,"F=1",0),(-2,2,True,self.Update2,"F=2",0)]

        self.tab1=Panel(0,5792e-6,["b","#66B2FF"],["F=1","F=2"],self.Power_calculation)

        slider1_1=self.tab1.add_slider(*slider_config[0])
        slider1_2=self.tab1.add_slider(*slider_config[1])
        slider1_3=self.tab1.add_slider(*slider_config[2])
        slider1_4=self.tab1.add_slider(*slider_config[3])
        slider1_5=self.tab1.add_slider(*slider_config[4])


        self.tab2=Panel(0 ,95,["b","#66B2FF"],["F=1","F=2"],self.Power_calculation)
        slider2_1=self.tab2.add_slider(*slider_config2[0])
        slider2_2=self.tab2.add_slider(*slider_config2[1])
        slider2_3=self.tab2.add_slider(*slider_config2[2])
        slider2_4=self.tab2.add_slider(*slider_config2[3])


        self.min_power_value= self.tab1.init_value
        self.max_power_value= self.tab1.final_value

        self.label1 =self.tab1.result_label1
        self.label2 = self.tab1.result_label2        

        self.wavelength_slider,self.wavelength_Lower_label = slider1_1
        self.Polarisation_slider,self.Polarisation_Lower_label= slider1_2 
        self.Mf1_slider,self.Mf1_Lower_label = slider1_3
        self.Mf2_slider,self.Mf2_Lower_label = slider1_4
        self.Power_slider,self.Power_slider_Lower_label = slider1_5 

        self.Trap_depth_curve1 = self.tab1.curve_list[0]
        self.Trap_depth_curve2 = self.tab1.curve_list[1]

        self.wavelength_slider2,self.wavelength_Lower_label2=slider2_1 
        self.Polarisation_slider2 ,self.Polarisation_Lower_label2 = slider2_2
        self.Mf1_slider2,self.Mf1_Lower_label2 =slider2_3
        self.Mf2_slider2,self.Mf2_Lower_label2 =slider2_4

        self.scattering_rate_curve1 = self.tab2.curve_list[0]
        self.scattering_rate_curve2 = self.tab2.curve_list[1]

###################################################################################################################################################################################################

        self.proxy1 = pg.SignalProxy(self.tab1.plot_widget.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved_tab1)
        self.proxy2 = pg.SignalProxy(self.tab2.plot_widget.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved_tab2)

        rayeligh_range = (np.pi*(self.Beam_waist**2))/(self.wavelength_slider.value()*1e-9)

        self.Propaxis_range = np.linspace(-limit, limit, 100)
        self.Transverse_range1 = np.linspace(-limit, limit, 100)
        self.Transverse_range2 = np.linspace(-limit, limit, 100)

        tabs.addTab(self.tab1,"Trap Depth")
        tabs.addTab(self.tab2,"Scattering Rate")
        self.setCentralWidget(tabs)
        _,_,z = self.Crossed_beam_math(self.Propaxis_range,self.Transverse_range1,self.Transverse_range2,self.Beam_waist,self.wavelength_slider.value()*1e-9,self.Power_slider.value()*1e-3,self.Polarisation_slider.value(),self.Mf1_slider.value())
        self.tab1.three_dimensional_Plotter(self.Propaxis_range,self.Transverse_range1,z,"2D","3D")
        self.Dual_Update()
        self.Update2()
        self.Power_calculation()
        QTimer.singleShot(100, self.preload_3d)

    def Dual_Update(self):
        self.Update1()
        self.Heavy_math()

    def preload_3d(self):

        self.tab1.plotting_stack.setCurrentIndex(1)
        QApplication.processEvents()
        self.tab1.plotting_stack.setCurrentIndex(0)

    def Crossed_beam_math(self,x,y,z,beam_waist,Wavelength,Power,laser_Polarisation,Mf1):

        X,Y = np.meshgrid(x,y)
        
        x_intensity = Intensity(beam_waist,Wavelength,Power,X,Y,0.0)
        y_intensity = Intensity(beam_waist,Wavelength,Power,Y,X,0.0)
        
              
        
        
        Total_intensity = x_intensity + y_intensity
        Z_value= Crossed_Beam_TrapDepth(3.610e7,3.811e7,2.369e15,2.415e15,laser_Polarisation,laser_Polarisation,-0.5,Mf1,Wavelength,Total_intensity)
        
        
        return X,Y,Z_value
        
    def Update1(self):

        laser_Polarisation = self.Polarisation_slider.value()
        self.Polarisation_Lower_label.setText(f"{laser_Polarisation}")

        Wavelength = self.wavelength_slider.value()*1e-9
        self.wavelength_Lower_label.setText(f"{self.wavelength_slider.value()}")
        

        if Wavelength>=780.241*1e-9:
            self.tab1.plot_widget.setYRange(-5792e-6,0)
            self.Trap_depth_curve1.setPen('r')
            self.Trap_depth_curve2.setPen('#FF7F7F')
        else:
            self.tab1.plot_widget.setYRange(0,5792e-6)
            self.Trap_depth_curve1.setPen('b')
            self.Trap_depth_curve2.setPen('#66B2FF')

        Mf1 = self.Mf1_slider.value()
        self.Mf1_Lower_label.setText(f"mf={Mf1}")

        Mf2 = self.Mf2_slider.value()
        self.Mf2_Lower_label.setText(f"mf={Mf2}")

        TrapDepth1 = Trap_Dept(3.610e7,3.811e7,2.369e15,2.415e15,laser_Polarisation,-0.5,Mf1,Wavelength,self.intensity)
        TrapDepth2 = Trap_Dept(3.610e7,3.811e7,2.369e15,2.415e15,laser_Polarisation,0.5,Mf2,Wavelength,self.intensity)
        

        self.Trap_depth_curve1.setData(self.Power,TrapDepth1)
        self.Trap_depth_curve2.setData(self.Power,TrapDepth2)
        

    def Heavy_math(self):
        
        laser_Polarisation = self.Polarisation_slider.value()
        self.Polarisation_Lower_label.setText(f"{laser_Polarisation}")

        Wavelength = self.wavelength_slider.value()*1e-9
        self.wavelength_Lower_label.setText(f"{self.wavelength_slider.value()}")
        
        Mf1 = self.Mf1_slider.value()
        self.Mf1_Lower_label.setText(f"mf={Mf1}")

        Power = self.Power_slider.value()
        self.Power_slider_Lower_label.setText(f"{Power}mW")

        _, _,Z_new= self.Crossed_beam_math(self.Propaxis_range,self.Transverse_range1,0,self.Beam_waist,Wavelength,Power*1e-3,laser_Polarisation,Mf1)

        z_max = np.max(Z_new)
        z_min = np.min(Z_new)
        if z_max<z_min:
            colour_math = (z_max-Z_new)/(z_max-z_min)
        else:
            colour_math = np.zeros_like(Z_new)

        print(f"max = {z_max}")
        print(f"min = {z_min}")

        surface_colours =pg.colormap.get('viridis').map(colour_math) 


        if hasattr(self.tab1, 'surface_plot'):
            self.tab1.surface_plot.setData(z=Z_new,colors = surface_colours)
        

    
    def Update2(self):

        laser_Polarisation = self.Polarisation_slider2.value()
        self.Polarisation_Lower_label2.setText(f"{laser_Polarisation}")
        
        Wavelength = self.wavelength_slider2.value()*1e-9
        self.wavelength_Lower_label2.setText(f"{self.wavelength_slider2.value()}")

        if Wavelength>=780.241*1e-9:
            self.scattering_rate_curve1.setPen('r')
            self.scattering_rate_curve2.setPen('#FF7F7F')
        else:
            self.scattering_rate_curve1.setPen('b')
            self.scattering_rate_curve2.setPen('#66B2FF')

        Mf1 = self.Mf1_slider2.value()
        self.Mf1_Lower_label2.setText(f"mf={Mf1}")

        Mf2 = self.Mf2_slider2.value()
        self.Mf2_Lower_label2.setText(f"mf={Mf2}")

        ScatteringRate1 = Scattering_Rate(3.610e7,3.811e7,2.369e15,2.415e15,laser_Polarisation,-0.5,Mf1,Wavelength,self.intensity)
        ScatteringRate2 = Scattering_Rate(3.610e7,3.811e7,2.369e15,2.415e15,laser_Polarisation,0.5,Mf2,Wavelength,self.intensity)

        self.scattering_rate_curve1.setData(self.Power,ScatteringRate1)
        self.scattering_rate_curve2.setData(self.Power,ScatteringRate2)

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
        
        if self.tab1.plot_widget.sceneBoundingRect().contains(pos):
            
            mouse_point = self.tab1.plot_widget.plotItem.vb.mapSceneToView(pos)
            
            
            self.tab1.coord_label.setText(f"Trap Depth Graph\n | Power: {mouse_point.x():.2f}(mW)| \n | Depth: {mouse_point.y()*1e3:.2f}(mK)|")

    def mouse_moved_tab2(self, event):
        pos = event[0]
        if self.tab2.plot_widget.sceneBoundingRect().contains(pos):
            mouse_point = self.tab2.plot_widget.plotItem.vb.mapSceneToView(pos)
            self.tab2.coord_label.setText(f"Scattering Rate Graph\n | Power: {mouse_point.x():.2f}(mW)|\n | Rate: {mouse_point.y():.2f}|")
                



        


app = QApplication(sys.argv)
window = AtomTrapApp()
window.show()
app.exec()
