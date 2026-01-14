from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from ase.io import read, write, iread
import yaml

# Constants
KB_J = 1.380649e-23     # Boltzmann constant in J/K
E_CHARGE = 1.60217663e-19 # Elementary charge in C
ANGSTROM = 1e-10        # m

def traj2xdatcar(traj_path: str, out_path: str = "XDATCAR", interval: int = 1):
    """
    Convert an ASE .traj file to a VASP XDATCAR file, 
    supporting variable cell (NPT) with full header repetition for each frame.
    Configuration numbers reflect the actual MD steps based on the interval.
    """
    traj_file = Path(traj_path)
    if not traj_file.exists():
        print(f"Error: Trajectory file '{traj_path}' not found.")
        return False
    
    print(f"Reading trajectory: {traj_path} (Interval: {interval})...")
    try:
        configs = list(iread(str(traj_file)))
        if not configs:
            print("Warning: Trajectory is empty.")
            return False
        
        print(f"Loaded {len(configs)} frames.")
        
        # Determine species and counts once
        atoms0 = configs[0]
        symbols = atoms0.get_chemical_symbols()
        species = list(dict.fromkeys(symbols))
        counts = [symbols.count(s) for s in species]
        # Use simple species list for system name to avoid "Al4"
        system_name = "".join(species)

        # Manual XDATCAR writing to match standard VASP format
        with open(out_path, 'w') as f:
            # --- Global Header (Once) ---
            atoms0 = configs[0]
            symbols = atoms0.get_chemical_symbols()
            species = list(dict.fromkeys(symbols))
            counts = [symbols.count(s) for s in species]
            system_name = "".join(species)

            f.write(f"{system_name}\n")
            f.write("    1.000000\n")
            # Initial lattice (placeholder, required by format)
            for vec in atoms0.cell:
                f.write(f"     {vec[0]:11.6f} {vec[1]:11.6f} {vec[2]:11.6f}\n")
            f.write(" " + " ".join(f"{s:>2}" for s in species) + "\n")
            f.write(" " + " ".join(f"{c:16d}" for c in counts) + "\n")

            # --- Frames ---
            for i, atoms in enumerate(configs):
                current_step = i * interval + 1
                
                # Write Lattice for every frame (standard for variable cell MD)
                for vec in atoms.cell:
                    f.write(f"     {vec[0]:11.6f} {vec[1]:11.6f} {vec[2]:11.6f}\n")
                
                f.write(f"Direct configuration= {current_step:5d}\n")
                scaled_pos = atoms.get_scaled_positions(wrap=True)
                for pos in scaled_pos:
                    f.write(f"   {pos[0]:.8f}   {pos[1]:.8f}   {pos[2]:.8f}\n")
                    
        print(f"Successfully converted {traj_path} -> {out_path}")
        return True
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False

def md_summary(csv_path: str):
    """Print a statistical summary of the md.csv file."""
    import pandas as pd
    csv_file = Path(csv_path)
    if not csv_file.exists():
        print(f"Error: CSV file '{csv_path}' not found.")
        return
    
    try:
        df = pd.read_csv(csv_path)
        print(f"\nMD Statistical Summary for: {csv_path}")
        print("-" * 50)
        cols = ['T_K', 'P_GPa', 'Epot_eV', 'Etot_eV', 'Vol_A3']
        cols = [c for c in cols if c in df.columns]
        summary = df[cols].describe().loc[['mean', 'std', 'min', 'max']]
        print(summary.to_string())
        print("-" * 50)
    except Exception as e:
        print(f"Error reading CSV: {e}")

def load_default_charges():
    """Load default oxidation states from pydefect database if available."""
    try:
        import pydefect
        pydefect_path = Path(pydefect.__file__).parent
        yaml_path = pydefect_path / "database" / "oxidation_state.yaml"
        if yaml_path.exists():
            with open(yaml_path, "r") as f:
                return yaml.safe_load(f)
    except:
        pass
    return {}

def detect_interval(input_path):
    """Try to detect interval from XDATCAR or neighboring md.csv."""
    input_path = Path(input_path)
    
    # 1. Try to find an XDATCAR (either the input itself or in the same dir)
    xdatcar_path = None
    if 'XDATCAR' in input_path.name:
        xdatcar_path = input_path
    else:
        # Look for XDATCAR in the same directory
        candidate = input_path.parent / "XDATCAR"
        if candidate.exists():
            xdatcar_path = candidate

    if xdatcar_path:
        try:
            configs = []
            with open(xdatcar_path, 'r') as f:
                for line in f:
                    if "Direct configuration=" in line:
                        val = line.split('=')[1].strip().split()[0]
                        configs.append(int(val))
                    if len(configs) >= 2:
                        break
            if len(configs) >= 2:
                return configs[1] - configs[0]
        except:
            pass

    # 2. Try to find md.csv in the same directory
    csv_path = input_path.parent / "md.csv"
    if csv_path.exists():
        try:
            import pandas as pd
            df = pd.read_csv(csv_path)
            if 'Step' in df.columns and len(df) >= 2:
                return int(df['Step'].iloc[1] - df['Step'].iloc[0])
        except:
            pass

    return None

def calculate_conductivity(traj_path, temp, dt, interval=1, charges_str="", out_prefix="md_results", charge_msd=False):
    """Calculate ionic conductivity from trajectory."""
    traj_path = Path(traj_path)
    if not traj_path.exists():
        print(f"Error: Trajectory file '{traj_path}' not found.")
        return

    # Auto-detect interval if not provided
    if interval == 1:
        detected = detect_interval(traj_path)
        if detected:
            interval = detected
            print(f"Auto-detected interval: {interval}")

    # Setup output path (same dir as input)
    out_dir = traj_path.parent
    out_prefix_path = out_dir / out_prefix
    log_file = out_prefix_path.with_suffix(".log")

    def log_print(msg):
        print(msg)
        with open(log_file, "a") as f:
            f.write(msg + "\n")

    with open(log_file, "w") as f:
        f.write("--- MD Conductivity Analysis ---\n")
        f.write(f"Input: {traj_path}\n")
        f.write(f"Temp: {temp} K\n")
        f.write(f"Time step: {dt} fs\n")
        f.write(f"Interval: {interval}\n")

    log_print(f"Reading trajectory: {traj_path}")
    try:
        # Auto-detect format
        fmt = 'vasp-xdatcar' if 'XDATCAR' in str(traj_path) else None
        # Use iread in a loop to avoid internal np.array issues in ASE/iread/list
        traj = []
        
        try:
            for atoms in iread(str(traj_path), format=fmt):
                traj.append(atoms)
        except Exception as e:
            if fmt == 'vasp-xdatcar':
                print(f"Standard XDATCAR reading failed: {e}. Trying robust mode...")
                import io
                with open(str(traj_path), 'r') as f:
                    content = f.read()
                if not content.strip():
                    raise ValueError("File is empty")
                first_line = content.splitlines()[0]
                pieces = content.split(first_line + '\n')
                traj = []
                for p in pieces:
                    if not p.strip(): continue
                    try:
                        frames = read(io.StringIO(first_line + '\n' + p), index=':', format='vasp-xdatcar')
                        traj.extend(frames)
                    except:
                        continue
                if not traj:
                    raise e
                print(f"Successfully read {len(traj)} frames in robust mode.")
            else:
                raise e
    except Exception as e:
        print(f"Error reading trajectory: {e}")
        if 'XDATCAR' in str(traj_path):
            print("Tip: VASP XDATCAR reading can be strict. Try using 'md.traj' instead for better compatibility.")
        return

    if not traj or len(traj) < 2:
        print("Error: Trajectory is too short or empty. Need at least 2 frames.")
        return

    n_steps = len(traj)
    vol_A3 = traj[0].get_volume()
    vol_m3 = vol_A3 * (ANGSTROM ** 3)
    species = sorted(list(set(traj[0].get_chemical_symbols())))
    
    # Charges
    defaults = load_default_charges()
    charges = defaults.copy()
    if charges_str:
        for p in charges_str.split(','):
            if ':' in p:
                el, q = p.split(':')
                charges[el.strip()] = float(q)

    log_print(f"Steps: {n_steps}, Volume: {vol_A3:.2f} A^3")
    log_print("Using oxidation states:")
    for sp in species:
        q = charges.get(sp, None)
        if q is None:
            q = 0.0
            log_print(f"  {sp}: {q} (Warning: not found in defaults, using 0.0)")
        else:
            log_print(f"  {sp}: {q}")
        charges[sp] = q
    
    # Use stack instead of np.array for safer creation from list of arrays
    pos_list = [atoms.get_scaled_positions() for atoms in traj]
    scaled_pos = np.stack(pos_list)
    
    d_scaled = scaled_pos[1:] - scaled_pos[:-1]
    d_scaled -= np.round(d_scaled)
    cum_disp_scaled = np.zeros_like(scaled_pos)
    cum_disp_scaled[1:] = np.cumsum(d_scaled, axis=0)
    
    cell = traj[0].get_cell()
    unwrapped_real = np.dot(cum_disp_scaled + scaled_pos[0], cell)

    dt_eff = dt * interval
    time_ps = np.arange(n_steps) * dt_eff * 1e-3

    results = {}
    plt.figure(figsize=(8, 6))
    
    for sp in species:
        indices = [i for i, s in enumerate(traj[0].get_chemical_symbols()) if s == sp]
        pos_sp = unwrapped_real[:, indices, :]
        disp_from_0 = pos_sp - pos_sp[0]
        msd = np.mean(np.sum(disp_from_0**2, axis=2), axis=1)
        
        s, e = int(n_steps*0.1), int(n_steps*0.9)
        if e > s + 1:
            slope, intercept = np.polyfit(time_ps[s:e], msd[s:e], 1)
        else:
            slope = 0
            intercept = 0
        
        D_cm2_s = (slope / 6.0) * 1e-8 * 1e4
        q = charges.get(sp, 0.0) * E_CHARGE
        sigma = ((len(indices)/vol_m3) * (q**2) * (slope/6.0*1e-8)) / (KB_J * temp) if q != 0 else 0
        
        results[sp] = {'D': D_cm2_s, 'sigma': sigma}
        log_print(f"\n--- Species: {sp} ---")
        log_print(f"  Diff. Coeff (D): {D_cm2_s:.3e} cm^2/s")
        log_print(f"  Conductivity (sigma_NE): {sigma:.3e} S/m ({sigma*10:.2f} mS/cm)")
        
        plt.plot(time_ps, msd, label=f"{sp} ($D$={D_cm2_s:.1e})")
        if e > s + 1:
            plt.plot(time_ps[s:e], slope * time_ps[s:e] + intercept, '--', alpha=0.5, color='gray')

    total_sigma = sum(r['sigma'] for r in results.values())
    log_print(f"\nTotal Conductivity: {total_sigma*10:.2f} mS/cm")
    
    plt.xlabel("Time (ps)")
    plt.ylabel(r"MSD (\AA^2)")
    plt.title(rf"MSD @ {temp}K (Total $\sigma$ = {total_sigma*10:.2f} mS/cm)")
    plt.legend(); plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plot_file = out_prefix_path.with_suffix(".pdf")
    plt.savefig(plot_file)
    log_print(f"Plot saved to {plot_file}")
    log_print(f"Log saved to {log_file}")