
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
from ase.io import read

def plot_md_log(csv_path: str, out_prefix: str = "md_plot"):
    """Plot T, P, E from md.csv."""
    if not Path(csv_path).exists():
        print(f"Error: {csv_path} not found.")
        return
    
    df = pd.read_csv(csv_path)
    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    
    # Temperature
    axes[0].plot(df['time_fs'], df['T_K'], color='r')
    axes[0].set_ylabel("Temperature (K)")
    
    # Potential Energy
    axes[1].plot(df['time_fs'], df['Epot_eV'], color='b')
    axes[1].set_ylabel("Potential Energy (eV)")
    
    # Pressure
    if 'P_GPa' in df.columns:
        axes[2].plot(df['time_fs'], df['P_GPa'], color='g')
        axes[2].set_ylabel("Pressure (GPa)")
    
    axes[2].set_xlabel("Time (fs)")
    plt.tight_layout()
    plt.savefig(f"{out_prefix}.pdf")
    print(f"MD plots saved to {out_prefix}.pdf")

def plot_rdf(traj_path: str, out_prefix: str = "rdf_plot", r_max: float = 10.0, n_bins: int = 200):
    """Calculate and plot Radial Distribution Function (RDF) from trajectory."""
    print(f"Reading trajectory for RDF: {traj_path}")
    try:
        # Read the last 20% of frames for better statistics of equilibrated state
        all_configs = read(traj_path, index=':')
        n_frames = len(all_configs)
        start_idx = int(n_frames * 0.8)
        configs = all_configs[start_idx:]
        print(f"Using last {len(configs)} frames for RDF averaging.")
    except Exception as e:
        print(f"Error reading trajectory: {e}")
        return

    from ase.geometry.analysis import Analysis
    
    # Get all unique elements
    species = sorted(list(set(configs[0].get_chemical_symbols())))
    pairs = []
    for i, s1 in enumerate(species):
        for j, s2 in enumerate(species):
            if i <= j:
                pairs.append((s1, s2))

    plt.figure(figsize=(10, 6))
    
    for s1, s2 in pairs:
        print(f"  - Calculating RDF for {s1}-{s2}...")
        all_rdf = []
        for atoms in configs:
            ana = Analysis(atoms)
            # rdf returns [r_values, rdf_values]
            rdf = ana.get_rdf(rmax=r_max, nbins=n_bins, elements=[s1, s2])[0]
            all_rdf.append(rdf)
        
        avg_rdf = np.mean(all_rdf, axis=0)
        r_axis = np.linspace(0, r_max, n_bins)
        plt.plot(r_axis, avg_rdf, label=f"{s1}-{s2}")

    plt.xlabel(r"Distance $r$ ($\AA$)")
    plt.ylabel(r"Radial Distribution $g(r)$")
    plt.title(f"Radial Distribution Function (Averaged over last {len(configs)} frames)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0, r_max)
    plt.ylim(bottom=0)
    plt.tight_layout()
    plt.savefig(f"{out_prefix}.pdf")
    print(f"RDF plot saved to {out_prefix}.pdf")

def plot_relax_log(log_path: str, out_prefix: str = "relax_plot"):
    """Plot convergence from relax_log.txt."""
    # This is a bit more complex as it needs to parse the text log
    # For now, let's keep it simple or implement if requested specifically
    print("plot_relax_log: To be implemented (requires text log parsing).")
