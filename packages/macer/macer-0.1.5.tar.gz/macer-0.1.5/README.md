<img src="docs/macer_logo.png" alt="macer Logo" width="30%">

# macer

![Version](https://img.shields.io/badge/version-0.1.5-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**macer: Machine-learning accelerated Atomic Computational Environment for automated Research workflows**

The `macer` package provides an automated command-line workflow for crystal structure relaxation, molecular dynamics simulations, and lattice dynamics calculations, using a variety of Machine-Learned Force Fields (MLFFs). It integrates universal Machine Learning Interatomic Potentials (uMLIP) calculators like [MACE](https://github.com/ACEsuit/mace-foundations), [MatterSim](https://github.com/microsoft/mattersim), [SevenNet](https://github.com/MDIL-SNU/SevenNet), [CHGNet](https://github.com/CederGroupHub/chgnet), [M3GNet](https://github.com/materialsvirtuallab/m3gnet), [Allegro](https://www.nequip.net/), [Orb](https://github.com/orbital-materials/orb-models), and [FairChem](https://github.com/facebookresearch/fairchem) with libraries like [ASE (Atomic Simulation Environment)](https://wiki.fysik.dtu.dk/ase/), [Phonopy](https://github.com/phonopy/phonopy), and [symfc](https://github.com/symfc/symfc). The self-consistent harmonic approximation (SSCHA) implementation is based on [qscaild](https://github.com/vanroeke/qscaild).

---

## Key Features

-   **MLFF Integration**: Utilizes various MLFFs as interatomic potential calculators for all supported workflows with same cli commands.
-   **Structure Relaxation**: Employs ASE optimizers (FIRE, BFGS, etc.) with VASP-compatible `ISIF` modes. Results are saved directly in the input directory by default (VASP-style).
-   **Molecular Dynamics**: Performs NPT, NVT (Nose–Hoover chain / Berendsen), and NVE ensemble simulations with logging.
-   **Phonon Calculations**: Uses `Phonopy` to calculate phonon band structure, density of states (DOS), **irreducible representations (irreps)**, and Grüneisen parameters.
-   **Phonon Mode Visualization**: Automatically generates **VESTA visualization files** (.vesta) and **magnetic CIF (.mcif) files** with displacement arrows for phonon modes at symmetry points or user-specified q-points.
-   **Quasiharmonic Approximation (QHA)**: Fully automates the calculation of thermodynamic properties like thermal expansion and heat capacity. Includes options for volume sampling.
-   **Self-Consistent Harmonic Approximation (SSCHA)**: An automated workflow to compute temperature-dependent effective force constants, follwing the [qscaild](https://github.com/vanroeke/qscaild) package. The implementation features:
    -   **Ensemble Reweighting:** Iteratively refines force constants by reweighting an ensemble of atomic configurations.
    -   **Simultaneous FC2 and FC3 Fitting:** Uses [symfc](https://github.com/symfc/symfc) to simultaneously fit both 2nd (harmonic) and 3rd (cubic) order force constants from a single ensemble, enabling the calculation of anharmonic free energy contributions.
    -   **Self-Consistent Volume Optimization:** Automatically finds the equilibrium volume at a target temperature by minimizing the SSCHA free energy.
    -   **Automatic Ensemble Regeneration:** Detects numerical instability (Effective Sample Size collapse) and automatically regenerates a new ensemble based on the current best-guess force constants.
    -   **Ensemble Generation:** Supports generating ensembles from random harmonic displacements or from full **Molecular Dynamics (MD)** simulations with proper equilibration and thermostatting (Langevin/NVE).
    -   **Flexible Ensemble Handling:** Can load pre-calculated ensembles in both binary (`.npz`) and text (`.txt`) formats to resume or analyze runs.
    -   **Outputs:** Generates convergence plots, iterative phonon band structures, the weighted-average atomic structure, and an atomic position distribution file (`distribution.dat`).
-   **Point Defect Analysis**: Automates point defect calculations (Chemical Potential Diagram, Defect Formation Energies) using `pydefect` and `vise`, integrating MLFF relaxation via `macer`.
    -   **Batch Processing**: Supports processing multiple input unit cells or glob patterns (e.g., `POSCAR-mp-*`) in a single command.
    -   **Automatic Stabilization**: Automatically detects if a target compound is thermodynamically unstable (above the convex hull) and applies a minimal energy shift to stabilize it, allowing the workflow to proceed.
    -   **Standard Energy Reporting**: Included in the summary are standard formation energies (at chemical potential = 0) for neutral (charge 0) defects.
    -   **Automatic VESTA Visualization**: Generates `defect_initial.vesta` and `defect.vesta` files automatically in each defect calculation directory for easy structure inspection.
---

## Installation & Usage (uv)

Macer uses `uv` for fast, conflict-free dependency management.

### 1. Install uv
Before using Macer, you must have `uv` installed on your system.
Please refer to the [official uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) or use one of the following:

```bash
# macOS / Linux (via brew)
brew install uv

# OR via curl
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Choose Installation Method

#### Option 1: Install from Source (Recommended for Development)
If you have cloned the repository from GitHub:

1.  **Create and activate a virtual environment:**
    ```bash
    uv venv macer_env
    source macer_env/bin/activate
    ```
2.  **Install in editable mode:**
    ```bash
    uv pip install -e .
    ```
3.  **Use wrapper scripts:**
    The `bin/` directory contains special wrapper scripts (`macer`, `macer_phonopy`, `macer_pydefect`, `macer_util`) that automatically manage isolated environments for different force fields.
    *   **Default Behavior**: Running `./bin/macer` without the `--ff` option will use **MatterSim** by default.
    *   **Specific Force Fields**: To use a specific model like MACE, simply add `--ff mace`. The script will handle the necessary environment setup.
    ```bash
    ./bin/macer relax -p POSCAR           # Uses MatterSim (default)
    ./bin/macer relax -p POSCAR --ff mace  # Uses MACE
    ```

#### Option 2: Install from PyPI (Standard User)
To install Macer directly into your environment:

1.  **Basic installation:**
    ```bash
    uv pip install macer
    ```
    This installs the core workflows. By default, **MatterSim** is included as the primary force field.
2.  **Install with specific force fields (Extras):**
    Due to potential dependency conflicts (like `e3nn` versions), other force fields are provided as "extras". Install the one you need using square brackets:
    ```bash
    uv pip install "macer[mace]"       # To use MACE
    uv pip install "macer[sevennet]"   # To use SevenNet
    uv pip install "macer[chgnet]"     # To use CHGNet
    ```

### 3. Setup (Add to PATH)
For convenience, add the `bin/` directory (for Option 1) or your environment's script path to your `PATH`.

```bash
# Example for Option 1
export PATH=$PATH:/path/to/your/macer-project/bin
```

---

## Legacy Installation (pip/conda)

If you prefer standard `pip` or `conda` without `uv`:

1.  Create a fresh environment.
2.  Install the core package:
    ```bash
    pip install -e .
    ```
3.  Install the specific requirements for your desired force field:
    ```bash
    pip install -r requirements/mace.txt
    ```
    *(Note: Do not install conflicting requirements like `mace.txt` and `sevennet.txt` in the same environment.)*

---

## Usage

The `macer` CLI provides two main commands: `macer` for relaxation and MD, and `macer_phonopy` for all lattice dynamics workflows.

```bash
# Get help for each main command and its subcommands
macer -h
macer relax -h
macer md -h

macer_phonopy -h
macer_phonopy sr -h
macer_phonopy pb -h
macer_phonopy qha -h
macer_phonopy sscha -h

macer_pydefect -h
macer_pydefect cpd -h
macer_pydefect defect -h
macer_pydefect full -h

macer_util -h
macer_util md -h
```

### Relaxation Examples (`macer relax`)

By default, relaxation results (`CONTCAR-*`, `OUTCAR-*`, etc.) are saved directly in the same directory as the input structure file. Use `--subdir` if you prefer a dedicated `RELAX-*` directory.

```bash
# Full cell relaxation (atoms + lattice) using the default force field
macer relax --poscar POSCAR --isif 3

# Batch relaxation for multiple structures using MACE
macer relax --poscar POSCAR-* --isif 2 --ff mace

# Use a specific Orb model (auto-downloaded by name)
macer relax --poscar POSCAR --isif 3 --ff orb --model orb_v3_conservative_inf_omat

# Generate outputs for PyDefect (single-point calculation)
macer relax --poscar POSCAR --isif 0 --pydefect

# Relaxation with a fixed c-axis
macer relax --poscar POSCAR --isif 3 --fix-axis c

# Calculate bulk modulus for multiple files
macer relax -p POSCAR-001 POSCAR-002 --bulk-modulus
```

### Molecular Dynamics Examples (`macer md`)

```bash
# NPT simulation at 600 K and 1 GPa using the default FF
macer md --ensemble npt --temp 600 --press 1.0 --nsteps 20000

# NVT simulation using MACE, with an initial relaxation step
macer md --ensemble nte --temp 600 --nsteps 5000 --ff mace --initial-relax

# Reproducible NVE run with a fixed random seed
macer md --ensemble nve --temp 300 --nsteps 10000 --seed 42
```

### Phonon & Lattice Dynamics Examples (`macer_phonopy`)

#### Unit Cell Symmetrization (`macer_phonopy sr`)
This is a first step for any lattice dynamics calculation to ensure a high-symmetry structure.
```bash
# Iteratively relax and symmetrize a unit cell
macer_phonopy sr --poscar POSCAR --tolerance 1e-3
```

#### Phonon Bands & Grüneisen Parameter (`macer_phonopy pb`)
Calculates and plots the phonon band structure.
```bash
# Calculate phonon bands using an automatically determined supercell size
macer_phonopy pb -p ./example/POSCAR

# Explicitly set the supercell dimension
macer_phonopy pb -p ./example/POSCAR --dim 2 2 2

# Calculate and plot the Grüneisen parameter, with automatic strain estimation
macer_phonopy pb -p ./example/POSCAR --dim 2 2 2 --plot-gruneisen

# Calculate irreducible representations and generate VESTA visualization for the Gamma point
macer_phonopy pb -p ./example/POSCAR --irreps

# Generate VESTA visualization for all high-symmetry points in the band path
macer_phonopy pb -p ./example/POSCAR --write-arrow

# Generate VESTA arrows for a specific user-defined q-point vector
macer_phonopy pb -p ./example/POSCAR --write-arrow --arrow-qpoint 0.2 0.2 0.2
```

#### Quasiharmonic Approximation (`macer_phonopy qha`)
Automates the full QHA workflow to compute thermodynamic properties.
```bash
# Run a full QHA workflow, automatically estimating the volume range
macer_phonopy qha --poscar POSCAR --num-volumes 7 --tmax 1200

# Run QHA with a specific supercell dimension and a manually specified volume range
macer_phonopy qha --poscar POSCAR --dim 2 2 2 --length-factor-min 0.98 --length-factor-max 1.02

# Run QHA using a local polynomial fit for the equation of state
macer_phonopy qha --poscar POSCAR --eos local_poly
```

#### Self-Consistent Harmonic Approximation (`macer_phonopy sscha`)
Performs a SSCHA workflow to find temperature-dependent effective force constants, featuring automatic ensemble regeneration.

```bash
# Basic SSCHA run at 300K with auto-sized supercell
macer_phonopy sscha -p POSCAR -T 300 --free-energy-conv 0.1

# Use a MD-generated ensemble for accuracy
macer_phonopy sscha -p POSCAR -T 500 --reference-method md --reference-md-nsteps 2000 --reference-md-nequil 500

# Run with ensemble regeneration enabled and a fixed random seed for reproducibility
macer_phonopy sscha -p POSCAR -T 300 --max-regen 5 --seed 1234

# Load a pre-calculated initial force constant and a reference ensemble to save time
macer_phonopy sscha -p POSCAR -T 300 --read-initial-fc path/to/FC_init --reference-ensemble path/to/ensemble.npz

# Optimize the cell volume and calculate effective FCs at 800 K
macer_phonopy sscha -p POSCAR -T 800 --optimize-volume

# Include 3rd order force constants in the fitting process
macer_phonopy sscha -p POSCAR -T 300 --include-third-order
```

### Defect Analysis Examples (`macer_pydefect`)

The `macer_pydefect` command automates the point defect calculation workflow, integrating `pydefect` and `vise` for analysis and `macer` for MLFF-based structure relaxation. It is verified to work with `pydefect` v0.9.11 and `vise` v0.9.5.

#### Chemical Potential Diagram (`macer_pydefect cpd`)
Generates the Chemical Potential Diagram (CPD) and determines the target chemical potential vertices.

```bash
# Generate CPD for a formula (retrieved from Materials Project)
macer_pydefect cpd -f MgAl2O4

# Generate CPD for a specific MPID with dopants
macer_pydefect cpd -m mp-1234 -d Ca Ti
```

#### Defect Formation Energy (`macer_pydefect defect`)
Calculates defect formation energies for a set of defects given the CPD info.

```bash
# Run defect calculations (requires standard_energies.yaml and target_vertices.yaml from CPD step)
macer_pydefect defect -p POSCAR -s standard_energies.yaml -t target_vertices.yaml --matrix 2 2 2
```

#### Full Workflow (`macer_pydefect full`)
Runs the entire pipeline: CPD generation -> Supercell generation -> Defect Calculation -> Analysis.

```bash
# Run full workflow for a POSCAR file
macer_pydefect full -p POSCAR --matrix 2 2 2 --min_atoms 100 --max_atoms 300

# Batch run for multiple POSCAR files using a glob pattern
macer_pydefect full -p POSCAR-mp-* --matrix 2 2 2 -d Cl
```

### Utility Suite (`macer_util`)

The `macer_util` command provides various post-processing and analysis tools, integrated into categories like `md`, `model`, and `struct`.

#### MD Post-processing (`macer_util md`)

```bash
# Calculate ionic conductivity
# Automatically detects MD interval from XDATCAR/md.csv and charges from pydefect
macer_util md conductivity -i ./md.traj -t 500 --dt 2

# Plot MD trajectory data (T, E, P from md.csv)
macer_util md plot -i md.csv

# Calculate and plot Radial Distribution Function (RDF)
macer_util md rdf -i md.traj

# Convert ASE .traj to VASP XDATCAR with a specific interval
macer_util md traj2xdatcar -i md.traj --interval 50

# Print statistical summary of MD results
macer_util md summary -i md.csv
```

#### Model & Structure Utilities (`macer_util model/struct`)

```bash
# Convert a model to float32 precision
macer_util model fp32 -i model.pth

# Convert VASP4 POSCAR to VASP5 (adds element symbols to the header)
macer_util struct vasp4to5 -i POSCAR
```

---

## Command Line Options

### `macer relax` Options

| Option | Description | Default |
|--------|-------------|---------|
| `-p`, `--poscar` | Input POSCAR file(s) or glob pattern(s). | `POSCAR` |
| `--model` | Path or name of the MLFF model. | (from `default.yaml`) |
| `--ff` | Force field to use. | (dynamic) |
| `--isif` | VASP ISIF mode (0–8) for relaxation. | 3 |
| `--no-pdf` | Do not generate the relaxation log PDF. | `False` |
| `--subdir` | Create a `RELAX-*` subdirectory for outputs. | `False` |
| `--fmax` | Force convergence threshold (eV/Å). | 0.01 |
| `--smax` | Stress convergence threshold (eV/Å³). | 0.001 |
| `--bulk-modulus` | Perform bulk modulus calculation instead of relaxation. | `False` |
| `--strain` | Max strain for E-V curve (e.g., 0.05 for ±5%). | `0.05` |
| `--eos` | Equation of state for bulk modulus (`birchmurnaghan` or `murnaghan`). | `birchmurnaghan` |

### `macer md` Options

| Option | Description | Default |
|--------|-------------|---------|
| `-p`, `--poscar` | Input POSCAR file. | `POSCAR` |
| `--ensemble` | MD ensemble: `npt`, `nte` (NVT), or `nve`. | `npt` |
| `--temp` | Target temperature [K]. | 300.0 |
| `--press` | Target pressure [GPa] (NPT only). | 0.0 |
| `--nsteps` | Number of MD steps. | 20000 |
| `--initial-relax` | Perform a full structural relaxation before the MD run. | `False` |

### `macer_phonopy` Options

#### `macer_phonopy pb` Options

| Option | Description | Default |
|--------|-------------|---------|
| `-p`, `--poscar` | Input POSCAR file(s). | Required |
| `-l`, `--length` | Minimum supercell lattice vector length in Å. | 20.0 |
| `--dim` | Set supercell dimension explicitly (e.g., `2 2 2`). Overrides `-l`. | None |
| `-pg`, `--plot-gruneisen` | Calculate and plot Grüneisen parameter. | False |
| `--strain` | Strain for Grüneisen calculation. If not set, estimated from bulk modulus. | None |
| `--irreps` | Calculate irreducible representations. | False |
| `--qpoint` | Q-point for irreps calculation (3 floats). | `0 0 0` |
| `--write-arrow` | Write VESTA and MCIF files for phonon mode visualization. | False |
| `--arrow-length` | Max arrow length in Å for VESTA visualization. | 1.7 |
| `--arrow-qpoint-gamma` | Generate arrows only for the Gamma point. | False |
| `--arrow-qpoint` | Generate arrows for a specific q-point vector (3 floats). | None |

#### `macer_phonopy qha` Options

| Option | Description | Default |
|---|---|---|
| `--dim` | Set supercell dimension explicitly (e.g., `2 2 2`). Overrides `--min-length`. | None |
| `--num-volumes` | Number of volume points to sample for the E-V curve. | 5 |
| `--length-scale` | Symmetric strain range for volume sampling (e.g., 0.05 for ±5%). Auto-estimated if not set. | None |
| `--length-factor-min/max` | Explicitly define the min/max length scaling factors for the volume range. | None |
| `--eos` | Equation of state for fitting (`vinet`, `birch_murnaghan`, `murnaghan`, `local_poly`). | `vinet` |
| `--tmax` | Maximum temperature for thermal property calculation. | 1300 K |

#### `macer_phonopy sscha` Options

The SSCHA workflow is divided into several stages, each with its own set of options.

| Group | Option | Description | Default |
|---|---|---|---|
| **General** | `-p`, `--poscar` | Input crystal structure file (e.g., POSCAR). | Required |
| | `--ff` | Force field to use. | (dynamic) |
| | `--model` | Path or name of the MLFF model. | (from `default.yaml`) |
| | `--device` | Compute device (`cpu`, `mps`, `cuda`). | `cpu` |
| | `--modal` | Modal for SevenNet model, if required. | None |
| | `--seed` | Random seed for reproducibility. | None |
| **Initial FC** | `--initial-fmax` | Force convergence for initial relaxation (eV/Å). | 5e-3 |
| | `--dim` | Supercell dimension (e.g., `2 2 2`). Overrides `--min-length`. | (auto) |
| | `-l`, `--min-length` | Minimum supercell length if `--dim` is not set (Å). | 15.0 |
| | `--amplitude` | Displacement amplitude for 0K FC calculation (Å). | 0.03 |
| | `--pm` | Use plus/minus displacements for initial FC generation. | False |
| | `--nodiag` | Do not use diagonal displacements for initial FC generation. | False |
| | `--symprec` | Symmetry tolerance for phonopy (Å). | 1e-5 |
| | `--read-initial-fc` | Path to `FORCE_CONSTANTS` to skip initial calculation. | None |
| | `--initial-symmetry-off` | Disable `FixSymmetry` in the initial structure relaxation. | False |
| **Ensemble** | `--reference-method` | Method to generate ensemble (`random`, `md`). | `md` |
| | `--reference-n-samples` | Number of samples for `random` method. | 200 |
| | `--reference-md-nsteps` | Number of sampling steps for `md` method. | 200 |
| | `--reference-md-nequil` | Number of equilibration steps for `md` method. | 100 |
| | `--reference-md-tstep` | MD timestep in fs. | 1.0 |
| | `--md-thermostat` | Thermostat for MD ensemble (`langevin`, `nve`). | `langevin` |
| | `--md-friction` | Friction for Langevin thermostat (ps⁻¹). | 0.01 |
| | `--reference-ensemble` | Path to an existing `reference_ensemble.npz` or `.txt` to use. | None |
| | `--no-save-reference-ensemble` | Do not save the generated `reference_ensemble` file. | False |
| | `--write-xdatcar` | Write an `XDATCAR` file from the MD trajectory. | False |
| | `--xdatcar-step` | Step interval for writing frames to `XDATCAR`. | 50 |
| **SSCHA** | `-T`, `--temperature` | Target temperature in Kelvin. | Required |
| | `--max-iter` | Maximum number of reweighting iterations per cycle. | 200 |
| | `--max-regen` | Maximum number of ensemble regenerations if ESS collapses. | 200 |
| | `--ess-collapse-ratio` | ESS/total ratio below which the ensemble is regenerated. | 0.5 |
| | `--free-energy-conv` | Free energy convergence threshold (meV/atom). | 0.1 |
| | `--fc-mixing-alpha` | Linear mixing parameter for FC updates (0 < α ≤ 1). | 0.5 |
| | `--mesh` | Q-point mesh for free energy calculation (e.g., `7 7 7`). | `7 7 7` |
| | `--include-third-order` | Enable simultaneous fitting of 3rd order force constants. | False |
| **Volume Optimization** | `--optimize-volume` | Enable self-consistent volume optimization by minimizing free energy. | False |
| | `--max-volume-iter` | Maximum iterations for volume optimization. | 10 |
| **Output** | `--output-dir` | Directory to save all output files. | `sscha_{poscar_stem}` |
| | `--save-every` | Save intermediate `FORCE_CONSTANTS` every N steps. | 5 |
| | `--no-plot-bands` | Disable plotting of band structures. | (Plotting is on) |
| | `--gamma-label` | Label for the Gamma point in plots. | `GM` |

### `macer_pydefect` Options

#### `macer_pydefect cpd` Options

| Option | Description | Default |
|---|---|---|
| `-f`, `--formula` | Chemical formula to retrieve from Materials Project (e.g., `MgAl2O4`). | None |
| `-m`, `--mpid` | Materials Project ID (e.g., `mp-3536`). | None |
| `-d`, `--doping` | List of dopant elements (e.g., `Ca Ti`). | None |
| `-p`, `--poscar` | Input POSCAR file(s) or glob pattern(s). | None |
| `--energy-shift-target` | Manually shift target energy in eV/atom (e.g., `0.05` to lower energy by 0.05 eV). | 0.0 |

#### `macer_pydefect defect` Options

| Option | Description | Default |
|---|---|---|
| `-p`, `--poscar` | Input unit cell POSCAR file(s) or glob pattern(s). | Required |
| `-d`, `--doping` | List of dopant elements (e.g., `Ca Ti`). | None |
| `-s`, `--std_energies` | Path to `standard_energies.yaml` from CPD step. | Required |
| `-t`, `--target_vertices` | Path to `target_vertices.yaml` from CPD step. | Required |
| `--matrix` | Supercell matrix (e.g., `2 2 2`). | None |
| `--min_atoms` | Minimum number of atoms for supercell. | 50 |
| `--max_atoms` | Maximum number of atoms for supercell. | 300 |
| `--no_symmetry_analysis` | Disable symmetry analysis (requires `sites_yaml`). | False |
| `--sites_yaml` | Path to `sites.yaml` file (if symmetry analysis is disabled). | None |

#### `macer_pydefect full` Options

| Option | Description | Default |
|---|---|---|
| `-p`, `--poscar` | Input unit cell POSCAR file(s) or glob pattern(s). | Required |
| `-d`, `--doping` | List of dopant elements (e.g., `Ca Ti`). | None |
| `--matrix` | Supercell matrix (e.g., `2 2 2`). | None |
| `--min_atoms` | Minimum number of atoms for supercell. | 50 |
| `--max_atoms` | Maximum number of atoms for supercell. | 300 |
| `--no_symmetry_analysis` | Disable symmetry analysis (requires `sites_yaml`). | False |
| `--sites_yaml` | Path to `sites.yaml` file (if symmetry analysis is disabled). | None |
| `--energy-shift-target` | Manually shift target energy in eV/atom. | 0.0 |

---

## Dependencies

### Core Dependencies
-   Python ≥ 3.8
-   ASE ≥ 3.20
-   matplotlib
-   numpy
-   pymatgen
-   monty
-   phonopy
-   seekpath

### Optional Dependencies (Install one per environment)
-   **MACE:** `mace-torch`, `e3nn==0.4.4`
-   **SevenNet:** `sevenn`, `e3nn>=0.5.0`
-   **CHGNet:** `chgnet`
-   **M3GNet:** `matgl`
-   **Allegro:** `nequip`
-   **MatterSim:** `mattersim`
-   **Orb:** `orb-models`
-   **FairChem:** `fairchem-core`, `huggingface_hub`

---

## Testing

To ensure the reliability of `macer` workflows, a comprehensive test suite is provided using `pytest`. The tests cover all major functionalities, including relaxation, molecular dynamics, lattice dynamics workflows (relax-unit, phonon-band, QHA, and SSCHA), and point defect workflows (cpd, defect, and full).

To run the tests:

1.  Install `pytest`:
    ```bash
    pip install pytest
    ```

2.  Run the tests from the project root:
    ```bash
    python -m pytest -v tests/
    ```

**Note:** The tests utilize a mocked calculator (ASE's EMT potential with an Aluminum structure) to validate workflow logic efficiently without requiring large MLFF model files or specific hardware (GPUs).

---
## Related packages
-   phonopy [https://github.com/phonopy/phonopy](https://github.com/phonopy/phonopy)
-   symfc [https://github.com/symfc/symfc](https://github.com/symfc/symfc)
-   pydefect [https://github.com/kumagai-group/pydefect](https://github.com/kumagai-group/pydefect)
-   SeeK-path [https://github.com/giovannipizzi/seekpath](https://github.com/giovannipizzi/seekpath)
---

## Standalone Scripts

The `scripts/` directory contains standalone versions of some key workflows, which can be run directly with `python`.

---

## MLFF Model Attribution

This project integrates various Machine-Learned Force Fields (MLFFs). For more information, please refer to the official repositories:
*   **MACE:** [https://github.com/ACEsuit/mace-foundations](https://github.com/ACEsuit/mace-foundations)
*   **SevenNet:** [https://github.com/MDIL-SNU/SevenNet](https://github.com/MDIL-SNU/SevenNet)
*   **CHGNet:** [https://github.com/CederGroupHub/chgnet](https://github.com/CederGroupHub/chgnet)
*   **M3GNet:** [https://github.com/materialsvirtuallab/m3gnet](https://github.com/materialsvirtuallab/m3gnet)
*   **Allegro:** [https://github.com/mir-group/nequip](https://github.com/mir-group/nequip)
*   **MatterSim:** [https://github.com/microsoft/mattersim](https://github.com/microsoft/mattersim)
*   **Orb:** [https://github.com/orbital-materials/orb-models](https://github.com/orbital-materials/orb-models)
*   **FairChem:** [https://github.com/facebookresearch/fairchem](https://github.com/facebookresearch/fairchem) (Models available at [Hugging Face](https://huggingface.co/facebook/UMA))


---

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.


---
 ## Contributors
- **Soungmin Bae** — [soungminbae@gmail.com](mailto:soungminbae@gmail.com), Tohoku University
- **Yasuhide Mochizuki** — [ahntaeyoung1212@gmail.com](mailto:ahntaeyoung1212@gmail.com), Institute of Science Tokyo
