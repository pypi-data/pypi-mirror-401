import argparse
import os
import sys
import glob
import csv
import numpy as np

from ase.io import read, write
from ase.io.trajectory import Trajectory
from ase.md.npt import NPT
from ase.md.verlet import VelocityVerlet
# NVT: prefer Nose–Hoover chain; fallback to Berendsen if unavailable.
try:
    from ase.md.nose_hoover_chain import NoseHooverChainNVT as NVT_NHC
except Exception:
    NVT_NHC = None
try:
    from ase.md.nvtberendsen import NVTBerendsen as NVT_Ber
except Exception:
    NVT_Ber = None

from ase.md.logger import MDLogger
from ase.geometry import cellpar_to_cell
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution, Stationary, ZeroRotation
import ase.units as u


from macer.calculator.factory import get_calculator, get_available_ffs
from macer.relaxation.optimizer import relax_structure
from macer.utils.validation import check_poscar_format

# --- Defaults -----------------------------------------------------------------

from macer.defaults import DEFAULT_MODELS, _macer_root, _model_root, DEFAULT_DEVICE

# Unit conversion: 1 (eV/Å^3) = 160.21766208 GPa
EV_A3_TO_GPa = 160.21766208


def parse_poscar_header_for_xdatcar(poscar_path="POSCAR"):
    """Read species and counts from POSCAR header for XDATCAR blocks."""
    atoms = read(poscar_path, format="vasp")
    all_symbols = atoms.get_chemical_symbols()
    species = list(dict.fromkeys(all_symbols))
    counts = [all_symbols.count(spec) for spec in species]
    return species, counts


def get_md_parser():
    # Determine default force field based on installed extras
    available_ffs = get_available_ffs()
    _dynamic_default_ff = available_ffs[0] if available_ffs else None

    parser = argparse.ArgumentParser(
        description="Minimal NpT, NVT (NTE), or NVE MD with MACE + ASE (inputs: POSCAR; outputs: md.traj/md.log/XDATCAR/md.csv)",
        epilog="""
Examples:
  # NPT (Nose–Hoover barostat) — 600 K, 1 GPa, GPU (MPS), save every 100 steps
  macer md --ensemble npt --temp 600 --press 1.0 --ttau 100 --ptau 1000 --device cpu --nsteps 20000 --save-every 100

  # NVT (NTE; prefers Nose–Hoover chain, falls back to Berendsen) — 600 K, 5000 steps
  macer md --ensemble nte --temp 600 --ttau 100 --nsteps 5000

  # NVE (microcanonical) — initial temp 600 K, 5000 steps
  macer md --ensemble nve --temp 600 --nsteps 5000

  # Reproducible run (fixed seed) + adjusted print/save intervals
  macer md --ensemble npt --temp 300 --press 0.0 --ttau 100 --ptau 1000 --seed 42 --print-every 10 --save-every 100
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False # Don't add help here, main parser will handle it
    )

    parser.add_argument("--poscar", "-p", type=str, default=None,
                        help="Input POSCAR file (VASP format atomic structure input).")
    parser.add_argument("--cif", "-c", type=str, default=None,
                        help="Input CIF file (will be converted to POSCAR).")
    parser.add_argument("--model", default=None, help="Path to the MLFF model file. Defaults to a specific model for each FF if not provided.")
    parser.add_argument("--ff", type=str, default=_dynamic_default_ff, choices=get_available_ffs(), help="Force field to use.")
    parser.add_argument("--modal", type=str, default=None, help="Modal for SevenNet model, if required.")
    parser.add_argument("--device", choices=["cpu", "mps", "cuda"], default=DEFAULT_DEVICE, help="compute device")
    parser.add_argument("--ensemble", choices=["npt", "nte", "nve"], default="npt",
                        help="MD ensemble: npt (Nose–Hoover), nte (=NVT; Nose–Hoover chain or Berendsen), or nve (microcanonical)")
    parser.add_argument("--temp", type=float, default=300.0, help="target temperature [K] (for NPT/NTE and initial velocities in NVE)")
    parser.add_argument("--press", type=float, default=0.0, help="target pressure [GPa] (NPT only)")
    parser.add_argument("--tstep", type=float, default=2.0, help="MD time step [fs]")
    parser.add_argument("--nsteps", type=int, default=20000, help="number of MD steps")
    parser.add_argument("--ttau", type=float, default=100.0, help="thermostat time constant [fs] (NPT/NTE only)")
    parser.add_argument("--ptau", type=float, default=1000.0, help="barostat time constant [fs] (NPT only)")
    parser.add_argument("--save-every", type=int, default=100, help="traj/log save interval")
    parser.add_argument("--xdat-every", type=int, default=1, help="XDATCAR write interval")
    parser.add_argument("--print-every", type=int, default=1, help="stdout print interval")
    parser.add_argument("--seed", type=int, default=None, help="random seed (None for random)")
    parser.add_argument("--csv", default="md.csv", help="CSV log path for MD outputs")
    parser.add_argument("--xdatcar", default="XDATCAR", help="XDATCAR path")
    parser.add_argument("--traj", default="md.traj", help="ASE trajectory path")
    parser.add_argument("--log", default="md.log", help="MD text log path")
    parser.add_argument("--output-dir", type=str, default=".", help="Directory to save MD output files.")
    parser.add_argument("--initial-relax", action="store_true", help="Perform initial structural relaxation before MD.")
    parser.add_argument("--initial-relax-optimizer", type=str, default="FIRE", help="Optimizer for initial relaxation (e.g., FIRE, BFGS, LBFGS).")
    parser.add_argument("--initial-relax-fmax", type=float, default=0.01, help="Force convergence threshold for initial relaxation (eV/Å).")
    parser.add_argument("--initial-relax-smax", type=float, default=0.001, help="Stress convergence threshold for initial relaxation (eV/Å³).")
    parser.add_argument("--initial-relax-symprec", type=float, default=1e-5, help="Symmetry tolerance for FixSymmetry during initial relaxation (default: 1e-5 Å).")
    parser.add_argument(
        "--initial-relax-no-symmetry",
        dest="initial_relax_use_symmetry",
        action="store_false",
        help="Disable the FixSymmetry constraint during initial relaxation."
    )

    return parser


from pathlib import Path

def run_md_simulation(args):
    # Determine input path based on priority -p > -c
    is_cif_mode = False
    if args.poscar:
        input_file_path = args.poscar
    elif args.cif:
        input_file_path = args.cif
        is_cif_mode = True
    else:
        print("Error: Please provide structure input via -p (POSCAR) or -c (CIF) option.")
        sys.exit(1)

    # Check for input file existence first
    input_path = Path(input_file_path)
    if not input_path.is_file():
        print(f"Input file not found at '{input_path}'. Please provide a valid file.")
        sys.exit(1)

    if not is_cif_mode:
        try:
            check_poscar_format(input_path)
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

    # Handle CIF conversion
    if is_cif_mode:
        try:
            atoms_in = read(str(input_path))
            write('POSCAR', atoms_in, format='vasp')
            args.poscar = 'POSCAR' # Update args for later use
            print(f"Converted {input_file_path} to POSCAR.")
        except Exception as e:
            print(f"Error converting CIF {input_file_path}: {e}")
            sys.exit(1)

    # If output_dir is default ('.'), create a new directory based on input and mlff
    if args.output_dir == ".":
        input_poscar_dir = os.path.dirname(os.path.abspath(args.poscar))
        if not input_poscar_dir:
             input_poscar_dir = "."
        
        base_dir_name = f"MD-{Path(args.poscar).name}-mlff={args.ff}"
        output_dir_candidate = Path(input_poscar_dir) / base_dir_name
        
        # Handle duplicates
        final_output_dir = output_dir_candidate
        i = 1
        while final_output_dir.exists():
            final_output_dir = Path(input_poscar_dir) / f"{base_dir_name}-NEW{i:02d}"
            i += 1
        
        args.output_dir = str(final_output_dir)
        print(f"Output directory set to: {args.output_dir}")

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # 0) Read input structure.
    atoms = read(args.poscar, format="vasp")

    # Determine model_path based on FF if not explicitly provided
    current_model_path = args.model
    if current_model_path is None:
        default_model_name = DEFAULT_MODELS.get(args.ff)
        if default_model_name:
            # Check CWD first, then package root
            cwd_model_path = os.path.join(os.getcwd(), "mlff-model", default_model_name)
            pkg_model_path = os.path.join(_model_root, default_model_name)
            
            if os.path.exists(cwd_model_path):
                current_model_path = cwd_model_path
            else:
                current_model_path = pkg_model_path
        else:
            print(f"Warning: No default model found for force field '{args.ff}' in default-model.yaml. Proceeding without a model path.")

    # Calculator.
    try:
        calc_kwargs = {
            "model_path": current_model_path,
            "device": args.device,
            "modal": args.modal,
        }
        
        # If the selected ff is not mace, and the model path is the default mace model,
        # set model_path to None so that the respective calculator can use its own default.
        # This check should use current_model_path, not args.model, to avoid TypeError with None.
        if args.ff != "mace" and current_model_path is not None and DEFAULT_MODELS.get("mace") and os.path.abspath(current_model_path) == os.path.abspath(os.path.join(_model_root, DEFAULT_MODELS["mace"])):
            calc_kwargs["model_path"] = None

        # Special handling for MACE model_paths which expects a list
        if args.ff == "mace":
            calc_kwargs["model_paths"] = [calc_kwargs["model_path"]]
            del calc_kwargs["model_path"]

        calc = get_calculator(ff_name=args.ff, **calc_kwargs)
    except (RuntimeError, ValueError) as e:
        print(f"Error initializing calculator: {e}")
        sys.exit(1)

    atoms.calc = calc

    # Initial relaxation if requested
    if args.initial_relax:
        print(f"Performing initial relaxation with {args.initial_relax_optimizer} (fmax={args.initial_relax_fmax}, smax={args.initial_relax_smax})...")
        atoms = relax_structure(
            input_file=atoms,
            fmax=args.initial_relax_fmax,
            smax=args.initial_relax_smax,
            device=args.device,
            isif=3, # Full relaxation (atoms and cell)
            quiet=False, # Show output for initial relaxation
            model_path=args.model,
            optimizer_name=args.initial_relax_optimizer,
            # Suppress output files from relax_structure for initial relaxation
            contcar_name=os.devnull,
            outcar_name=os.devnull,
            xml_name=os.devnull,
            make_pdf=False,
            write_json=False,
            ff=args.ff,
            modal=args.modal,
            symprec=args.initial_relax_symprec,
            use_symmetry=args.initial_relax_use_symmetry
        )
        print("Initial relaxation completed.")
        # Re-attach calculator after relaxation, as relax_structure might create a new Atoms object
        try:
            calc = get_calculator(ff_name=args.ff, **calc_kwargs)
        except (RuntimeError, ValueError) as e:
            print(f"Error re-initializing calculator after relaxation: {e}")
            sys.exit(1)
        atoms.calc = calc

    # Upper-triangular cell is recommended for NPT (harmless for NVT; keeps cell normalized).
    tri_cell = cellpar_to_cell(atoms.cell.cellpar())
    atoms.set_cell(tri_cell, scale_atoms=True)
    atoms.pbc = True

    # Initialize velocities; remove net translation and rotation.
    rng = (np.random.default_rng(args.seed) if args.seed is not None else None)
    MaxwellBoltzmannDistribution(atoms, temperature_K=args.temp, force_temp=True, rng=rng)
    Stationary(atoms)
    ZeroRotation(atoms)

    # 1) MD integrator setup.
    timestep = args.tstep * u.fs
    ttime = args.ttau * u.fs

    if args.ensemble == "npt":
        # NPT with Nose–Hoover barostat (ASE NPT).
        extstress = args.press * u.GPa
        pfact = (args.ptau * u.fs) ** 2 * u.GPa
        dyn = NPT(
            atoms,
            timestep=timestep,
            temperature_K=args.temp,
            externalstress=extstress,
            ttime=ttime,
            pfactor=pfact,
        )
    elif args.ensemble == "nve":
        # NVE (microcanonical) with Velocity-Verlet integrator.
        dyn = VelocityVerlet(atoms, timestep=timestep)
    elif args.ensemble == "nte":
        # NVT (NTE): prefer Nose–Hoover chain; fallback to Berendsen.
        if NVT_NHC is not None:
            dyn = NVT_NHC(
                atoms,
                timestep=timestep,
                temperature_K=args.temp,
                tdamp=ttime,  # thermostat damping time constant
            )
        elif NVT_Ber is not None:
            dyn = NVT_Ber(
                atoms,
                timestep=timestep,
                temperature_K=args.temp,
                taut=ttime,  # Berendsen thermostat time constant
            )
        else:
            raise ImportError(
                "NVT integrator not found in this ASE installation. "
                "Please install/update ASE with NoseHooverChainNVT or NVTBerendsen."
            )
    else:
        # This should not be reached due to argparse choices
        raise ValueError(f"Unknown ensemble: {args.ensemble}")

    # 2) Logging: trajectory + text logger.
    traj_path = os.path.join(args.output_dir, args.traj)
    traj = Trajectory(traj_path, "w", atoms)
    dyn.attach(traj.write, interval=args.save_every)
    log_path = os.path.join(args.output_dir, args.log)
    logfile = open(log_path, "w")
    dyn.attach(MDLogger(dyn, atoms, logfile, header=True, stress=True, peratom=False),
               interval=args.save_every)

    # 3) XDATCAR setup.
    species, counts = parse_poscar_header_for_xdatcar(args.poscar)
    xdatcar_path = os.path.join(args.output_dir, args.xdatcar)
    xdat_handle = open(xdatcar_path, "w")

    # 4) CSV (custom observables) setup.
    csv_path = os.path.join(args.output_dir, args.csv)
    csv_handle = open(csv_path, "w", newline="")
    csv_writer = csv.writer(csv_handle)
    csv_writer.writerow(["step", "time_fs", "Epot_eV", "Ekin_eV", "Etot_eV", "T_K", "Vol_A3", "P_GPa", "H_eV"])

    # State & utilities.
    config_idx = 0
    step_counter = 0

    def write_xdatcar_block():
        """Append one XDATCAR configuration block from current Atoms state."""
        current_step = step_counter + 1
        
        # If it's the very first step, write the Title/Scale/Lattice/Species/Counts header
        if current_step == 1:
            xdat_handle.write(" ".join(species) + "\n")
            xdat_handle.write("    1.000000\n")
            # First frame lattice
            for vec in atoms.cell:
                xdat_handle.write(f"     {vec[0]:11.6f} {vec[1]:11.6f} {vec[2]:11.6f}\n")
            xdat_handle.write(" " + " ".join(f"{s:>2}" for s in species) + "\n")
            xdat_handle.write(" " + " ".join(f"{c:16d}" for c in counts) + "\n")

        # Standard VASP XDATCAR repeats Lattice for every frame in NPT/Variable Cell runs
        for vec in atoms.cell:
            xdat_handle.write(f"     {vec[0]:11.6f} {vec[1]:11.6f} {vec[2]:11.6f}\n")
            
        xdat_handle.write(f"Direct configuration= {current_step:5d}\n")
        for s in atoms.get_scaled_positions(wrap=True):
            xdat_handle.write(f"   {s[0]:.8f}   {s[1]:.8f}   {s[2]:.8f}\n")

    def collect_observables():
        """Compute a set of common MD observables from the current state."""
        epot = atoms.get_potential_energy()
        ekin = atoms.get_kinetic_energy()
        etot = epot + ekin
        temp = atoms.get_temperature()
        vol = atoms.get_volume()
        sigma = atoms.get_stress(voigt=False)  # stress tensor in eV/Å^3
        p_eVa3 = -np.trace(sigma) / 3.0
        p_GPa = p_eVa3 * EV_A3_TO_GPa
        H = etot + p_eVa3 * vol  # enthalpy-like quantity (E + pV) in eV
        t_fs = step_counter * args.tstep
        return epot, ekin, etot, temp, vol, p_GPa, H, t_fs

    def print_status_line(epot, ekin, etot, temp, vol, p_GPa, H, t_fs):
        """Pretty single-line status for stdout."""
        print(
            f"Step{step_counter:7d} | t={t_fs:7.2f} fs | "
            f"Epot={epot: .6f} eV | Ekin={ekin: .6f} eV | Etot={etot: .6f} eV | "
            f"T={temp:7.2f} K | Vol={vol:8.3f} Å^3 | P={p_GPa: 7.4f} GPa | H={H: .6f} eV"
        )

    def write_csv_line(epot, ekin, etot, temp, vol, p_GPa, H, t_fs):
        """Append one row of observables to the CSV log."""
        csv_writer.writerow([step_counter, t_fs, epot, ekin, etot, temp, vol, p_GPa, H])

    # Initial (step 0) record: console + XDATCAR + CSV.
    epot, ekin, etot, temp, vol, p_GPa, H, t_fs = collect_observables()
    print_status_line(epot, ekin, etot, temp, vol, p_GPa, H, t_fs)
    write_xdatcar_block()
    write_csv_line(epot, ekin, etot, temp, vol, p_GPa, H, t_fs)
    step_counter += 1  # subsequent integration starts at step 1

    # Per-step callback.
    def on_step():
        """Callback executed every step."""
        nonlocal step_counter
        epot, ekin, etot, temp, vol, p_GPa, H, t_fs = collect_observables()
        if (step_counter % args.print_every) == 0:
            print_status_line(epot, ekin, etot, temp, vol, p_GPa, H, t_fs)
        
        # Synchronize XDATCAR with traj saving (save_every)
        if (step_counter % args.save_every) == 0:
            write_xdatcar_block()
            
        write_csv_line(epot, ekin, etot, temp, vol, p_GPa, H, t_fs)
        step_counter += 1

    dyn.attach(on_step, interval=1)

    # 5) Run MD.
    dyn.run(args.nsteps)

    # 6) Finalize.
    xdat_handle.close()
    csv_handle.close()
    print(f"Done ({args.ensemble.upper()} MD): outputs saved to {args.output_dir} -> {args.traj} / {args.log} / {args.xdatcar} / {args.csv}")
