import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy import constants
import scipy.constants as const
####################Plots#########################
plt.style.use("dark_background")
fig, axes = plt.subplots(2,2,figsize= (12,8))
plt.subplots_adjust(left=0.10,right=0.95,top=0.92,bottom=0.30,hspace=0.35,wspace=0.30)



#############Initial values and constant###############
c= constants.c
k_B =constants.k
resonance_wavelength = 780e-9
omega_0= (2*np.pi*c)/resonance_wavelength
omega_D1 =2.368e15
omega_D2 =2.413e15
Power = np.linspace(0,300e-3,300)
gamma = 2 * np.pi * 6.066e6
gamma_D1 = 2 * np.pi * 5.75e6
gamma_D2 = 2 * np.pi * 6.066e6
initial_radius=0
inintial_Win= 1.5e-3
initial_focal_length=  8e-3
initial_wavelength=850e-9
initial_detuning= (2*np.pi*c)/initial_wavelength-omega_0
Rubidium_mass = 1.443e-25
beam_waist_measured =3e-6
dia_w0 =4*((initial_wavelength* initial_focal_length) / (np.pi * inintial_Win))
init_w0 =dia_w0/2
#######################FUNCTIONS###########################


def trap_depth(gamma_1,gamma_2,Power,wave_len,Win,focal_length):
    
    w0 = 4*((wave_len * focal_length) / (np.pi * Win))
    laser_frequency = (2*np.pi*c)/wave_len
    detuning = (1/3*gamma_1*((1/(omega_D1-laser_frequency))+(1/(omega_D1+laser_frequency))))+(2/3*gamma_2*((1/(omega_D2-laser_frequency))+(1/(omega_D2+laser_frequency))))
    numerator = (3*c**2)*Power
    denominator = (omega_D2**3)*(w0/2)**2
    trap_depth_in_joules = (numerator/denominator)*detuning
    trap_depth_kelvin = np.abs(trap_depth_in_joules / k_B)
    return trap_depth_kelvin
    
initial_trapdepth_unpacked= trap_depth(gamma_D1,gamma_D2,Power,initial_wavelength,inintial_Win,initial_focal_length)
max_depth = np.max(initial_trapdepth_unpacked*1e3)
axes[0,0].set_ylim(0,max_depth*5)


def radial_trap_frequency(trap_depth,mass,wavelength,focal_length,Win):
    w0 = 4*((wavelength * focal_length) / (np.pi * Win))
    var1 = (4*trap_depth)/(mass*(w0/2)**2)
    return np.sqrt(var1)

initial_radial_frequency_unpacked = radial_trap_frequency(initial_trapdepth_unpacked*k_B,Rubidium_mass,initial_wavelength,initial_focal_length,inintial_Win)

def axial_trap_frequency(trap_depth,mass,wavelength,focal_length,Win):
    w0 = 4*((wavelength * focal_length) / (np.pi * Win))
    rayleigh_length= (np.pi*(w0/2)**2)/wavelength
    var2 =(2*trap_depth)/(mass*rayleigh_length**2)
    return np.sqrt(var2)

initial_trapaxial_frequency_unpacked = axial_trap_frequency(initial_trapdepth_unpacked*k_B,Rubidium_mass,initial_wavelength,initial_focal_length,inintial_Win)
max_freq = max(np.max(initial_radial_frequency_unpacked),np.max(initial_trapaxial_frequency_unpacked))
axes[0,1].set_ylim(0, (max_freq/ (2 * np.pi * 1000)) * 5)

def measured_trap_depth(gamma_1,gamma_2,Power,wave_len,w0):
    laser_frequency = (2*np.pi*c)/wave_len
    detuning = (1/3*gamma_1*((1/(omega_D1-laser_frequency))+(1/(omega_D1+laser_frequency))))+(2/3*gamma_2*((1/(omega_D2-laser_frequency))+(1/(omega_D2+laser_frequency))))
    numerator = (3*c**2)*Power
    denominator = (omega_D2**3)*w0**2
    trap_depth_in_joules = (numerator/denominator)*detuning
    trap_depth_kelvin = np.abs(trap_depth_in_joules / k_B)
    return trap_depth_kelvin

initial_measured_trap_depth =measured_trap_depth(gamma_D1,gamma_D2,Power,initial_wavelength,beam_waist_measured)
max_depth2 = np.max(initial_measured_trap_depth*1e3)
axes[1,0].set_ylim(0, (max_depth2)*5)
   
def measured_radial_trap_frequency(trap_depth,mass,w0):
    var1 = (4*trap_depth)/(mass*w0**2)
    return np.sqrt(var1)

initial_measured_radial_trap_frequency= measured_radial_trap_frequency(initial_measured_trap_depth*k_B,Rubidium_mass,beam_waist_measured)

def measured_axial_trap_frequency(trap_depth,mass,wavelength,w0):
    rayleigh_length= (np.pi*w0**2)/wavelength
    var2 =(2*trap_depth)/(mass*rayleigh_length**2)
    return np.sqrt(var2)

initial_measured_axial_trap_frequency= measured_axial_trap_frequency(initial_measured_trap_depth*k_B,Rubidium_mass,initial_wavelength,beam_waist_measured)

max_freq2 = max(np.max(initial_measured_radial_trap_frequency),np.max(initial_measured_axial_trap_frequency))
axes[1,1].set_ylim(0, (max_freq2 / (2 * np.pi * 1000)) * 5)


#################Plotting########################
dic1 = dict(color= "#0328fc",alpha =0.85)
line1, =axes[0,0].plot(Power*1000,initial_trapdepth_unpacked*1e3,**dic1)
line2, = axes[0,1].plot(Power*1000,initial_radial_frequency_unpacked/(2*np.pi*1e3),**dic1,label="Radial")
line3, = axes[0,1].plot(Power*1000,initial_trapaxial_frequency_unpacked/(2*np.pi*1e3),color= "#fcc603",alpha =0.85,label="Axial")

line4, =axes[1,0].plot(Power*1000,initial_measured_trap_depth*1e3,**dic1)
line5, = axes[1,1].plot(Power*1000,initial_measured_radial_trap_frequency/(2*np.pi*1e3),**dic1,label="Radial")
line6, = axes[1,1].plot(Power*1000,initial_measured_axial_trap_frequency/(2*np.pi*1e3),color= "#fcc603",alpha =0.85,label="Axial")

axes[0,1].legend()
axes[1,1].legend()

#####################Axis Lmiits###############
axes[0,0].set_xlim(0,300)
axes[0,1].set_xlim(0,300)
axes[1,0].set_xlim(0,300)
axes[1,1].set_xlim(0,300)



#################axis labels######################
axes[0,0].set_xlabel("Power(mW)",color = "white")
axes[0,0].set_ylabel("Trap_depth(mK)",color = "white")
axes[0,1].set_xlabel("Power(mW)",color = "white")
axes[0,1].set_ylabel("Frequency(KHz)",color = "white")
axes[0,0].grid(color="white", linestyle="--", alpha=0.3)
axes[0,1].grid(color="white", linestyle="--", alpha=0.3)

axes[1,0].set_xlabel("Power(mW)",color = "white")
axes[1,0].set_ylabel("Trap_depth(mK)",color = "white")
axes[1,1].set_xlabel("Power(mW)",color = "white")
axes[1,1].set_ylabel("Frequency(KHz)",color = "white")
axes[1,0].grid(color="white", linestyle="--", alpha=0.3)
axes[1,1].grid(color="white", linestyle="--", alpha=0.3)

axes[0,0].set_title(f"Trap depth for Focal Spot({init_w0*1e6:.2f}μm)")
axes[0,1].set_title(f"Trap Frequency for Focal Spot({init_w0*1e6:.2f}μm)")

axes[1,0].set_title(f"Measured Waist ({beam_waist_measured*1e6:.0f} μm)")
axes[1,1].set_title("Measured Frequencies")


#################Sliders######################
slider1 = plt.axes([0.20, 0.2, 0.5, 0.03])
slider2 = plt.axes([0.20, 0.15, 0.5, 0.03])
slider3 = plt.axes([0.20, 0.10, 0.5, 0.03])
  
wavelength_slider=Slider(slider1,"Wavelength(m)",700e-9,1064e-9,valinit=initial_wavelength)    
focallength_slider=Slider(slider2,"Focal_length(m)",5e-3,15e-3,valinit=initial_focal_length)
Win_slider=Slider(slider3,"Initial_Beam_radius(m)",1e-3,5e-3,valinit=inintial_Win)




#################UPDATE FUNCTION#####################
def update(var):
    WAVELENGTH =wavelength_slider.val
    FOCALLENGTH=focallength_slider.val
    INIT_WIN= Win_slider.val
    DIA_W0 = 4*((WAVELENGTH* FOCALLENGTH) / (np.pi * INIT_WIN))
    INIT_W0 = DIA_W0/2
   
   
    y1_data = trap_depth(gamma_D1,gamma_D2,Power,WAVELENGTH,INIT_WIN,FOCALLENGTH,)
    y2_data = radial_trap_frequency(y1_data*k_B,Rubidium_mass,WAVELENGTH,FOCALLENGTH,INIT_WIN)
    y3_data = axial_trap_frequency(y1_data*k_B,Rubidium_mass,WAVELENGTH,FOCALLENGTH,INIT_WIN)
    y4_data = measured_trap_depth(gamma_D1,gamma_D2,Power,WAVELENGTH,beam_waist_measured)
    y5_data = measured_radial_trap_frequency(y4_data*k_B,Rubidium_mass,beam_waist_measured)
    y6_data = measured_axial_trap_frequency(y4_data*k_B,Rubidium_mass,WAVELENGTH,beam_waist_measured)

    axes[0,0].set_title(f"Trap depth for Focal Spot({INIT_W0*1e6:.2f}μm)")
    axes[0,1].set_title(f"Trap Frequency for Focal Spot({INIT_W0*1e6:.2f}μm)")
    

    line1.set_ydata(y1_data*1e3)
    line2.set_ydata(y2_data/(2*np.pi*1e3))
    line3.set_ydata(y3_data/(2*np.pi*1e3))
    line4.set_ydata(y4_data*1e3)
    line5.set_ydata(y5_data/(2*np.pi*1e3))
    line6.set_ydata(y6_data/(2*np.pi*1e3))

    fig.canvas.draw_idle()




wavelength_slider.on_changed(update)
focallength_slider.on_changed(update)
Win_slider.on_changed(update)



plt.show()