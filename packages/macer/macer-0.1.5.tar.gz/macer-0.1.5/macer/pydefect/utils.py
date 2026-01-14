"""
Macer: Machine-learning accelerated Atomic Computational Environment for automated Research workflows
Copyright (c) 2025 The Macer Package Authors
Author: Soungmin Bae <soungminbae@gmail.com>
License: MIT
"""

import sys
import os
from pathlib import Path
import yaml
from monty.serialization import loadfn
from pymatgen.core import Structure, Composition
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDEntry

from pydefect.defaults import defaults
from pydefect.analyzer.make_defect_structure_info import MakeDefectStructureInfo
from pydefect.cli.make_defect_vesta_file import MakeDefectVestaFile

from macer.calculator.factory import get_available_ffs, get_calculator
from macer.relaxation.optimizer import relax_structure
from macer.utils.logger import Logger
from macer.io.writers import write_pydefect_dummy_files
from macer.defaults import DEFAULT_MODELS, _macer_root, _model_root, DEFAULT_DEVICE

def get_unique_dir_name(base_name):
    if not Path(base_name).exists():
        return Path(base_name)
    i = 1
    while True:
        new_name = f"{base_name}-NEW{i:02d}"
        if not Path(new_name).exists():
            return Path(new_name)
        i += 1

def stabilize_target(relative_energies_path, target_formula, manual_shift=0.0, buffer=1e-5):
    """
    Checks if the target is above convex hull. If so, shifts its energy in relative_energies.yaml
    to make it stable. Returns the total applied shift value (0.0 if stable and no manual shift).
    """
    if not Path(relative_energies_path).exists():
        print(f"Error: {relative_energies_path} does not exist.")
        return 0.0

    with open(relative_energies_path, 'r') as f:
        rel_energies = yaml.safe_load(f)

    # 1. Apply manual shift first (temporarily to check stability or permanently if stable)
    if target_formula not in rel_energies:
        print(f"Error: Target {target_formula} not found in {relative_energies_path}")
        return 0.0
    
    original_energy = rel_energies[target_formula]
    # We apply the manual shift (subtracted, as per convention: positive shift means lowering energy? 
    # The user said "--energy-shift-target 0.05 이면 target energy 를 0.05 eV 낮춤" -> new = old - 0.05)
    # So if manual_shift is 0.05, we subtract 0.05.
    current_energy_after_manual = original_energy - manual_shift
    rel_energies[target_formula] = current_energy_after_manual
    
    entries = []
    target_entry = None

    # Re-build entries with the manual shift applied
    for formula, energy_per_atom in rel_energies.items():
        try:
            comp = Composition(formula)
            total_energy = energy_per_atom * comp.num_atoms
            entry = PDEntry(comp, total_energy)
            entries.append(entry)
            if formula == target_formula:
                target_entry = entry
        except Exception as e:
            print(f"Warning: Could not process formula {formula}: {e}")

    if target_entry is None:
        return 0.0

    pd = PhaseDiagram(entries)
    e_above_hull = pd.get_e_above_hull(target_entry)
    
    extra_stabilization_shift = 0.0

    if e_above_hull > 1e-8:  # Use a small epsilon
        # It's still unstable after manual shift (or manual shift was 0)
        required_shift = -1.0 * e_above_hull
        # Add buffer
        extra_stabilization_shift = required_shift - buffer
        
        print(f"Target {target_formula} is unstable (e_above_hull={e_above_hull:.4f} eV/atom).")
        print(f"Additional stabilization shift required: {extra_stabilization_shift:.6f} eV/atom.")

    # Total shift = manual_shift (already subtracted) + extra_stabilization_shift (negative value to lower energy further)
    # But wait, user said "shift 0.05 means lower by 0.05".
    # My stabilize logic was "return recommended_shift" where recommended_shift was negative.
    # So let's keep consistent: return value is the net change in energy.
    # manual_shift argument is positive -> net change is -manual_shift.
    # extra_stabilization_shift is negative.
    
    total_change = -manual_shift + extra_stabilization_shift
    
    if total_change != 0.0:
        final_energy = float(original_energy + total_change)
        rel_energies[target_formula] = final_energy
        
        with open(relative_energies_path, 'w') as f:
            yaml.dump(rel_energies, f)
            
        print(f"Total applied energy shift: {total_change:.6f} eV/atom (Manual: -{manual_shift}, Stabilization: {extra_stabilization_shift:.6f}).")
        return total_change

    return 0.0

def write_summary_at_vertices(summary_path: Path, applied_shift=0.0):
    """
    Calculates and prints defect formation energies for each chemical potential
    vertex from a defect_energy_summary.json file.
    """
    if not summary_path.exists():
        print(f"Error: {summary_path} not found.")
        return

    try:
        # loadfn will deserialize into DefectEnergySummary object
        summary = loadfn(summary_path)
    except Exception as e:
        print(f"Error loading {summary_path}: {e}")
        return

    rel_chem_pots = summary.rel_chem_pots
    defect_energies_summary = summary.defect_energies
    output_filename = "defect_energy_summary-at-vertices.txt"

    with open(output_filename, "w") as f:
        f.write(f"title: {summary.title}\n")
        if applied_shift != 0.0:
            f.write(f"# Energy shift applied to make target stable: {applied_shift} eV/atom\n")
        f.write("\n")

        f.write("--- Standard Formation Energies (Chemical Potential = 0) ---\n")
        f.write(f"{'Defect Name':<20} {'Charge':<10} {'Formation Energy (eV)'}\n")
        f.write(f"{'-'*20} {'-'*10} {'-'*25}\n")
        
        for defect_name, defect_group in defect_energies_summary.items():
             if 0 in defect_group.charges:
                 idx = defect_group.charges.index(0)
                 energy = defect_group.defect_energies[idx].formation_energy
                 f.write(f"{defect_name:<20} {'0':<10} {energy:>25.4f}\n")
        f.write("\n")

        for vertex_label, chem_pots in rel_chem_pots.items():
            f.write(f"--- Vertex: {vertex_label} ---\n")
            chem_pot_str = ", ".join([f"{elem}: {pot:.4f}" for elem, pot in chem_pots.items()])
            f.write(f"Relative chemical potentials: {chem_pot_str}\n")
            f.write("-" * 40 + "\n")
            f.write(f"{ 'Defect Name':<20} {'Formation Energy (eV)'}\n")
            f.write(f"{'-'*20} {'-'*25}\n")

            formation_energies = {}
            for defect_name, defect_group in defect_energies_summary.items():
                charge_0_defect_energy = None
                try:
                    if 0 in defect_group.charges:
                        charge_0_index = defect_group.charges.index(0)
                        charge_0_defect_energy = defect_group.defect_energies[charge_0_index]
                except (ValueError, AttributeError):
                    pass

                if not charge_0_defect_energy:
                    continue

                atom_io = defect_group.atom_io
                base_energy = charge_0_defect_energy.formation_energy
                
                reservoir_contribution = 0.0
                for element, num_diff in atom_io.items():
                    if element in chem_pots:
                        reservoir_contribution -= num_diff * chem_pots[element]

                formation_energy = base_energy + reservoir_contribution
                formation_energies[defect_name] = formation_energy
            
            sorted_defects = sorted(formation_energies.items(), key=lambda item: item[0])
            for name, energy in sorted_defects:
                f.write(f"{name:<20} {energy:>25.4f}\n")
            
            f.write("\n")

    print(f"Output written to {output_filename}")


def run_macer_relax(target_dirs, isif=3, supercell_info=None, ff=None, model_path=None, device=None, fmax=0.03, verbose=False, modal=None):
    """
    Unified relaxation function for CPD and Defect workflows.
    Iterates over target_dirs and runs macer relaxation.
    """
    if not target_dirs:
        return []

    # Determine FF and Model if not provided
    if ff is None:
        available_ffs = get_available_ffs()
        if not available_ffs:
            print("Error: No MLFF packages installed.")
            return []
        ff = available_ffs[0]
    
    if device is None:
        device = DEFAULT_DEVICE
    
    if model_path is None:
        default_model_name = DEFAULT_MODELS.get(ff)
        if default_model_name:
            FFS_USING_MODEL_NAME = {"fairchem", "orb", "chgnet", "m3gnet"}
            if ff in FFS_USING_MODEL_NAME:
                model_path = default_model_name
            else:
                # Check CWD first, then package root
                cwd_model_path = os.path.join(os.getcwd(), "mlff-model", default_model_name)
                pkg_model_path = os.path.join(_model_root, default_model_name)
                
                if os.path.exists(cwd_model_path):
                    model_path = cwd_model_path
                else:
                    model_path = pkg_model_path
    
    print(f"Initializing {ff.upper()} calculator on {device}...")
    calc_kwargs = {"model_path": model_path, "device": device, "modal": modal}
    if ff == "mace":
        calc_kwargs["model_paths"] = [calc_kwargs["model_path"]]
        del calc_kwargs["model_path"]

    try:
        calculator = get_calculator(ff_name=ff, **calc_kwargs)
        print("Calculator initialized.")
    except Exception as e:
        print(f"Failed to initialize calculator: {e}")
        return []

    successful_dirs = []
    cwd = Path.cwd()
    original_stdout = sys.stdout

    for d in target_dirs:
        if verbose:
            print(f"Relaxing in {d.name}...")
        os.chdir(d) 
        try:
            log_name = f"relax-POSCAR_log.txt"
            with Logger(log_name) as lg:
                sys.stdout = lg
                write_pydefect_dummy_files(".") 
                relax_structure(
                    input_file="POSCAR",
                    fmax=fmax,
                    isif=isif,
                    device=device,
                    calculator=calculator, 
                    ff=ff,
                    outcar_name="OUTCAR", 
                    contcar_name="CONTCAR",
                    xml_name="vasprun.xml",
                    make_pdf=True,
                    write_json=True,
                    modal=modal
                )
            
                if Path("vasprun.xml").exists() or Path("OUTCAR").exists():
                     successful_dirs.append(d)
                     
                     # Generate defect_structure_info.json directly using CONTCAR if supercell_info is provided
                     # This logic comes from run_auto_defect[-full].py
                     if supercell_info:
                         try:
                            if Path("CONTCAR").exists() and Path("defect_entry.json").exists():
                                final_structure = Structure.from_file("CONTCAR")
                                defect_entry = loadfn("defect_entry.json")
                                
                                dsi_maker = MakeDefectStructureInfo(
                                    perfect=supercell_info.structure,
                                    initial=defect_entry.structure,
                                    final=final_structure,
                                    symprec=defaults.symmetry_length_tolerance,
                                    dist_tol=defaults.dist_tol
                                )
                                dsi_maker.defect_structure_info.to_json_file("defect_structure_info.json")
                                print(f"Generated defect_structure_info.json for {d.name}")

                                # Generate VESTA files for defect visualization
                                try:
                                    # Reload from file to ensure clean state matching CLI usage
                                    dsi_loaded = loadfn("defect_structure_info.json")
                                    vesta_maker = MakeDefectVestaFile(dsi_loaded)
                                    vesta_maker.initial_vesta.write_file("defect_initial.vesta")
                                    vesta_maker.final_vesta.write_file("defect.vesta")
                                    print(f"Generated VESTA files for {d.name}")
                                except Exception as e_vesta:
                                    print(f"Warning: Failed to generate VESTA files: {e_vesta}")

                         except Exception as e:
                            print(f"Warning: Failed to generate defect_structure_info.json for {d.name}: {e}")
            
        except Exception as e:
            sys.stdout = original_stdout
            print(f"Relaxation failed in {d.name}: {e}")
        finally:
            sys.stdout = original_stdout
            os.chdir(cwd)
            
    return successful_dirs
