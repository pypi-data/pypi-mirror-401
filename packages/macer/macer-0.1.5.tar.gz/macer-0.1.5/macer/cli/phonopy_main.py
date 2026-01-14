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
from pathlib import Path
from ase.io import read, write

# Suppress common warnings from third-party libraries (e.g., Mattersim, Torch)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*weights_only=False.*")
warnings.filterwarnings("ignore", message=".*cuequivariance.*")
warnings.filterwarnings("ignore", category=UserWarning, module="pkg_resources")

# Suppress UserWarnings from specific MLFF libraries
for module_name in ["mattersim", "mace", "sevenn", "chgnet", "matgl", "nequip", "orb_models", "fairchem"]:
    warnings.filterwarnings("ignore", category=UserWarning, module=module_name)

from macer.phonopy.relax_unit import run_relax_unit
from macer.phonopy.phonon_band import run_macer_workflow
from macer.phonopy.qha import add_qha_parser
from macer.phonopy.sscha import add_sscha_parser
from macer.defaults import DEFAULT_MODELS, _macer_root, _model_root, DEFAULT_DEVICE
from macer.calculator.factory import get_calculator, get_available_ffs, ALL_SUPPORTED_FFS
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


from macer.utils.logger import Logger


def _call_run_macer_workflow(args):
    """
    Helper function to adapt parsed arguments to run_macer_workflow.
    Handles multiple input POSCAR files.
    """
    is_cif_mode = False
    if args.input_files:
        input_patterns = args.input_files
    elif args.cif_files:
        input_patterns = args.cif_files
        is_cif_mode = True
    else:
        print("Error: Please provide structure input via -p (POSCAR) or -c (CIF) option.")
        sys.exit(1)

    input_files = []
    for pat in input_patterns:
        input_files.extend(glob.glob(pat))
    
    if not input_files:
        print(f"Position input file (POSCAR format) not found at: {', '.join(input_patterns)}. Please provide a valid position file in POSCAR format. If you provide a cif file, please use -c option.")
        sys.exit(1)

    original_cwd = os.getcwd()

    is_plusminus_val = 'auto'
    if args.is_plusminus:
        is_plusminus_val = True

    is_diagonal_val = True
    if not args.is_diagonal:
        is_diagonal_val = False

    # Determine symprec for seekpath
    symprec_for_seekpath = args.symprec
    if args.symprec == 1e-5 and args.tolerance_sr != 0.01:
        symprec_for_seekpath = args.tolerance_sr

    for filepath_str in sorted(list(set(input_files))):
        original_input_path = Path(filepath_str).resolve()
        
        if not is_cif_mode:
            try:
                check_poscar_format(original_input_path)
            except ValueError as e:
                print(f"Error: {e}")
                continue
        
        # Automatically enable write_arrow if a specific arrow q-point mode is selected
        if args.arrow_qpoint_gamma or (args.arrow_qpoint is not None):
            args.write_arrow = True
        
        # Default input path is the file itself
        input_path = original_input_path
        output_prefix = original_input_path.stem
        
        # Handle conversion
        if is_cif_mode:
            try:
                # Convert to POSCAR in the same directory
                target_dir = original_input_path.parent
                poscar_out = target_dir / "POSCAR"
                
                atoms_in = read(str(original_input_path))
                write(str(poscar_out), atoms_in, format='vasp')
                print(f"Converted {original_input_path.name} to {poscar_out}")
                
                input_path = poscar_out
                # Use the CIF stem as prefix
                output_prefix = original_input_path.stem
            except Exception as e:
                print(f"Error converting CIF {filepath_str}: {e}")
                continue

        output_dir = input_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)

        # Setup logger
        log_name = output_dir / f"macer_phonopy_pb-{output_prefix}.log"
        orig_stdout = sys.stdout
        
        try:
            with Logger(str(log_name)) as lg:
                sys.stdout = lg

                # Determine model path and info string
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
                                current_model_path = pkg_model_path
                        model_info_str = f" (default for {args.ff.upper()}: {default_model_name})"
                    else:
                        if args.ff:
                            model_info_str = f" (no model specified, using {args.ff.upper()} internal default)"
                        else:
                            sys.stderr.write("Error: No force field specified. Please use the --ff option.\n")
                            sys.exit(1)

                os.chdir(output_dir)

                dim_override_str = " ".join(map(str, args.dim)) if args.dim else None

                run_macer_workflow(
                    input_path=input_path,
                    min_length=args.length,
                    displacement_distance=args.amplitude,
                    is_plusminus=is_plusminus_val,
                    is_diagonal=is_diagonal_val,
                    macer_device=args.device,
                    macer_model_path=current_model_path,
                    model_info_str=model_info_str,
                    yaml_path_arg=args.yaml,
                    out_path_arg=args.out,
                    gamma_label=args.gamma,
                    symprec_seekpath=symprec_for_seekpath,
                    dim_override=dim_override_str,
                    no_defaults_band_conf=args.no_defaults,
                    atom_names_override=args.atom_names,
                    rename_override=args.rename,
                    tolerance_sr=args.tolerance_sr,
                    tolerance_phonopy=args.tolerance_phonopy,
                    macer_optimizer_name=args.optimizer,
                    fix_axis=args.fix_axis,
                    macer_ff=args.ff,
                    macer_modal=args.modal,
                    plot_gruneisen=args.plot_gruneisen,
                    gruneisen_strain=args.strain,
                    gmin=args.gmin,
                    gmax=args.gmax,
                    gruneisen_target_energy=args.target_energy,
                    filter_outliers_factor=args.filter_outliers,
                    use_relax_unit=args.use_relax_unit,
                    initial_fmax=args.initial_fmax,
                    initial_symprec=args.initial_symprec,
                    initial_isif=args.initial_isif,
                    output_prefix=output_prefix, # Added this argument
                    show_irreps=args.irreps,
                    irreps_qpoint=args.qpoint,
                    tolerance_irreps=args.tolerance_irreps,
                    write_arrow=args.write_arrow,
                    arrow_length=args.arrow_length,
                    arrow_min_cutoff=args.arrow_min_cutoff,
                    arrow_qpoint_gamma=args.arrow_qpoint_gamma,
                    arrow_qpoint=args.arrow_qpoint
                )

        except Exception as e: # Catch all exceptions
            sys.stdout = orig_stdout # Restore stdout before printing error
            import traceback
            sys.stderr.write("An unexpected error occurred during macer_phonopy pb execution:\n")
            sys.stderr.write(traceback.format_exc()) # Print full traceback
            sys.exit(1)

        finally:
            sys.stdout = orig_stdout # Restore stdout
            os.chdir(original_cwd)


def main():
    parser = argparse.ArgumentParser(
        description=MACER_LOGO + f"\nmacer_phonopy (v{__version__}): Machine-learning accelerated Atomic Computational Environment for automated Research workflows",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--version", "-v", action="version", version=f"macer_phonopy {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")



    # phonon-band command (alias: pb)
    phonon_band_parser = subparsers.add_parser(
        "phonon-band",
        aliases=["pb"],
        description=MACER_LOGO + f"\nmacer_phonopy pb (v{__version__}): Full phonopy workflow using MLFFs for phonon dispersion calculation, including band.conf generation.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    phonon_band_parser.add_argument(
        "-p", "--poscar", dest="input_files", required=False, nargs='+', default=None,
        help="One or more input cell files in VASP POSCAR format."
    )
    phonon_band_parser.add_argument(
        "-c", "--cif", dest="cif_files", required=False, nargs='+', default=None,
        help="One or more input cell files in CIF format."
    )
    phonon_band_parser.add_argument(
        "-l", "--length", type=float, default=20.0,
        help="Minimum length of supercell lattice vectors in Å (default: 20.0)."
    )
    phonon_band_parser.add_argument("--amplitude", type=float, default=0.01, help="Displacement amplitude in Å (default: 0.01).")
    phonon_band_parser.add_argument('--tolerance-sr', type=float, default=0.01, help='Symmetry tolerance (Å) for macer_phonopy sr. Default: 0.01.')
    phonon_band_parser.add_argument('--tolerance-phonopy', type=float, default=5e-3, help='Symmetry tolerance for phonopy. Default: 5e-3.')
    phonon_band_parser.add_argument(
        "--use-relax-unit",
        action="store_true",
        help="Use iterative relaxation/symmetrization (macer_phonopy sr) for the initial structure preparation. "
             "Default is a single 'macer relax' run."
    )
    phonon_band_parser.add_argument("--initial-fmax", type=float, default=1e-3,
                        help="Force convergence threshold for initial 'macer relax' in eV/Å. (default: 0.001)")
    phonon_band_parser.add_argument("--initial-symprec", type=float, default=1e-5,
                        help="Symmetry tolerance for FixSymmetry during initial 'macer relax' (default: 1e-5 Å).")
    phonon_band_parser.add_argument("--initial-isif", type=int, default=3,
                        help="VASP ISIF mode for initial 'macer relax'. (default: 3)")
    phonon_band_parser.add_argument('--pm', dest='is_plusminus', action="store_true", help='Generate plus and minus displacements for each direction.')
    phonon_band_parser.add_argument('--nodiag', dest='is_diagonal', action="store_false", help='Do not generate diagonal displacements.')
    phonon_band_parser.add_argument('--model', type=str, default=None, help='Path to the force field model file for macer.')
    phonon_band_parser.add_argument('--device', type=str, default=DEFAULT_DEVICE, choices=['cpu', 'mps', 'cuda'], help='Device for macer computation.')
    phonon_band_parser.add_argument("--ff", type=str, default=_dynamic_default_ff, choices=ALL_SUPPORTED_FFS, help="Force field to use. (default: mattersim)")
    phonon_band_parser.add_argument("--modal", type=str, default=None, help="Modal for SevenNet model.")
    phonon_band_parser.add_argument("--optimizer", type=str, default="FIRE", help="Optimizer to use for relaxation (e.g., FIRE, BFGS, LBFGS).")
    phonon_band_parser.add_argument(
        '--fix-axis', type=lambda s: [axis.strip() for axis in s.split(',')],
        help='Fix specified axes (e.g., "a,c" or "x,y,z") for supercell construction. The corresponding dimension will be set to 1.'
    )
    phonon_band_parser.add_argument(
        '--plot-gruneisen', '-pg', dest='plot_gruneisen', action="store_true",
        help='Plot Gruneisen parameter on phonon dispersion.'
    )
    phonon_band_parser.add_argument(
        '--strain', type=float, default=None,
        help='Strain for Gruneisen parameter. If not set, it will be estimated from the bulk modulus.'
    )
    phonon_band_parser.add_argument(
        '--gmin', type=float, default=None,
        help='Minimum Gruneisen parameter for color scale.'
    )
    phonon_band_parser.add_argument(
        '--gmax', type=float, default=None,
        help='Maximum Gruneisen parameter for color scale.'
    )
    phonon_band_parser.add_argument(
        '--filter-outliers', type=float, nargs='?', const=3.0, default=None,
        help='Filter outlier Grüneisen values from the plot. '
             'Optionally provide a factor to multiply the IQR (default: 3.0). '
             'Points outside [Q1 - factor*IQR, Q3 + factor*IQR] will be hidden.'
    )
    phonon_band_parser.add_argument(
        '--target-energy', type=float, default=10.0,
        help='Target energy in meV for bulk modulus-based strain estimation (default: 10.0).'
    )
    phonon_band_parser.add_argument("--yaml", default="phonopy_disp.yaml", type=Path, help="Path to phonopy_disp.yaml to read DIM from (for band.conf).")
    phonon_band_parser.add_argument("--out", default="band.conf", type=Path, help="Output band.conf file name.")
    phonon_band_parser.add_argument("--gamma", default="GM", help="Gamma label for BAND_LABELS (e.g., GM or Γ).")
    phonon_band_parser.add_argument("--symprec", type=float, default=1e-5, help="Symmetry tolerance passed to SeeK-path (default: 1e-5).")
    phonon_band_parser.add_argument("--dim", type=int, nargs='+', default=None, help='Set supercell dimension. Accepts 3 integers for a diagonal matrix (e.g., "2 2 2") or 9 for a full matrix. Overrides -l/--length.')
    phonon_band_parser.add_argument("--no-defaults", action="store_true", help="Do not include default FORCE_SETS, FC_SYMMETRY, EIGENVECTORS lines.")
    phonon_band_parser.add_argument("--atom-names", default=None, help='Override ATOM_NAME, e.g. "K Zr P O".')
    phonon_band_parser.add_argument("--rename", default=None, help='Rename mapping, e.g. "Na=K,Zr=Zr".')
    phonon_band_parser.add_argument(
        "--irreps", "--irreducible-representation", dest="irreps", action="store_true",
        help="Calculate irreducible representations."
    )
    phonon_band_parser.add_argument(
        "--qpoint", nargs=3, type=float, default=[0.0, 0.0, 0.0],
        help="Q-point for irreducible representations calculation. Default is 0 0 0."
    )
    phonon_band_parser.add_argument(
        "--tolerance-irreps", type=float, default=1e-5,
        help="Degeneracy tolerance for irreducible representations (default: 1e-5)."
    )
    
    arrow_group = phonon_band_parser.add_argument_group('Arrow (VESTA) Export Settings')
    arrow_group.add_argument(
        "--write-arrow", "-wa", dest="write_arrow", action="store_true",
        help="Write VESTA files for phonon mode visualization. Default is for special q-points."
    )
    arrow_group.add_argument(
        "--arrow-length", type=float, default=1.8,
        help="Set the length of the longest arrow in the visualization (in Angstroms). Default is 1.8."
    )
    arrow_group.add_argument(
        "--arrow-min-cutoff", type=float, default=0.3,
        help="Do not draw arrows with lengths smaller than this value (in Angstroms). Default is 0.3."
    )
    # Mutually exclusive group for filtering mode
    mode_group = arrow_group.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--arrow-qpoint-gamma", action="store_true",
        help="Write arrows only for the Gamma point."
    )
    mode_group.add_argument(
        "--arrow-qpoint", nargs=3, type=float, default=None,
        help="Write arrows for a specific q-point vector (3 floats)."
    )

    phonon_band_parser.set_defaults(func=_call_run_macer_workflow)

    # Add QHA sub-command
    add_qha_parser(subparsers)

    # Add SSCHA sub-command
    add_sscha_parser(subparsers)

    # symmetry-refine command
    symmetry_refine_parser = subparsers.add_parser(
        "symmetry-refine",
        aliases=["sr"],
        description=MACER_LOGO + f"\nmacer_phonopy sr (v{__version__}): Iteratively relax and symmetrize a unit cell using MLFFs and spglib.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    # ... (rest of symmetry_refine_parser arguments) ...

    symmetry_refine_parser.add_argument(
        "--poscar", "-p", dest="input_files", type=str, nargs='+',
        default=None,
        help="Input POSCAR file(s) or pattern(s) (e.g., POSCAR-*)."
    )
    symmetry_refine_parser.add_argument(
        "--cif", "-c", dest="cif_files", type=str, nargs='+',
        default=None,
        help="Input CIF file(s) or pattern(s)."
    )
    symmetry_refine_parser.add_argument(
        "--model", type=str, default=None,
        help="Path to the MACE model file. Defaults to the bundled mace-omat-0-small-fp32.model."
    )
    symmetry_refine_parser.add_argument(
        "--ff", type=str, default=_dynamic_default_ff,
        choices=ALL_SUPPORTED_FFS,
        help="Force field to use. (default: mattersim)"
    )
    symmetry_refine_parser.add_argument("--modal", type=str, default=None, help="Modal for SevenNet model.")
    symmetry_refine_parser.add_argument(
        "--device", type=str, default=DEFAULT_DEVICE,
        choices=["cpu", "mps", "cuda"],
        help="Compute device for MACE (cpu, mps, or cuda)."
    )
    symmetry_refine_parser.add_argument("--tolerance", type=float, default=0.01, help="Symmetry tolerance for spglib (in Å).")
    symmetry_refine_parser.add_argument(
        "--tolerance-sym", type=float, default=None,
        help="Symmetry tolerance for space group detection (in Å). If not set, uses --tolerance."
    )
    symmetry_refine_parser.add_argument(
        "--symprec-fix", type=float, default=1e-5,
        help="Symmetry tolerance for FixSymmetry constraint during relaxation (default: 1e-5 Å)."
    )
    symmetry_refine_parser.add_argument(
        "--symmetry-off",
        dest="use_symmetry",
        action="store_false",
        help="Disable the FixSymmetry constraint during relaxation steps."
    )
    symmetry_refine_parser.add_argument("--max-iterations", type=int, default=10, help="Maximum number of relaxation-symmetrization iterations.")
    symmetry_refine_parser.add_argument("--fmax", type=float, default=0.01, help="Force convergence threshold for relaxation (eV/Å).")
    symmetry_refine_parser.add_argument("--smax", type=float, default=0.001, help="Stress convergence threshold for relaxation (eV/Å³).")
    symmetry_refine_parser.add_argument(
        "--optimizer", type=str, default="FIRE",
        help="Optimizer to use for relaxation (e.g., FIRE, BFGS, LBFGS).",
    )
    symmetry_refine_parser.add_argument("--quiet", action="store_true", help="Suppress verbose output during relaxation steps.")
    symmetry_refine_parser.add_argument("--output-prefix", type=str, default=None, help="Prefix for output files. Defaults to the input POSCAR filename.")
    symmetry_refine_parser.add_argument(
        '--fix-axis', type=lambda s: [axis.strip() for axis in s.split(',')],
        help='Fix specified axes (e.g., "a,c" or "x,y,z") during relaxation. Atoms will not move along these axes.'
    )
    symmetry_refine_parser.set_defaults(func=run_relax_unit)

    args = parser.parse_args()
    if hasattr(args, "func"):
        if args.command == 'qha' and args.num_volumes < 4:
            parser.error("For the 'qha' command, number of volume points (--num-volumes) must be at least 4.")
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
