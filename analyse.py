# Reads QE outputs and prints the lattice constant and vacancy formation energies.
import glob, re
import numpy as np

RY = 13.605693122994   # 1 Ry in eV

def final_energy(fname):
    """Last '!    total energy' line in a pw.x output, in eV."""
    e = None
    with open(fname) as f:
        for line in f:
            if line.startswith("!"):
                e = float(line.split("=")[1].split()[0]) * RY
    if e is None:
        raise RuntimeError(f"no final energy in {fname}: did the run finish?")
    return e

# 1. Lattice constant from the scan (fit a parabola, take its minimum)
scan = sorted(glob.glob("scan_*.out"))
if scan:
    a = np.array([float(re.findall(r"scan_(\d+\.\d+)", s)[0]) for s in scan])
    E = np.array([final_energy(s) for s in scan])
    c = np.polyfit(a, E, 2)
    a0 = -c[1] / (2 * c[0])
    print(f"Equilibrium lattice constant: {a0:.4f} Angstrom")

# 2. Vacancy formation energy for each supercell size
for n in (2, 3):
    tag = f"{n}x{n}x{n}"
    try:
        Ep = final_energy(f"perfect_{tag}.out")
        Ev = final_energy(f"vacancy_{tag}.out")
    except (FileNotFoundError, RuntimeError) as err:
        print(f"{tag}: skipped ({err})")
        continue
    N = 2 * n**3
    Evac = Ev - (N - 1) / N * Ep
    print(f"{tag} ({N} atoms): E_vac = {Evac:.3f} eV")
