"""
Macer: Machine-learning accelerated Atomic Computational Environment for automated Research workflows
Copyright (c) 2025 The Macer Package Authors
Author: Soungmin Bae <soungminbae@gmail.com>
License: MIT
"""

import sys
import os
import shutil
from argparse import Namespace
from pathlib import Path
import yaml

from pymatgen.core import Structure, Composition
from vise.cli.main_functions import get_poscar_from_mp
from pydefect.cli.vasp.main_vasp_functions import make_competing_phase_dirs, make_composition_energies
from pydefect.cli.main_functions import make_standard_and_relative_energies, make_cpd_and_vertices
from pydefect.defaults import defaults as pydefect_defaults

from macer.pydefect.utils import run_macer_relax, stabilize_target
from macer.utils.validation import check_poscar_format

def run_cpd_workflow(args):
    """
    Auto CPD workflow.
    args requires: formula, mpid, doping. Optional: poscar
    """
    
    # ------------------------------------------------------------------
    # Step 1: Get POSCAR and Determine Elements
    # ------------------------------------------------------------------
    target_formula = None
    host_elements = []
    competing_elements = []
    
    # If POSCAR is provided, use it to determine formula and elements
    if args.poscar:
        print(f"--- Step 1: Read input POSCAR from {args.poscar} ---")
        input_poscar_path = Path(args.poscar).absolute()
        if not input_poscar_path.exists():
            print(f"Error: {input_poscar_path} does not exist.")
            return
        
        # Validate POSCAR format (VASP 5 check)
        try:
            check_poscar_format(input_poscar_path)
        except ValueError as e:
            print(f"\nError: {e}\n")
            return

        try:
            structure = Structure.from_file(str(input_poscar_path))
            host_elements = [str(e) for e in structure.composition.elements]
            target_formula = structure.composition.reduced_formula
            print(f"Host Elements: {host_elements}, Target Formula: {target_formula}")
            
        except Exception as e:
            print(f"Failed to read input POSCAR: {e}")
            return

    else:
        # Standard flow using get_poscar_from_mp
        target_str = args.formula if args.formula else args.mpid
        if not target_str:
            print("\nError: No structure specified. Provide -p, -f or -m.")
            return

        print(f"--- Step 1: Retrieve POSCAR for {target_str} ---")
        
        args_gp = Namespace(mpid=args.mpid, formula=args.formula)
        try:
            get_poscar_from_mp(args_gp)
            if Path("POSCAR").exists():
                print(f"Successfully retrieved POSCAR for {target_str}.")
            else:
                print("Error: POSCAR file was not created.")
                return
        except Exception as e:
            print(f"Failed to retrieve POSCAR: {e}")
            return

        # Determine elements from the retrieved POSCAR
        try:
            structure = Structure.from_file("POSCAR")
            host_elements = [str(e) for e in structure.composition.elements]
            target_formula = structure.composition.reduced_formula
            print(f"Host Elements: {host_elements}, Target Formula: {target_formula}")
        except Exception as e:
            print(f"Failed to read POSCAR or determine elements: {e}")
            return

    # Determine competing elements
    competing_elements = host_elements.copy()
    if args.doping:
        for dopant in args.doping:
            if dopant not in competing_elements:
                competing_elements.append(dopant)
        print(f"Dopant(s) added: {args.doping}. Full competing element list: {competing_elements}")

    # ------------------------------------------------------------------
    # Create CPD Output Directory and Move Files
    # ------------------------------------------------------------------
    dopants_part = ""
    if args.doping:
        dopants_part = f"-DOPANG={'_'.join(args.doping)}"
    
    base_dir_name = f"CPD-target={target_formula}{dopants_part}-mlff={args.ff}"
    
    # Determine base path for output directory
    base_path = Path.cwd()
    if args.poscar:
        base_path = Path(args.poscar).absolute().parent
        
    cpd_output_dir = base_path / base_dir_name
    
    i = 1
    original_base = cpd_output_dir
    while cpd_output_dir.exists():
        cpd_output_dir = Path(f"{original_base}-NEW{i:03d}")
        i += 1
    
    print(f"\nCreating output directory: {cpd_output_dir.name}")
    print(f"Location: {cpd_output_dir.parent}")
    cpd_output_dir.mkdir()
    
    # Move/Copy initial files to the new directory
    if args.poscar:
        # Copy user provided POSCAR to the workspace
        shutil.copy(str(Path(args.poscar).absolute()), cpd_output_dir / "POSCAR")
    else:
        # Move downloaded files
        for filename in ["POSCAR", "prior_info.yaml"]:
            if Path(filename).exists():
                shutil.move(filename, cpd_output_dir / filename)
            
    # Change working directory
    original_cwd = Path.cwd()
    os.chdir(cpd_output_dir)
    print(f"Changed working directory to: {os.getcwd()}")

    try:
        # ------------------------------------------------------------------
        # Step 2: Generate competing phase directories
        # ------------------------------------------------------------------
        print(f"\n--- Step 2: Generate competing phase directories ({'-'.join(competing_elements)}) ---")
        args_mp = Namespace(elements=competing_elements, 
                            e_above_hull=pydefect_defaults.e_above_hull)
        try:
            make_competing_phase_dirs(args_mp)
            print("Competing phase directories created.")
        except Exception as e:
            print(f"Failed to generate competing phase directories: {e}")
            return

        # ------------------------------------------------------------------
        # Step 3: Run macer relax in each directory
        # ------------------------------------------------------------------
        print("\n--- Step 3: Run macer relax (Single MLFF Load) ---")
        
        # If input POSCAR was provided, ensure it is included as {formula}_host
        host_dir_name = f"{target_formula}_host"
        if args.poscar:
             host_dir = Path(host_dir_name)
             if not host_dir.exists():
                 host_dir.mkdir()
                 shutil.copy("POSCAR", host_dir / "POSCAR")
                 # Create dummy prior_info.yaml if not exists, as some tools might check for it
                 if not (host_dir / "prior_info.yaml").exists():
                      # Minimal content
                      with open(host_dir / "prior_info.yaml", "w") as f:
                          yaml.dump({"band_gap": 0.0, "total_magnetization": 0.0}, f)
                 print(f"Created {host_dir_name} from input POSCAR.")
        
        target_dirs = []
        for d in Path.cwd().iterdir():
            if d.is_dir() and (d / "POSCAR").exists():
                 # Check for prior_info.yaml OR if it is the host dir
                 if (d / "prior_info.yaml").exists() or d.name == host_dir_name:
                     target_dirs.append(d)
        
        target_dirs.sort(key=lambda x: x.name)
        
        if not target_dirs:
            print("No defect directories found to relax.")
            return

        # Use the utility function for relaxation (ISIF=3 for CPD)
        successful_dirs = run_macer_relax(
            target_dirs, 
            isif=3, 
            verbose=True, 
            fmax=args.fmax,
            ff=args.ff,
            model_path=args.model,
            device=args.device,
            modal=args.modal
        )

        # ------------------------------------------------------------------
        # Step 4: Generate composition_energies.yaml
        # ------------------------------------------------------------------
        print("\n--- Step 4: Generate composition_energies.yaml ---")
        if successful_dirs:
            yaml_filename = "composition_energies.yaml"
            yaml_input = yaml_filename if Path(yaml_filename).exists() else None
            
            args_mce = Namespace(yaml_file=yaml_input,
                                 dirs=successful_dirs,
                                 verbose=False)
            try:
                make_composition_energies(args_mce)
                print(f"Created/Updated {yaml_filename} from {len(successful_dirs)} calculations.")
            except Exception as e:
                print(f"Failed to create composition_energies.yaml: {e}")
        else:
            print("No successful calculations to process.")

        # ------------------------------------------------------------------
        # Step 5: Generate Standard and Relative Energies
        # ------------------------------------------------------------------
        print("\n--- Step 5: Generate Standard and Relative Energies ---")
        if Path("composition_energies.yaml").exists():
            # Filter composition_energies to exclude cross-impurity compounds
            try:
                with open("composition_energies.yaml", 'r') as f:
                    comp_energies = yaml.safe_load(f)
                
                filtered_comp_energies = {}
                removed_compounds = []
                
                for formula, data in comp_energies.items():
                    comp = Composition(formula)
                    elements_in_comp = [str(e) for e in comp.elements]
                    impurities_in_comp = [e for e in elements_in_comp if e not in host_elements]
                    
                    if len(impurities_in_comp) <= 1:
                        filtered_comp_energies[formula] = data
                    else:
                        removed_compounds.append(formula)
                
                if removed_compounds:
                    print(f"Filtering out compounds with multiple impurities: {removed_compounds}")
                
                filtered_yaml_filename = "composition_energies_filtered.yaml"
                with open(filtered_yaml_filename, 'w') as f:
                    yaml.dump(filtered_comp_energies, f)
                    
                args_sre = Namespace(composition_energies_yaml=filtered_yaml_filename)
                make_standard_and_relative_energies(args_sre)
                print("Generated standard_energies.yaml and relative_energies.yaml (from filtered data).")
                
            except Exception as e:
                print(f"Failed to generate standard/relative energies: {e}")
        else:
            print("composition_energies.yaml not found. Skipping Step 5.")

        # ------------------------------------------------------------------
        # Step 6: Chemical Potential Diagram
        # ------------------------------------------------------------------
        print(f"\n--- Step 6: Generate Chemical Potential Diagram for {target_formula} ---")
        if Path("relative_energies.yaml").exists() and target_formula:
            
            # Check for stability and apply shift if necessary
            applied_shift = stabilize_target("relative_energies.yaml", target_formula, manual_shift=args.energy_shift_target)
            
            # Note: We use host_elements for the vertices of the CPD
            args_cv = Namespace(rel_energy_yaml="relative_energies.yaml", 
                                target=target_formula, 
                                elements=host_elements) 
            try:
                # Check for unary system to avoid Qhull error
                if len(host_elements) == 1:
                    print(f"Unary system detected ({host_elements[0]}). Manually generating target_vertices.yaml.")
                    manual_vertices = {
                        "target": target_formula,
                        "A": {
                            "chem_pot": {host_elements[0]: 0.0},
                            "competing_phases": [],
                            "impurity_phases": []
                        }
                    }
                    with open("target_vertices.yaml", "w") as f:
                        yaml.dump(manual_vertices, f)
                    print("Generated target_vertices.yaml manually.")
                else:
                    make_cpd_and_vertices(args_cv)
                    print("Generated chem_pot_diag.json and target_vertices.yaml.")
                
                if applied_shift != 0.0 and Path("target_vertices.yaml").exists():
                    with open("target_vertices.yaml", "a") as f:
                        f.write(f"# Energy shift applied to make target stable: {applied_shift} eV/atom\n")
                    print(f"Appended stability shift info to target_vertices.yaml")
                    
            except Exception as e:
                print(f"Failed to generate chemical potential diagram: {e}")
        else:
            print("relative_energies.yaml not found or target formula missing. Skipping Step 6.")

    finally:
        # os.chdir(original_cwd) # Not strictly necessary if script ends here, but good practice
        pass
