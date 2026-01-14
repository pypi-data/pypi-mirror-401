"""
Macer: Machine-learning accelerated Atomic Computational Environment for automated Research workflows
Copyright (c) 2025 The Macer Package Authors
Author: Soungmin Bae <soungminbae@gmail.com>
License: MIT
"""

import argparse
import sys
import glob
import copy
import os
from macer.pydefect.cpd import run_cpd_workflow
from macer.pydefect.defect import run_defect_workflow
from macer.pydefect.full import run_full_workflow
from macer.calculator.factory import get_available_ffs, ALL_SUPPORTED_FFS
from macer.defaults import DEFAULT_DEVICE
from macer import __version__

MACER_LOGO = r"""
███╗   ███╗  █████╗   ██████╗ ███████╗ ██████╗
████╗ ████║ ██╔══██╗ ██╔════╝ ██╔════╝ ██╔══██╗
██╔████╔██║ ███████║ ██║      █████╗   ██████╔╝
██║╚██╔╝██║ ██╔══██║ ██║      ██╔══╝   ██╔══██╗
██║ ╚═╝ ██║ ██║  ██║ ╚██████╗ ███████╗ ██║  ██║
╚═╝     ╚═╝ ╚═╝  ╚═╝  ╚═════╝ ╚══════╝ ╚═╝  ╚═╝
ML-accelerated Atomic Computational Environment for Research
"""

# Determine default force field based on installed extras
available_ffs = get_available_ffs()
_dynamic_default_ff = available_ffs[0] if available_ffs else None

def run_batch_workflow(args):
    # Determine the actual workflow function
    workflow_func = args.workflow_func
    
    if hasattr(args, 'poscar') and args.poscar:
        input_patterns = args.poscar
        input_files = []
        for pat in input_patterns:
            input_files.extend(glob.glob(pat))
        input_files = sorted(list(set(input_files)))
        
        if not input_files:
            print(f"No input files found matching: {input_patterns}")
            sys.exit(1)
            
        if len(input_files) > 1:
            print(f"Found {len(input_files)} input files. Running workflow sequentially.")
        
        # Save original CWD to restore after each workflow execution
        original_cwd = os.getcwd()

        for f in input_files:
            # Restore CWD to ensure relative paths work and outputs are in the correct place
            os.chdir(original_cwd)

            print(f"\n{'='*60}")
            print(f"Processing Input File: {f}")
            print(f"{'='*60}\n")
            
            # Create a copy of args for this iteration
            single_args = copy.copy(args)
            single_args.poscar = f
            
            try:
                workflow_func(single_args)
            except Exception as e:
                print(f"Error processing {f}: {e}")
                import traceback
                traceback.print_exc()
                continue
    else:
        # No poscar provided (e.g. cpd without -p)
        workflow_func(args)

def main():
    parser = argparse.ArgumentParser(
        description=MACER_LOGO + f"\nmacer_pydefect (v{__version__}): Automated Point Defect Calculations with MLFFs",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--version", "-v", action="version", version=f"macer_pydefect {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Common MLFF arguments
    mlff_parent = argparse.ArgumentParser(add_help=False)
    mlff_parent.add_argument("--ff", type=str, default=_dynamic_default_ff, choices=ALL_SUPPORTED_FFS, help="Force field to use. (default: mattersim)")
    mlff_parent.add_argument("--model", type=str, default=None, help="Path to the MLFF model file.")
    mlff_parent.add_argument("--device", type=str, default=DEFAULT_DEVICE, choices=["cpu", "mps", "cuda"], help="Compute device.")
    mlff_parent.add_argument("--modal", type=str, default=None, help="Modal for SevenNet model.")

    # CPD command
    cpd_parser = subparsers.add_parser(
        "cpd",
        parents=[mlff_parent],
        description="Run Chemical Potential Diagram (CPD) workflow.",
        help="Generate CPD and target vertices."
    )
    cpd_parser.add_argument("-f", "--formula", type=str, help="Formula to retrieve from Materials Project (e.g., MgAl2O4)")
    cpd_parser.add_argument("-m", "--mpid", type=str, help="Materials Project ID (e.g., mp-3536)")
    cpd_parser.add_argument("-d", "--doping", type=str, nargs='+', help="Dopant element(s) (e.g., Cl)")
    cpd_parser.add_argument("-p", "--poscar", type=str, nargs='+', help="Input POSCAR file(s) (Optional)")
    cpd_parser.add_argument("--fmax", type=float, default=0.03, help="Force convergence threshold (eV/Å). Default: 0.03")
    cpd_parser.add_argument("--energy-shift-target", type=float, default=0.0, help="Manually shift target energy (eV/atom). Default: 0.0")
    cpd_parser.set_defaults(func=run_batch_workflow, workflow_func=run_cpd_workflow)

    # Defect command
    defect_parser = subparsers.add_parser(
        "defect",
        parents=[mlff_parent],
        description="Run Defect Analysis workflow (Supercell generation, Relaxation, Analysis).",
        help="Calculate defect formation energies."
    )
    defect_parser.add_argument("-p", "--poscar", type=str, nargs='+', required=True, help="Input POSCAR file(s) (Perfect Unitcell)")
    defect_parser.add_argument("-d", "--doping", type=str, nargs='+', help="Dopant element(s) (e.g., Cl)")
    defect_parser.add_argument("-s", "--std_energies", type=str, required=True, help="Path to standard_energies.yaml")
    defect_parser.add_argument("-t", "--target_vertices", type=str, required=True, help="Path to target_vertices.yaml")
    defect_parser.add_argument("--matrix", nargs="+", type=int, help="Supercell matrix applied to the conventional cell. 1, 3 or 9 components are accepted.")
    defect_parser.add_argument("--min_atoms", type=int, default=50, help="Minimum number of atoms (default: 50)")
    defect_parser.add_argument("--max_atoms", type=int, default=300, help="Maximum number of atoms (default: 300)")
    defect_parser.add_argument("--no_symmetry_analysis", dest="analyze_symmetry", action="store_false", help="Set if symmetry is not analyzed. If set, sites.yaml file is required.")
    defect_parser.set_defaults(analyze_symmetry=True)
    defect_parser.add_argument("--sites_yaml", type=str, dest="sites_yaml_filename", help="Path to sites.yaml file.")
    defect_parser.add_argument("--fmax", type=float, default=0.03, help="Force convergence threshold (eV/Å). Default: 0.03")
    defect_parser.set_defaults(func=run_batch_workflow, workflow_func=run_defect_workflow)

    # Full command
    full_parser = subparsers.add_parser(
        "full",
        parents=[mlff_parent],
        description="Run Full Defect Analysis workflow (CPD + Defect Analysis).",
        help="Run both CPD and Defect Analysis workflows."
    )
    full_parser.add_argument("-f", "--formula", type=str, help="Formula to retrieve from Materials Project (e.g., MgAl2O4)")
    full_parser.add_argument("-m", "--mpid", type=str, help="Materials Project ID (e.g., mp-3536)")
    full_parser.add_argument("-p", "--poscar", type=str, nargs='+', help="Input POSCAR file(s) (Perfect Unitcell)")
    full_parser.add_argument("-d", "--doping", type=str, nargs='+', help="Dopant element(s) (e.g., Cl)")
    full_parser.add_argument("--matrix", nargs="+", type=int, help="Supercell matrix applied to the conventional cell. 1, 3 or 9 components are accepted.")
    full_parser.add_argument("--min_atoms", type=int, default=50, help="Minimum number of atoms (default: 50)")
    full_parser.add_argument("--max_atoms", type=int, default=300, help="Maximum number of atoms (default: 300)")
    full_parser.add_argument("--no_symmetry_analysis", dest="analyze_symmetry", action="store_false", help="Set if symmetry is not analyzed. If set, sites.yaml file is required.")
    full_parser.set_defaults(analyze_symmetry=True)
    full_parser.add_argument("--sites_yaml", type=str, dest="sites_yaml_filename", help="Path to sites.yaml file.")
    full_parser.add_argument("--fmax", type=float, default=0.03, help="Global force convergence threshold (eV/Å). Default: 0.03. Can be overridden by --fmax-cpd or --fmax-defect.")
    full_parser.add_argument("--fmax-cpd", type=float, help="Force convergence threshold for CPD step (eV/Å). Overrides --fmax.")
    full_parser.add_argument("--fmax-defect", type=float, help="Force convergence threshold for Defect step (eV/Å). Overrides --fmax.")
    full_parser.add_argument("--energy-shift-target", type=float, default=0.0, help="Manually shift target energy (eV/atom). Default: 0.0")
    full_parser.set_defaults(func=run_batch_workflow, workflow_func=run_full_workflow)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
