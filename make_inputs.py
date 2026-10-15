# Writes Quantum ESPRESSO inputs for the tungsten vacancy study.
# Usage:
#   python3 make_inputs.py scan            -> lattice-constant scan inputs
#   python3 make_inputs.py cells 3.172     -> supercell inputs at your lattice constant
import sys
from ase.build import bulk
from ase.io import write

PSEUDO = {"W": "w_pbe_v1.2.uspp.F.UPF"}
COMMON = dict(
    control={"pseudo_dir": "./pseudo", "outdir": "./tmp", "tprnfor": True},
    system={"ecutwfc": 40, "ecutrho": 320,
            "occupations": "smearing", "smearing": "mv", "degauss": 0.02},
    electrons={"conv_thr": 1e-8, "mixing_beta": 0.3},
)

def write_pw(fname, atoms, kpts, calc="scf"):
    inp = {k: dict(v) for k, v in COMMON.items()}
    inp["control"]["calculation"] = calc
    inp["control"]["prefix"] = fname.replace(".in", "")
    if calc == "relax":
        inp["ions"] = {"ion_dynamics": "bfgs"}
    write(fname, atoms, format="espresso-in", input_data=inp,
          pseudopotentials=PSEUDO, kpts=kpts)
    # drop empty namelists that older QE versions reject
    txt = open(fname).read()
    for nl in ("&FCP\n/\n", "&RISM\n/\n"):
        txt = txt.replace(nl, "")
    open(fname, "w").write(txt)
    print("wrote", fname, "with", len(atoms), "atoms")

mode = sys.argv[1]
if mode == "scan":
    for a in [3.12, 3.14, 3.16, 3.18, 3.20, 3.22, 3.24]:
        w = bulk("W", "bcc", a=a, cubic=True)          # 2-atom cubic cell
        write_pw(f"scan_{a:.2f}.in", w, (12, 12, 12))
elif mode == "cells":
    a = float(sys.argv[2])
    for n, k in [(2, 6), (3, 4)]:                       # 16 and 54 atoms
        perfect = bulk("W", "bcc", a=a, cubic=True).repeat((n, n, n))
        write_pw(f"perfect_{n}x{n}x{n}.in", perfect, (k, k, k))
        vac = perfect.copy()
        del vac[0]                                      # remove one atom
        write_pw(f"vacancy_{n}x{n}x{n}.in", vac, (k, k, k), calc="relax")
