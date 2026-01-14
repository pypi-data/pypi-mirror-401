
"""
Macer: Machine-learning accelerated Atomic Computational Environment for automated Research workflows
Copyright (c) 2025 The Macer Package Authors
Author: Soungmin Bae <soungminbae@gmail.com>
License: MIT
"""

import os
import numpy as np
from ase.io import read, write
from ase.optimize import FIRE, BFGS, LBFGS, MDMin, GPMin, QuasiNewton as QN
from ase.optimize.sciopt import SciPyFminCG
from ase.io.trajectory import Trajectory
from ase import Atoms # Added import
from ase.constraints import FixSymmetry


from macer.relaxation.isif import get_relax_target
from macer.io.writers import (
    write_outcar, write_vasprun_xml, write_calc_results_json
)
from macer.io.plotting import plot_relaxation_log

from macer.calculator.factory import get_calculator

def relax_structure(
    input_file, fmax=0.01, smax=0.001, # Removed default "POSCAR"
    device="cpu", isif=2, fix_axis=None,
    quiet=False, contcar_name="CONTCAR",
    outcar_name="OUTCAR", xml_name="vasprun-mace.xml",
    make_pdf=True, write_json=False, model_path=None, max_steps=None,
    optimizer_name="FIRE", output_dir_override: str | None = None, ff: str = "sevennet",
    modal: str = None, symprec: float = 1e-6, use_symmetry: bool = True,
    calculator=None
):
    if isinstance(input_file, Atoms):
        atoms = input_file
        # If input is an Atoms object, we need a prefix for output files.
        # Use a tag if available, otherwise a generic one.
        prefix = atoms.info.get('tag', 'relaxed_structure')
        output_dir = output_dir_override if output_dir_override is not None else "." # Use override or default to current
        if not quiet:
            print(f" Loaded structure from Atoms object ({len(atoms)} atoms)")
    else:
        atoms = read(input_file, format="vasp")
        prefix = os.path.basename(input_file)
        output_dir = output_dir_override if output_dir_override is not None else (os.path.dirname(input_file) or ".")
        if not quiet:
            print(f" Loaded structure from {input_file} ({len(atoms)} atoms)")
    
    if calculator:
        calc = calculator
    else:
        calc_kwargs = {
            "model_path": model_path,
            "device": device,
            "modal": modal,
        }

        # Special handling for MACE model_paths which expects a list
        if ff == "mace":
            calc_kwargs["model_paths"] = [calc_kwargs["model_path"]]
            del calc_kwargs["model_path"]
            
        calc = get_calculator(ff_name=ff, **calc_kwargs)
    
    atoms.calc = calc

    # Handle ISIF=0 as a single-point calculation
    if isif == 0:
        if not quiet:
            print(" ISIF=0 → Single-point calculation (no relaxation).")
        
        e = atoms.get_potential_energy()
        fmax_cur = np.abs(atoms.get_forces()).max()
        
        if not quiet:
            print(f" Single-point | E = {e:.6f} eV | Fmax={fmax_cur:.5f}")

        # Write output files
        atoms.velocities = None
        write(contcar_name, atoms, format="vasp")
        write_outcar(atoms, e, outcar_name)
        write_vasprun_xml(atoms, e, xml_name)
        if write_json:
            write_calc_results_json(atoms, e, filename=os.path.join(output_dir, "calc_results.json"))
        if make_pdf:
            plot_relaxation_log(prefix, output_dir, energies=[], steps=[], forces_hist=[], stress_hist=[], isif=isif, atoms=atoms)
        
        return atoms # Return the original atoms object

    target = get_relax_target(atoms, isif, fix_axis or [])

    # Add FixSymmetry constraint by default
    if use_symmetry:
        current_constraints = atoms.constraints
        if not any(isinstance(c, FixSymmetry) for c in current_constraints):
            current_constraints.append(FixSymmetry(atoms, symprec=symprec))
            atoms.set_constraint(current_constraints)
            if not quiet:
                print(f" Applied FixSymmetry constraint to preserve symmetry during relaxation (symprec={symprec}).")

    energies, steps, forces_hist, stress_hist = [], [], [], []

    if not quiet:
        print(f"Starting {optimizer_name} relaxation (fmax={fmax:.4f} eV/Å, smax={smax:.4f} eV/Å³, ISIF={isif})")

    # Ensure trajectory file is written to output_dir
    traj_path = os.path.join(output_dir, f"relax-{prefix}.traj")
    with Trajectory(traj_path, "w", target) as traj:
        optimizer_map = {
            "FIRE": FIRE,
            "BFGS": BFGS,
            "LBFGS": LBFGS,
            "GPMin": GPMin,
            "MDMin": MDMin,
            "CG": SciPyFminCG,
            "QN": QN,
        }
        OptimizerClass = optimizer_map.get(optimizer_name)
        if OptimizerClass is None:
            raise ValueError(f"Unknown optimizer: {optimizer_name}. Available optimizers are: {', '.join(optimizer_map.keys())}")

        # Common arguments for optimizers
        optimizer_args = {"trajectory": traj}
        if optimizer_name == "FIRE":
            optimizer_args["maxstep"] = 0.1
            optimizer_args["dt"] = 0.1
        elif optimizer_name == "LBFGS":
            optimizer_args["logfile"] = None # LBFGS requires logfile to be None if not used
        
        opt = OptimizerClass(target, **optimizer_args)

        def log_callback():
            e = atoms.get_potential_energy()
            fmax_cur = np.abs(atoms.get_forces()).max()
            stress_cur = np.abs(atoms.get_stress()).max() if isif >= 3 else 0.0
            steps.append(len(steps))
            energies.append(e)
            forces_hist.append(fmax_cur)
            stress_hist.append(stress_cur)
            print(f" Step {len(steps):4d} | E = {e:.6f} eV | Fmax={fmax_cur:.5f} | σmax={stress_cur:.5f}")
            if max_steps is not None and len(steps) >= max_steps:
                print(f"Reached max steps ({max_steps}). Stopping optimization.")
                if hasattr(opt, "stop"):
                    opt.stop()
                else:
                    raise SystemExit
            elif fmax_cur < fmax and (isif < 3 or stress_cur < smax):
                print("Converged: force & stress thresholds satisfied.")
                if hasattr(opt, "stop"):
                    opt.stop()
                else:
                    raise SystemExit

        opt.attach(log_callback, interval=1)
        try:
            opt.run(fmax=fmax)
        except SystemExit:
            pass

    e = atoms.get_potential_energy()

    # Remove velocities before writing to file to avoid velocity block in CONTCAR
    atoms.velocities = None

    write(contcar_name, atoms, format="vasp")
    write_outcar(atoms, e, outcar_name)
    write_vasprun_xml(atoms, e, xml_name)
    if write_json:
        write_calc_results_json(atoms, e, filename=os.path.join(output_dir, "calc_results.json"))

    if make_pdf:
        plot_relaxation_log(prefix, output_dir, energies, steps, forces_hist, stress_hist, isif, atoms)
    
    return atoms # Return the relaxed atoms object
