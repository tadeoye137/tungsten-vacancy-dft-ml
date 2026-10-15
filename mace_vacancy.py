# Vacancy formation energy of bcc W with the MACE-MP-0 machine-learning potential.
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
    Ev = vac.get_potential_energy()

    N = len(perfect)
    print(f"{n}x{n}x{n}   {N:5d}   {Ev - (N - 1) / N * Ep:.3f}")
