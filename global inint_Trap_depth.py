global inint_Trap_depth
inint_Trap_depth =calculate_trapdepth(gamma,inint_detuning)



global inint_beam_waist
inint_beam_waist= Calculate_beam_waist(780.24e-9,Win,inint_focallength)

global inint_Trap_depth
inint_Trap_depth =calculate_trapdepth(gamma,inint_detuning)




def calculate_trapdepth(decay_rate,detuning):
    constant= (3*np.pi*c**2)/(2*omega_0**3)
    return(constant*decay_rate*calculate_intensity)/detuning






import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy import constants
import scipy.constants as const
c= constants.c
k_B =constants.k
resonance_wavelength = 780e-9
omega_0= (2*np.pi*c)/resonance_wavelength

def costant_trapdepth(gamma,wavelength,beam_waist,power):

    nominator =3*c**2*gamma
    detuning = ((2*np.pi*c)/wavelength)-omega_0
    denominator =(omega_0**3)*detuning*(beam_waist**2)
    trapdepth_in_joules = (nominator/denominator)*power
    trapdepth_in_kelvin = np.abs(trapdepth_in_joules/k_B) 
    return trapdepth_in_kelvin
 
















def Calculate_beam_waist(wave_len,Win,focal_length):
    x =np.pi*Win
    return (wave_len*focal_length)/x


def calculate_intensity(Power,radius,wave_len,Win,focal_length):
    def Calculate_beam_waist():
        x =np.pi*Win
        return (wave_len*focal_length)/x
    peak_intensity =(2*Power)/(np.pi*Calculate_beam_waist()**2)
    return peak_intensity*np.exp()**((-2*radius**2)/Calculate_beam_waist**2)


def calculate_trapdepth(decay_rate,detuning,Power,radius,wave_len,Win,focal_length):
    def calculate_intensity():
        def Calculate_beam_waist():
            x =np.pi*Win
            return (wave_len*focal_length)/x
    peak_intensity =(2*Power)/(np.pi*Calculate_beam_waist()**2)
    return peak_intensity*np.exp()**((-2*radius**2)/Calculate_beam_waist**2)


    constant= (3*np.pi*c**2)/(2*omega_0**3)
    return(constant*decay_rate*calculate_intensity)/detuning