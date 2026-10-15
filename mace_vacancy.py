# Vacancy formation energy of bcc W with the MACE-MP-0 machine-learning potential.
!pip install -q mace-torch ase

import numpy as np
from ase.build import bulk
from ase.optimize import BFGS
from mace.calculators import mace_mp

calc = mace_mp(model="medium", device="cpu", default_dtype="float64")

# 1. Lattice constant: scan a, fit a parabola, take the minimum
a_vals = np.linspace(3.12, 3.24, 13)
E_vals = []
for a in a_vals:
    w = bulk("W", "bcc", a=a, cubic=True)
    w.calc = calc
    E_vals.append(w.get_potential_energy())
c = np.polyfit(a_vals, E_vals, 2)
a0 = -c[1] / (2 * c[0])
print(f"MACE lattice constant: {a0:.4f} Angstrom")

# 2. Vacancy formation energy for growing supercells
print("cell     atoms   E_vac (eV)")
for n in (2, 3, 4, 5, 6):
    perfect = bulk("W", "bcc", a=a0, cubic=True).repeat((n, n, n))
    perfect.calc = calc
    Ep = perfect.get_potential_energy()

    vac = perfect.copy()
    del vac[0]
    vac.calc = calc
    BFGS(vac, logfile=None).run(fmax=0.01)   # relax atoms, box fixed

import matplotlib.pyplot as plt

dft = [(16, 3.700), (54, 3.364)]              # your QE results
N_m, E_m = zip(*mace)
N_d, E_d = zip(*dft)

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(N_m, E_m, "-o", color="#eb6834", lw=2, ms=8, label="MACE-MP-0")
ax.plot(N_d, E_d, "s", color="#2a78d6", ms=10, label="DFT (Quantum ESPRESSO, PBE)")

ax.annotate(f"{E_m[-1]:.2f} eV", (N_m[-1], E_m[-1]),
            textcoords="offset points", xytext=(0, 10), ha="center")
for N, E in dft:
    ax.annotate(f"{E:.2f}", (N, E), textcoords="offset points",
                xytext=(12, -4), color="#333333")

ax.set_xlabel("Atoms in supercell")
ax.set_ylabel("Vacancy formation energy (eV)")
ax.set_title("Vacancy formation energy in bcc W")
ax.grid(alpha=0.3)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False)
plt.tight_layout()
plt.savefig("W_vacancy.png", dpi=200)
plt.show()
fig, ax = plt.subplots(figsize=(6.5, 4.2))

# Published PBE range (128 atoms) as a shaded band
ax.axhspan(3.24, 3.33, color="#2a78d6", alpha=0.12, lw=0)
ax.text(440, 3.285, "Published PBE (128 atoms)", va="center", ha="right",
        fontsize=8, color="#1c5cab")

# Experiment as a dashed line
ax.axhline(3.62, color="#555555", ls="--", lw=1)
ax.text(440, 3.64, "Experiment 3.62 ± 0.2 eV", va="bottom", ha="right",
        fontsize=8, color="#555555")

ax.plot(N_m, E_m, "-o", color="#eb6834", lw=2, ms=8, label="MACE-MP-0")
ax.plot(N_d, E_d, "s", color="#2a78d6", ms=10, label="DFT, this work (PBE)")
for N, E in dft:
    ax.annotate(f"{E:.2f}", (N, E), textcoords="offset points",
                xytext=(12, -4), fontsize=9)
ax.annotate(f"{E_m[-1]:.2f}", (N_m[-1], E_m[-1]),
            textcoords="offset points", xytext=(0, -16), ha="center", fontsize=9)

ax.set_xlabel("Atoms in supercell")
ax.set_ylabel("Vacancy formation energy (eV)")
ax.set_title("Vacancy formation energy in bcc W")
ax.set_ylim(2.5, 3.85)
ax.grid(alpha=0.3)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, loc="center right")
plt.tight_layout()
plt.savefig("W_vacancy.png", dpi=200)
plt.show()
    Ev = vac.get_potential_energy()

    N = len(perfect)
    print(f"{n}x{n}x{n}   {N:5d}   {Ev - (N - 1) / N * Ep:.3f}")
