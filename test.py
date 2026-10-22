import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy import constants

####################Plots#########################
plt.style.use("dark_background")
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
plt.subplots_adjust(left=0.10, right=0.95, top=0.92, bottom=0.30, hspace=0.35, wspace=0.30)

#############Initial values and constants###############
c = constants.c
k_B = constants.k
omega_D1 = 2.368e15
omega_D2 = 2.413e15
gamma_D1 = 2 * np.pi * 5.75e6
gamma_D2 = 2 * np.pi * 6.066e6
Rubidium_mass = 1.443e-25

Power = np.linspace(60e-3, 300e-3, 300)

initial_wavelength = 850e-9
initial_focal_length = 8e-3
initial_Win = 1.5e-3
initial_beam_waist = 1e-6

#######################FUNCTIONS###########################
def compute_detuning(wave_len):
    laser_frequency = (2 * np.pi * c) / wave_len
    term_D1 = (1 / (omega_D1 - laser_frequency)) + (1 / (omega_D1 + laser_frequency))
    term_D2 = (1 / (omega_D2 - laser_frequency)) + (1 / (omega_D2 + laser_frequency))
    return (1/3 * gamma_D1 * term_D1) + (2/3 * gamma_D2 * term_D2)

def diffraction_waist(wave_len, focal_length, Win):
    return (wave_len * focal_length) / (np.pi * Win)

def trap_depth_K(Power, wave_len, Win, focal_length):
    w0 = diffraction_waist(wave_len, focal_length, Win)
    detuning = compute_detuning(wave_len)
    return np.abs((3 * c**2) * Power * detuning / ((omega_D2**3) * w0**2 * k_B))

def measured_trap_depth_K(Power, wave_len, w0):
    detuning = compute_detuning(wave_len)
    return np.abs((3 * c**2) * Power * detuning / ((omega_D2**3) * w0**2 * k_B))

def radial_freq(trap_K, wave_len, focal_length, Win):
    w0 = diffraction_waist(wave_len, focal_length, Win)
    return np.sqrt((4 * trap_K * k_B) / (Rubidium_mass * w0**2))

def axial_freq(trap_K, wave_len, focal_length, Win):
    w0 = diffraction_waist(wave_len, focal_length, Win)
    return np.sqrt((2 * trap_K * k_B) / (Rubidium_mass * (np.pi * w0**2 / wave_len)**2))

def measured_radial_freq(trap_K, w0):
    return np.sqrt((4 * trap_K * k_B) / (Rubidium_mass * w0**2))

def measured_axial_freq(trap_K, wave_len, w0):
    return np.sqrt((2 * trap_K * k_B) / (Rubidium_mass * (np.pi * w0**2 / wave_len)**2))

#################Initialization######################
y1 = trap_depth_K(Power, initial_wavelength, initial_Win, initial_focal_length)
y2 = radial_freq(y1, initial_wavelength, initial_focal_length, initial_Win)
y3 = axial_freq(y1, initial_wavelength, initial_focal_length, initial_Win)
y4 = measured_trap_depth_K(Power, initial_wavelength, initial_beam_waist)
y5 = measured_radial_freq(y4, initial_beam_waist)
y6 = measured_axial_freq(y4, initial_wavelength, initial_beam_waist)

line1, = axes[0, 0].plot(Power * 1000, y1 * 1e6, color="#0328fc", alpha=0.85)
line2, = axes[0, 1].plot(Power * 1000, y2 / (2*np.pi*1e3), color="#0328fc", alpha=0.85, label="Radial")
line3, = axes[0, 1].plot(Power * 1000, y3 / (2*np.pi*1e3), color="#fcc603", alpha=0.85, label="Axial")
line4, = axes[1, 0].plot(Power * 1000, y4 * 1e6, color="#0328fc", alpha=0.85)
line5, = axes[1, 1].plot(Power * 1000, y5 / (2*np.pi*1e3), color="#0328fc", alpha=0.85, label="Radial")
line6, = axes[1, 1].plot(Power * 1000, y6 / (2*np.pi*1e3), color="#fcc603", alpha=0.85, label="Axial")

for ax in axes.flat:
    ax.grid(color="white", linestyle="--", alpha=0.3)
    ax.set_xlabel("Power (mW)")

axes[0, 0].set_ylabel("Trap Depth (μK)")
axes[0, 1].set_ylabel("Frequency (kHz)")
axes[1, 0].set_ylabel("Trap Depth (μK)")
axes[1, 1].set_ylabel("Frequency (kHz)")
axes[0, 1].legend(); axes[1, 1].legend()

#################Update Logic#####################
def update(val):
    W = wavelength_slider.val * 1e-9
    F = focallength_slider.val * 1e-3
    Win = Win_slider.val * 1e-3
    W0 = beam_waist_slider.val * 1e-6

    # Update Data
    y1 = trap_depth_K(Power, W, Win, F)
    y2 = radial_freq(y1, W, F, Win)
    y3 = axial_freq(y1, W, F, Win)
    y4 = measured_trap_depth_K(Power, W, W0)
    y5 = measured_radial_freq(y4, W0)
    y6 = measured_axial_freq(y4, W, W0)

    line1.set_ydata(y1 * 1e6)
    line2.set_ydata(y2 / (2*np.pi*1e3))
    line3.set_ydata(y3 / (2*np.pi*1e3))
    line4.set_ydata(y4 * 1e6)
    line5.set_ydata(y5 / (2*np.pi*1e3))
    line6.set_ydata(y6 / (2*np.pi*1e3))

    # Update Limits
    axes[0, 0].set_ylim(0, np.max(y1 * 1e6) * 1.1)
    axes[0, 1].set_ylim(0, max(np.max(y2), np.max(y3)) / (2*np.pi*1e3) * 1.1)
    axes[1, 0].set_ylim(0, np.max(y4 * 1e6) * 1.1)
    axes[1, 1].set_ylim(0, max(np.max(y5), np.max(y6)) / (2*np.pi*1e3) * 1.1)
    
    axes[1, 0].set_title(f"Measured Waist ({beam_waist_slider.val:.0f} μm) Trap Depth")
    fig.canvas.draw_idle()

#################Sliders######################
ax_s1 = plt.axes([0.20, 0.20, 0.5, 0.03]); ax_s2 = plt.axes([0.20, 0.15, 0.5, 0.03])
ax_s3 = plt.axes([0.20, 0.10, 0.5, 0.03]); ax_s4 = plt.axes([0.20, 0.05, 0.5, 0.03])

wavelength_slider = Slider(ax_s1, "Wavelength (nm)", 700, 1064, valinit=850)
focallength_slider = Slider(ax_s2, "Focal Length (mm)", 5, 15, valinit=8)
Win_slider = Slider(ax_s3, "Input Beam Radius (mm)", 1, 3, valinit=1.5)
beam_waist_slider = Slider(ax_s4, "Measured Beam Waist (μm)", 1, 50, valinit=1)

for s in [wavelength_slider, focallength_slider, Win_slider, beam_waist_slider]:
    s.on_changed(update)

plt.show()