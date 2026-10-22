import numpy as np
import pyqtgraph as pg
from scipy import constants

C = constants.c
ħ= constants.hbar
K_B= constants.k

def Trap_Dept(τ1,τ2,freq_1,freq_2,Polarisation,gf,Mf,wavelength,Intensity): 

        constant = (np.pi*(C**2))/2
        laser_frequency = (2*np.pi*C)/wavelength

        Detuning1=laser_frequency-freq_1
        term1 = (τ1*(1-(Polarisation*gf*Mf)))/((freq_1**3)*(Detuning1))

        Detuning2 = laser_frequency - freq_2 
        term2 = (τ2*(2+(Polarisation*gf*Mf)))/((freq_2**3)*(Detuning2))

        return (constant*(term1+term2)*Intensity)/K_B

def Scattering_Rate(τ1,τ2,freq_1,freq_2,Polarisation,gf,Mf,wavelength,Intensity):
        
        constant =(np.pi*(C)**2)/(2*ħ)
        laser_frequency = (2*np.pi*C)/wavelength

        Detuning1=laser_frequency-freq_1
        term1 = ((τ1**2)*(1-(Polarisation*gf*Mf)))/((freq_1**3)*(Detuning1**2))

        Detuning2 = laser_frequency - freq_2
        term2 = ((τ2**2)*(2+(Polarisation*gf*Mf)))/((freq_2**3)*(Detuning2**2))

        return constant*(term1+term2)*Intensity

def Power_calculator_function(τ1,τ2,freq_1,freq_2,Polarisation,gf,Mf,wavelength,Beam_waist,input_trap_depth):
        
        constant = (np.pi*(C**2))/2
        laser_frequency = (2*np.pi*C)/wavelength
        Trapt_depth = input_trap_depth*K_B
        
        Detuning1=laser_frequency-freq_1
        term1 = (τ1*(1-(Polarisation*gf*Mf)))/((freq_1**3)*(Detuning1))

        Detuning2 = laser_frequency - freq_2 
        term2 = (τ2*(2+(Polarisation*gf*Mf)))/((freq_2**3)*(Detuning2))

        return ((Trapt_depth*np.pi*(Beam_waist**2))/(2*constant*(term1+term2)))





