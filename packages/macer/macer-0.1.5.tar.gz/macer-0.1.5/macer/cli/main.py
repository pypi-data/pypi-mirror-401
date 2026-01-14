"""
Macer: Machine-learning accelerated Atomic Computational Environment for automated Research workflows
Copyright (c) 2025 The Macer Package Authors
Author: Soungmin Bae <soungminbae@gmail.com>
License: MIT
"""

import argparse
import sys
import os
import glob
import warnings
from ase.io import read, write

# Suppress common warnings from third-party libraries (e.g., Mattersim, Torch)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*weights_only=False.*")
warnings.filterwarnings("ignore", message=".*cuequivariance.*")
warnings.filterwarnings("ignore", category=UserWarning, module="pkg_resources")

# Suppress UserWarnings from specific MLFF libraries
for module_name in ["mattersim", "mace", "sevenn", "chgnet", "matgl", "nequip", "orb_models", "fairchem"]:
    warnings.filterwarnings("ignore", category=UserWarning, module=module_name)

from macer.utils.logger import Logger
from macer.relaxation.optimizer import relax_structure
from macer.relaxation.bulk_modulus import run_bulk_modulus_calculation
from macer.io.writers import write_pydefect_dummy_files
from macer.molecular_dynamics import cli
from macer.defaults import DEFAULT_MODELS, _macer_root, _model_root, DEFAULT_DEVICE
from macer.calculator.factory import get_available_ffs, ALL_SUPPORTED_FFS
from macer.utils.validation import check_poscar_format
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


def get_model_display_name(ff, model_arg):
    if not ff:
        return "Unknown"
    if model_arg:
        return f"{ff.upper()} (User: {os.path.basename(model_arg)})"
    default_model = DEFAULT_MODELS.get(ff)
    if default_model:
        return f"{ff.upper()} ({default_model})"
    return f"{ff.upper()} (Default)"


def print_banner(version, model_info):
    print(MACER_LOGO)
    print(f"  Version: {version}")
    print(f"  Model  : {model_info}")
    print(f"  Web    : https://github.com/soungmin-bae/macer")
    print("-" * 50)
    print("\n")


def print_model_download_help(model_path):
    model_name = os.path.basename(model_path)
    print(f"\nError: Model file not found: {model_path}")
    print(f"   Please download the pre-trained model and place it in the 'mlff-model' directory of the project.")
    print("\nDownload Instructions:")

    if "Allegro" in model_name:
         print(f"   1) Allegro-OAM-L-0.1.ase.nequip.pth")
         print(f"      This file is a pre-trained model for the Allegro/NequIP framework.")
         print(f"      Official Download (NequIP Model Hosting)")
         print(f"      https://www.nequip.net/models/mir-group/Allegro-OAM-L:0.1")
         print(f"         Downloaded as a .zip file. Extract it to get the model weights.")

    elif "sevennet" in model_name.lower():
         print(f"   2) checkpoint_sevennet_0.pth")
         print(f"      SevenNet pre-trained checkpoint.")
         print(f"      GitHub Raw Download")
         print(f"      https://raw.githubusercontent.com/MDIL-SNU/SevenNet/main/sevenn/pretrained_potentials/SevenNet_0__11Jul2024/checkpoint_sevennet_0.pth")

    elif "mace" in model_name.lower():
         print(f"   3) mace-omat-0-small.model")
         print(f"      MACE-OMAT series model.")
         print(f"      GitHub (MACE Foundations)")
         print(f"      https://github.com/ACEsuit/mace-foundations")
         print(f"      Hugging Face Model Hub")
         print(f"      https://huggingface.co/mace-foundations")
         print(f"      (Search for 'omat-small' or similar models)")

    elif "mattersim" in model_name.lower():
         print(f"   4) mattersim-v1.0.0-1M.pth")
         print(f"      Microsoft MatterSim pre-trained model.")
         print(f"      GitHub Raw Download")
         print(f"      https://raw.githubusercontent.com/microsoft/mattersim/main/pretrained_models/MatterSim-v1.0.0-1M.pth")
    
    print("\nSummary Table:")
    print("   | Filename                          | Download Link / Location                                                                 |")
    print("   |-----------------------------------|------------------------------------------------------------------------------------------|")
    print("   | Allegro-OAM-L-0.1.ase.nequip.pth  | https://www.nequip.net/models/mir-group/Allegro-OAM-L:0.1                                |")
    print("   | checkpoint_sevennet_0.pth         | https://raw.githubusercontent.com/MDIL-SNU/SevenNet/main/.../checkpoint_sevennet_0.pth   |")
    print("   | mace-omat-0-small.model           | GitHub: https://github.com/ACEsuit/mace-foundations                                      |")
    print("   |                                   | Hugging Face: https://huggingface.co/mace-foundations                                    |")
    print("   | mattersim-v1.0.0-1M.pth           | https://raw.githubusercontent.com/microsoft/mattersim/main/.../MatterSim-v1.0.0-1M.pth   |")
    print("\n")


def main():
    parser = argparse.ArgumentParser(
        description=MACER_LOGO + f"\nMachine-learning accelerated Atomic Computational Environment for automated Research workflows (v{__version__})",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--version", "-v", action="version", version=f"macer {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Relaxation command
    relax_parser = subparsers.add_parser(
        "relax",
        description=MACER_LOGO + f"\nmacer relax (v{__version__}): Relax atomic structures using MLFFs with VASP-like ISIF modes. Supports multiple input files (POSCAR-*).",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    relax_parser.add_argument("--poscar", "-p", type=str, nargs='+', default=None,
                        help="Input POSCAR file(s) or pattern(s) (VASP format atomic structure input, e.g. POSCAR-*).")
    relax_parser.add_argument("--cif", "-c", type=str, nargs='+', default=None,
                        help="Input CIF file(s) or pattern(s). Will be converted to POSCAR.")
    relax_parser.add_argument("--model", type=str, default=None,
                        help="Path to the MLFF model file. Defaults to a specific model for each FF if not provided.")
    relax_parser.add_argument("--ff", type=str, default=_dynamic_default_ff, choices=ALL_SUPPORTED_FFS, help="Force field to use. (default: mattersim)")
    relax_parser.add_argument("--modal", type=str, default="PBE", help="Modal for SevenNet model, if required (e.g., 'R2SCAN', 'PBE'). Defaults to 'PBE'.")
    relax_parser.add_argument("--fmax", type=float, default=0.01, help="Force convergence threshold (eV/Å).")
    relax_parser.add_argument("--smax", type=float, default=0.001, help="Stress convergence threshold (eV/Å³).")
    relax_parser.add_argument("--device", type=str, default=DEFAULT_DEVICE, choices=["cpu", "mps", "cuda"])
    relax_parser.add_argument("--isif", type=int, default=3, choices=list(range(9)),
                        help="""VASP ISIF mode for relaxation.
  0: Single-point calculation (no relaxation).
  1,2: Relax positions (cell fixed).
  3: Relax positions, cell shape, and volume.
  4: Relax positions and cell shape (volume fixed).
  5: Relax cell shape (positions and volume fixed).
  6: Relax cell shape and volume (positions fixed).
  7: Relax volume only (positions and shape fixed).
  8: Relax positions and volume (shape fixed).
""")
    relax_parser.add_argument("--subdir", action="store_true", help="Create a 'RELAX-*' subdirectory for outputs. By default, results are saved directly in the input directory.")
    relax_parser.add_argument(
        "--max-step",
        type=int,
        default=None,
        help="Maximum number of optimization steps.",
    )
    relax_parser.add_argument(
        "--optimizer",
        type=str,
        default="FIRE",
        help="Optimizer to use for relaxation (e.g., FIRE, BFGS, LBFGS).",
    )
    relax_parser.add_argument("--fix-axis", type=str, default="",
                        help="Fix lattice axes (a, b, c) during relaxation. Provide axes as a comma-separated string (e.g., 'a,b'). Only effective when the cell is allowed to change (e.g., ISIF=3, 4, 5, 6, 7).")
    relax_parser.add_argument(
        "--symprec",
        type=float,
        default=1e-5,
        help="Symmetry tolerance for FixSymmetry constraint (default: 1e-5 Å)."
    )
    relax_parser.add_argument(
        "--symmetry-off",
        dest="use_symmetry",
        action="store_false",
        help="Disable the FixSymmetry constraint during relaxation."
    )
    relax_parser.add_argument("--quiet", action="store_true")
    relax_parser.add_argument("--no-pdf", action="store_true", help="Disable log PDF output")
    relax_parser.add_argument("--pydefect", action="store_true", help="Write PyDefect-compatible files (calc_results.json, unitcell.yaml, perfect_band_edge_state.json).")
    relax_parser.add_argument("--contcar", type=str, default=None, help="Output CONTCAR file name.")
    relax_parser.add_argument("--outcar", type=str, default=None, help="Output OUTCAR file name.")
    relax_parser.add_argument("--vasprun", type=str, default=None, help="Output vasprun.xml file name.")

    # Add bulk modulus arguments
    bm_group = relax_parser.add_argument_group('Bulk Modulus Calculation')
    bm_group.add_argument("--bulk-modulus", action="store_true", help="Perform bulk modulus calculation instead of relaxation.")
    bm_group.add_argument("--strain", type=float, default=0.05, help="Maximum strain for E-V curve (e.g., 0.05 for +/- 5%% volume change).")
    bm_group.add_argument("--n-points", type=int, default=9, help="Number of points for E-V curve.")
    bm_group.add_argument("--eos", type=str, default="birchmurnaghan", choices=["birchmurnaghan", "murnaghan"], help="Equation of state for fitting (default: birchmurnaghan).")
    bm_group.add_argument("--no-eos-plot", action="store_true", help="Disable plotting the E-V curve.")

    # MD command
    # Get the MD parser from md.py and use it as a parent
    md_base_parser = cli.get_md_parser()
    md_parser = subparsers.add_parser(
        "md",
        description=MACER_LOGO + f"\nmacer md (v{__version__}): " + md_base_parser.description, # Use description from md_base_parser
        epilog=md_base_parser.epilog,           # Use epilog from md_base_parser
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[md_base_parser]                # Add md_base_parser as a parent
    )

    args = parser.parse_args()

    # Check if user mistakenly provided a FF name to --model
    if args.model and args.model.lower() in ALL_SUPPORTED_FFS:
        print(f"Error: '{args.model}' is a force field name, not a model file path.")
        print(f"Did you mean to use '--ff {args.model}' to select the force field?")
        print(f"Usage example: macer relax --ff {args.model} ...")
        sys.exit(1)

    if args.command in ["relax", "md"]:
        model_display = get_model_display_name(args.ff, args.model)
        print_banner(__version__, model_display)

    if args.command == "relax":
        if args.poscar:
            input_patterns = args.poscar
            is_cif_mode = False
        elif args.cif:
            input_patterns = args.cif
            is_cif_mode = True
        else:
            print("Error: Please provide structure input via -p (POSCAR) or -c (CIF) option.")
            sys.exit(1)

        input_files = []
        for pat in input_patterns:
            escaped_pat = glob.escape(pat)
            input_files.extend(glob.glob(escaped_pat))
        input_files = sorted(set(input_files))

        if not input_files:
            print(f"Input file not found at: {', '.join(input_patterns)}. Please provide a valid file.")
            sys.exit(1)

        if args.bulk_modulus:
            orig_stdout = sys.stdout
            for input_file in input_files:
                prefix = os.path.basename(input_file)
                real_input_path = input_file
                
                if is_cif_mode:
                    try:
                        atoms_in = read(input_file)
                        write('POSCAR', atoms_in, format='vasp')
                        real_input_path = 'POSCAR'
                        if prefix.lower().endswith('.cif'):
                            prefix = prefix[:-4]
                    except Exception as e:
                        print(f"Error converting CIF {input_file}: {e}")
                        continue

                output_dir = os.path.dirname(input_file) or "."
                log_name = os.path.join(output_dir, f"bulk_modulus-{prefix}.log")

                try:
                    with Logger(log_name) as lg:
                        sys.stdout = lg
                        print(f"--- Starting Bulk Modulus Calculation for {input_file} ---")
                        print(f"Log file will be saved to: {log_name}")
                        run_bulk_modulus_calculation(
                            input_path=real_input_path,
                            strain=args.strain,
                            n_points=args.n_points,
                            eos=args.eos,
                            no_eos_plot=args.no_eos_plot,
                            ff=args.ff,
                            model=args.model,
                            device=args.device,
                            modal=args.modal
                        )
                except Exception as e:
                    sys.stdout = orig_stdout # restore stdout
                    import traceback
                    print(f"Error during bulk modulus calculation for {input_file}: {e}")
                    traceback.print_exc()
                    # Continue to the next file
                finally:
                    sys.stdout = orig_stdout # restore stdout
            sys.exit(0)

        if args.ff is None:
            available = get_available_ffs()
            if not available:
                print("Error: No force field specified and no default force field could be determined because no supported MLFF packages appear to be installed.")
                print("Please install macer with an extra, e.g., 'pip install \"[mace]\"'")
            else:
                # This case should not happen if get_available_ffs() is not empty,
                # because _dynamic_default_ff would be set. But for robustness:
                print(f"Error: No force field specified and no default could be determined. Please specify one with --ff. Available: {available}")
            sys.exit(1)
        fix_axis = [ax.strip().lower() for ax in args.fix_axis.split(",") if ax.strip()]

        if (args.contcar or args.outcar or args.vasprun) and len(input_files) > 1:
            print("WARNING: Custom output names (--contcar, --outcar, --vasprun) are used with multiple input files.")
            print("Output files may be overwritten. Consider running files one by one.")

        orig_stdout = sys.stdout

        for infile in input_files:
            prefix = os.path.basename(infile)
            relax_input = infile
            
            if not is_cif_mode:
                try:
                    check_poscar_format(infile)
                except ValueError as e:
                    print(f"Error: {e}")
                    continue
            
            if is_cif_mode:
                try:
                    atoms_in = read(infile)
                    write('POSCAR', atoms_in, format='vasp')
                    if prefix.lower().endswith('.cif'):
                        prefix = prefix[:-4]
                    # Use atoms object for relax_structure to preserve prefix/metadata
                    atoms_in.info['tag'] = prefix if prefix else "structure"
                    relax_input = atoms_in
                except Exception as e:
                    print(f"Error converting CIF {infile}: {e}")
                    continue

            input_dir = os.path.dirname(os.path.abspath(infile)) or "."
            
            if not args.subdir:
                output_dir = input_dir
            else:
                base_dir_name = f"RELAX-{prefix}-mlff={args.ff}"
                output_dir_candidate = os.path.join(input_dir, base_dir_name)
                
                output_dir = output_dir_candidate
                i = 1
                while os.path.exists(output_dir):
                    output_dir = os.path.join(input_dir, f"{base_dir_name}-NEW{i:02d}")
                    i += 1
                
                os.makedirs(output_dir, exist_ok=True)
                print(f"Created output directory: {output_dir}")

            log_name = os.path.join(output_dir, f"relax-{prefix}_log.txt")

            contcar_name = os.path.join(output_dir, args.contcar or f"CONTCAR-{prefix}")
            outcar_name = os.path.join(output_dir, args.outcar or f"OUTCAR-{prefix}")
            xml_name = os.path.join(output_dir, args.vasprun or f"vasprun-{prefix}.xml")

            try:
                with Logger(log_name) as lg:
                    sys.stdout = lg
                    if args.pydefect:
                        write_pydefect_dummy_files(output_dir)
                        print("NOTE: perfect_band_edge_state.json and unitcell.yaml were written as dummy files for pydefect dei and pydefect des.")
                    
                    # Determine model_path and prepare info string
                    current_model_path = args.model
                    model_info_str = ""
                    # Define FFs that expect a model NAME, not a file path from mlff-model
                    FFS_USING_MODEL_NAME = {"fairchem", "orb", "chgnet", "m3gnet"}

                    if current_model_path:
                        model_info_str = f" (from --model option)"
                    else:
                        default_model_name = DEFAULT_MODELS.get(args.ff)
                        if default_model_name:
                            if args.ff in FFS_USING_MODEL_NAME:
                                # For these FFs, the default is a model name to be used directly
                                current_model_path = default_model_name
                            else:
                                # For other FFs, the default is a filename in the mlff-model directory
                                # Check CWD first, then package root
                                cwd_model_path = os.path.join(os.getcwd(), "mlff-model", default_model_name)
                                pkg_model_path = os.path.join(_model_root, default_model_name)
                                
                                if os.path.exists(cwd_model_path):
                                    current_model_path = cwd_model_path
                                else:
                                    # Use package path (may or may not exist, will be handled by error check)
                                    current_model_path = pkg_model_path
                                
                            model_info_str = f" (default for {args.ff.upper()}: {default_model_name})"
                        else:
                            model_info_str = f" (no model specified, using {args.ff.upper()} internal default)"
                    
                    print(f"Using {args.ff.upper()} on '{prefix}' | ISIF={args.isif} | fmax={args.fmax} | smax={args.smax} | device={args.device})")
                    if current_model_path:
                        print(f"  MLFF Model: {current_model_path}{model_info_str}")
                    else:
                        print(f"  MLFF Model:{model_info_str}")

                    try:
                        relax_structure(
                            input_file=relax_input,
                            fmax=args.fmax,
                            smax=args.smax,
                            device=args.device,
                            isif=args.isif,
                            fix_axis=fix_axis,
                            quiet=args.quiet,
                            contcar_name=contcar_name,
                            outcar_name=outcar_name,
                            xml_name=xml_name,
                            make_pdf=not args.no_pdf,
                            write_json=args.pydefect,
                            model_path=current_model_path, # Use the potentially modified model_path
                            max_steps=args.max_step,
                            optimizer_name=args.optimizer,
                            ff=args.ff,
                            modal=args.modal,
                            symprec=args.symprec,
                            use_symmetry=args.use_symmetry,
                            output_dir_override=output_dir
                        )
                    except (RuntimeError, ValueError) as e:
                        sys.stdout = orig_stdout # Restore stdout before printing error
                        print(f"Error: {e}")
                        if "is not installed" in str(e):
                            print(f"To use the '{args.ff}' force field, please reinstall macer with 'pip install \".[{args.ff}]\"'")
                        sys.exit(1)
                    results_path_info = f"in '{output_dir}'" if output_dir else "in the current directory"
                    print(f"Finished {prefix} -> Results saved {results_path_info}")
                    print("-" * 80)
            except Exception as e:
                sys.stdout = orig_stdout
                
                # Check for FileNotFoundError related to model
                model_path_candidate = locals().get('current_model_path')
                # Check if it is a FileNotFoundError (or OSError with errno 2) and involves the model path
                is_model_missing = False
                if isinstance(e, (FileNotFoundError, OSError)):
                    if model_path_candidate:
                         # normalize paths for comparison if possible, or just check inclusion
                         if str(model_path_candidate) in str(e) or os.path.basename(str(model_path_candidate)) in str(e):
                             is_model_missing = True
                
                if is_model_missing:
                    print_model_download_help(model_path_candidate)
                else:
                    print(f"[SKIP] {infile}: {e}")
                continue
            finally:
                sys.stdout = orig_stdout

    elif args.command == "md":
        cli.run_md_simulation(args) # Call the run_md_simulation function with parsed args

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

