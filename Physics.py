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

def Crossed_Beam_TrapDepth(τ1,τ2,freq_1,freq_2,𝒫1,𝒫2,gf,Mf,wavelength,Intensity): #𝒫
        
        constant = (np.pi*(C**2))/2
        laser_frequency = (2*np.pi*C)/wavelength

        Detuning1=laser_frequency-freq_1
        term_11 = (τ1*(1-(𝒫1*gf*Mf)))/((freq_1**3)*(Detuning1))
        term_21 = (τ1*(1-(𝒫2*gf*Mf)))/((freq_1**3)*(Detuning1))

        Detuning2 = laser_frequency - freq_2 
        term_12 = (τ2*(2+(𝒫1*gf*Mf)))/((freq_2**3)*(Detuning2))
        term_22 = (τ2*(2+(𝒫2*gf*Mf)))/((freq_2**3)*(Detuning2))

        return (constant*(term_11+term_12+term_21+term_22)*Intensity)/K_B

def Intensity(beam_waist,wavelength,Power,P1,P2,T):                   #P1= Propogation axis-1
        
        Rayleigh_range = (np.pi*(beam_waist**2))/wavelength                        #P2= Propogation axis-2
        W_Propogation_axis1= beam_waist*(np.sqrt(1+(P1/Rayleigh_range)**2))         #T = Transverse axis
        initial_intensity1 = (2*Power)/(np.pi*(W_Propogation_axis1**2))
        term1 = np.exp(-1*2*(((P2**2) +(T**2))/(W_Propogation_axis1**2))) 
        
        return initial_intensity1*term1
        
















