import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ------------------------------------------------
# Frequency axis
# ------------------------------------------------

f = np.linspace(85,105,5000)

# ------------------------------------------------
# Chebyshev response
# ------------------------------------------------

def cheby_response(fc,bw,ripple):

    eps = np.sqrt(10**(ripple/10)-1)

    x = (f-fc)/(bw/2)

    T3 = 4*x**3 - 3*x

    H = 1/np.sqrt(1 + eps**2 * T3**2)

    return 20*np.log10(H)

# ------------------------------------------------
# Component synthesis
# ------------------------------------------------

def component_values(fc,bw):

    L = 100e-9

    C = 1 / ((2*np.pi*fc*1e6)**2 * L)

    # crude estimate of coupling capacitance
    Cc = 0.8 * bw

    return (
        L,
        L,
        L,
        C,
        C,
        C,
        Cc*1e-12,
        Cc*1e-12
    )

# ------------------------------------------------
# Figure
# ------------------------------------------------

fig,ax = plt.subplots(figsize=(12,6))
plt.subplots_adjust(bottom=0.25,right=0.78)

fc0 = 95
bw0 = 4
ripple0 = 0.5

line, = ax.plot(
    f,
    cheby_response(fc0,bw0,ripple0),
    lw=2
)

ax.axvspan(
    93,
    97,
    color='green',
    alpha=0.2
)

ax.set_xlim(88,102)
ax.set_ylim(-40,1)

ax.grid(True)

ax.set_title("3-Pole Chebyshev Filter")

ax.set_xlabel("Frequency (MHz)")
ax.set_ylabel("Gain (dB)")

# ------------------------------------------------
# Component display
# ------------------------------------------------

text_box = fig.text(
    0.80,
    0.55,
    "",
    fontsize=10,
    family="monospace"
)

# ------------------------------------------------
# Sliders
# ------------------------------------------------

ax_fc = plt.axes([0.20,0.15,0.55,0.03])
ax_bw = plt.axes([0.20,0.10,0.55,0.03])
ax_rp = plt.axes([0.20,0.05,0.55,0.03])

s_fc = Slider(
    ax_fc,
    "Center MHz",
    90,
    100,
    valinit=fc0
)

s_bw = Slider(
    ax_bw,
    "BW MHz",
    1,
    10,
    valinit=bw0
)

s_rp = Slider(
    ax_rp,
    "Ripple dB",
    0.1,
    2.0,
    valinit=ripple0
)

# ------------------------------------------------
# Update
# ------------------------------------------------

def update(val):

    fc = s_fc.val
    bw = s_bw.val
    ripple = s_rp.val

    line.set_ydata(
        cheby_response(
            fc,
            bw,
            ripple
        )
    )

    L1,L2,L3,C1,C2,C3,Cc1,Cc2 = component_values(fc,bw)

    text_box.set_text(
f"""
L1 = {L1*1e9:6.1f} nH
L2 = {L2*1e9:6.1f} nH
L3 = {L3*1e9:6.1f} nH

C1 = {C1*1e12:6.2f} pF
C2 = {C2*1e12:6.2f} pF
C3 = {C3*1e12:6.2f} pF

Cc1= {Cc1*1e12:6.2f} pF
Cc2= {Cc2*1e12:6.2f} pF

Rs = 50 Ω
Rl = 50 Ω
"""
    )

    fig.canvas.draw_idle()

update(None)

s_fc.on_changed(update)
s_bw.on_changed(update)
s_rp.on_changed(update)

plt.show()




