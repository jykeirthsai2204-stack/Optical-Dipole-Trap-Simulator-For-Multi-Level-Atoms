import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy import constants
import scipy.constants as const

# =========================
# Plot Style
# =========================
plt.style.use("dark_background")

fig, ax = plt.subplots(figsize=(9, 6))
plt.subplots_adjust(bottom=0.45)

# =========================
# Constants
# =========================
k_B = constants.k
c = constants.c

gamma = 2 * np.pi * 6.066e6

wavelength = 850e-9
omega_0 = 2 * np.pi * (c / 780e-9)

laser_frequency = (2 * np.pi * c) / wavelength

initial_focal_length = 8e-3
initial_radius = 0

Power = np.linspace(60e-3, 300e-3, 240)

Win = 1.5e-3

Detuning = laser_frequency - omega_0

# =========================
# Trap Depth Function
# =========================
def calculate_trapdepth(
    decay_rate,
    detuning,
    Power,
    radius,
    wave_len,
    Win,
    focal_length
):

    # Beam waist after focusing
    w0 = (wave_len * focal_length) / (np.pi * Win)

    # Peak Gaussian intensity
    peak_intensity = (2 * Power) / (np.pi * w0**2)

    # Radial Gaussian profile
    intensity = peak_intensity * np.exp((-2 * radius**2) / (w0**2))

    # Dipole potential constant
    constant = (3 * np.pi * const.c**2) / (2 * omega_0**3)

    # Trap depth in Joules
    trap_depth_joules = (
        constant * decay_rate * intensity
    ) / detuning

    # Convert to Kelvin
    trap_depth_kelvin = np.abs(
        trap_depth_joules / k_B
    )

    return trap_depth_kelvin

# =========================
# Avoid exact resonance
# =========================
if abs(Detuning) < 1e-12:
    Detuning = 1e-9

# =========================
# Initial Data
# =========================
initial_ydata = calculate_trapdepth(
    gamma,
    Detuning,
    Power,
    initial_radius,
    wavelength,
    Win,
    initial_focal_length
)

# =========================
# Plot Initial Graph
# =========================
line, = ax.plot(
    Power * 1000,
    initial_ydata * 1e6,
    color="cyan",
    linewidth=2
)

# Labels
ax.set_xlabel("Laser Power (mW)", fontsize=12)
ax.set_ylabel("Trap Depth (µK)", fontsize=12)
ax.set_title("Optical Dipole Trap Depth vs Laser Power", fontsize=14)

# Grid
ax.grid(color="white", linestyle="--", alpha=0.3)

# =========================
# FIXED AXIS LIMITS
# (important so graph visually changes)
# =========================
ax.set_xlim(60, 300)

fixed_max = np.max(initial_ydata * 1e6) * 5
ax.set_ylim(0, fixed_max)

# =========================
# Sliders
# =========================

# Focal length slider
slider1 = plt.axes([0.2, 0.10, 0.5, 0.03])

# Wavelength slider
slider2 = plt.axes([0.2, 0.20, 0.5, 0.03])

# Radius slider
slider3 = plt.axes([0.2, 0.30, 0.5, 0.03])

focallength_slider = Slider(
    slider1,
    "Focal Length (m)",
    5e-3,
    15e-3,
    valinit=initial_focal_length
)

laser_wavelength = Slider(
    slider2,
    "Wavelength (m)",
    780e-9,
    900e-9,
    valinit=wavelength
)

radius_slider = Slider(
    slider3,
    "Radius (m)",
    0.0,
    2e-6,
    valinit=initial_radius
)

# =========================
# Update Function
# =========================
def update(val):

    FOCAL_LENGTH = focallength_slider.val
    WAVELENGTH = laser_wavelength.val
    RADIUS = radius_slider.val

    # Laser frequency
    laser_frequency = (2 * np.pi * c) / WAVELENGTH

    # Detuning
    DETUNING = laser_frequency - omega_0

    # Prevent singularity near resonance
    if abs(DETUNING) < 1e6:
        DETUNING = 1e6

    # New trap depth
    y_data = calculate_trapdepth(
        gamma,
        DETUNING,
        Power,
        RADIUS,
        WAVELENGTH,
        Win,
        FOCAL_LENGTH
    )

    # Update graph
    line.set_ydata(y_data * 1e6)

    # Redraw
    fig.canvas.draw_idle()

# =========================
# Connect Sliders
# =========================
focallength_slider.on_changed(update)
laser_wavelength.on_changed(update)
radius_slider.on_changed(update)

# =========================
# Show Plot
# =========================
plt.show()