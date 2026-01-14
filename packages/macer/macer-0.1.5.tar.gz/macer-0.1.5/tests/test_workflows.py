import os
import pytest
import subprocess
import shutil
from pathlib import Path
from ase.io import read
from macer.cli.main import main as macer_main
from macer.cli.phonopy_main import main as macer_phonopy_main
from macer.cli.pydefect_main import main as macer_pydefect_main
from unittest.mock import patch, MagicMock
import sys

# Helper to simulate CLI arguments
def run_cli_command(main_func, args):
    with patch.object(sys, 'argv', args):
        try:
            main_func()
        except SystemExit as e:
            # argparse exits with 0 on success (help) or error code on failure
            if e.code != 0:
                raise RuntimeError(f"Command failed with exit code {e.code}")

def test_macer_relax(clean_dir):
    """Test 'macer relax' workflow."""
    print("\nRunning test_macer_relax...")
    
    # Run relaxation with very loose convergence for speed
    # Mocking --ff mace (will use EMT via conftest)
    args = ["macer", "relax", "-p", "POSCAR", "--ff", "mace", "--fmax", "10.0", "--max-step", "2"]

    run_cli_command(macer_main, args)

    assert Path("CONTCAR-POSCAR").exists()
    assert Path("OUTCAR-POSCAR").exists()
    assert Path("vasprun-POSCAR.xml").exists()
    
    atoms = read("CONTCAR-POSCAR")
    assert len(atoms) == 8  # Si 8 atoms

def test_macer_md(clean_dir):
    """Test 'macer md' workflow."""
    print("\nRunning test_macer_md...")
    
    # Run extremely short MD
    args = ["macer", "md", "-p", "POSCAR", "--ff", "mace", "--ensemble", "nvt", "--temp", "300", "--nsteps", "5", "--save-every", "1"]
    # Argument adjustment: --ensemble choice in CLI is 'nte' for NVT
    args = ["macer", "md", "-p", "POSCAR", "--ff", "mace", "--ensemble", "nte", "--temp", "300", "--nsteps", "5", "--save-every", "1"]

    run_cli_command(macer_main, args)

    assert Path("md.log").exists()
    assert Path("md.traj").exists()
    assert Path("XDATCAR").exists()
    assert Path("md.csv").exists()

def test_macer_phonopy_sr(clean_dir):
    """Test 'macer_phonopy sr' (symmetry-refine) workflow."""
    print("\nRunning test_macer_phonopy_sr...")
    
    # Use 1 iteration max
    args = ["macer_phonopy", "sr", "-p", "POSCAR", "--ff", "mace", "--max-iterations", "1", "--output-prefix", "test_ru"]
    
    run_cli_command(macer_phonopy_main, args)
    
    assert Path("test_ru-symmetrized").exists()

def test_macer_phonopy_pb(clean_dir):
    """Test 'macer_phonopy pb' (phonon-band) workflow."""
    print("\nRunning test_macer_phonopy_pb...")
    
    # Small dim, minimal length
    # Use --initial-isif 0 to skip initial relaxation which would fail due to subprocess not being mocked
    args = ["macer_phonopy", "pb", "-p", "POSCAR", "--ff", "mace", "--dim", "1", "1", "1", "--initial-isif", "0"]
    
    run_cli_command(macer_phonopy_main, args)

    assert Path("phonopy_disp-POSCAR.yaml").exists()
    assert Path("FORCE_SETS_POSCAR").exists()
    assert Path("band-POSCAR.conf").exists()
    assert Path("band-POSCAR.pdf").exists()

def test_macer_phonopy_qha(clean_dir):
    """Test 'macer_phonopy qha' workflow."""
    print("\nRunning test_macer_phonopy_qha...")
    
    # Minimized qha run
    # num-volumes 4 is minimum required by our code check
    # Use --eos local_poly for robustness in testing
    args = [
        "macer_phonopy", "qha", "-p", "POSCAR", "--ff", "mace",
        "--dim", "1", "1", "1",
        "--num-volumes", "4",
        "--length-scale", "0.01", # Small strain
        "--mesh", "1", "1", "1",
        "--isif", "0", # Skip initial relax for speed
        "--eos", "local_poly"
    ]
    
    run_cli_command(macer_phonopy_main, args)    
    # Output dir is usually qha_{stem}
    out_dir = Path("qha_POSCAR")
    assert out_dir.exists()
    assert (out_dir / "e-v.dat").exists()
    assert (out_dir / "thermal_expansion.pdf").exists()

def test_macer_phonopy_sscha(clean_dir):
    """Test 'macer_phonopy sscha' workflow."""
    print("\nRunning test_macer_phonopy_sscha...")
    
    # Highly reduced SSCHA run
    args = [
        "macer_phonopy", "sscha", "-p", "POSCAR", "--ff", "mace",
        "-T", "300",
        "--dim", "1", "1", "1",
        "--reference-method", "random",
        "--reference-n-samples", "2", # Minimum samples
        "--max-iter", "1", # 1 iteration
        "--max-regen", "0",
        "--mesh", "1", "1", "1",
        "--no-plot-bands"
    ]
    
    run_cli_command(macer_phonopy_main, args)
    
    # Output dir is usually sscha_{stem}
    out_dir = Path("sscha_POSCAR")
    assert out_dir.exists()
    assert (out_dir / "sscha_convergence.log").exists()
    assert (out_dir / "FORCE_CONSTANTS_SSCHA_final").exists()

def test_macer_pydefect_cpd(clean_dir):
    """Test 'macer_pydefect cpd' workflow."""
    print("\nRunning test_macer_pydefect_cpd...")
    
    # Use ZnO for CPD test
    from tests.conftest import POSCAR_ZNO
    if POSCAR_ZNO.exists():
        shutil.copy(POSCAR_ZNO, "POSCAR")
    
    poscar_content = Path("POSCAR").read_text()
    
    # Mocking external pydefect/vise functions
    # Patch run_macer_relax to avoid running actual MLFF relaxation
    with patch("macer.pydefect.cpd.get_poscar_from_mp") as mock_gp, \
         patch("macer.pydefect.cpd.make_competing_phase_dirs") as mock_mpd, \
         patch("macer.pydefect.cpd.make_composition_energies") as mock_mce, \
         patch("macer.pydefect.cpd.make_standard_and_relative_energies") as mock_msre, \
         patch("macer.pydefect.cpd.make_cpd_and_vertices") as mock_mcv, \
         patch("macer.pydefect.cpd.run_macer_relax") as mock_relax:

        # Setup side effects
        def gp_se(args):
            Path("POSCAR").write_text(poscar_content)
            Path("prior_info.yaml").write_text("band_gap: 3.3\n")
        mock_gp.side_effect = gp_se
        
        def mpd_se(args):
            d = Path("Zn_competing")
            d.mkdir()
            (d / "POSCAR").write_text(poscar_content)
            (d / "prior_info.yaml").write_text("band_gap: 0.0\n")
        mock_mpd.side_effect = mpd_se
        
        mock_relax.return_value = [Path("Zn_competing")]
        
        # Write valid YAML content to avoid NoneType errors in safe_load
        mock_mce.side_effect = lambda x: Path("composition_energies.yaml").write_text("Zn1O1: {energy: -5.0}")
        mock_msre.side_effect = lambda x: Path("relative_energies.yaml").write_text("Zn1O1: -2.5")
        mock_mcv.side_effect = lambda x: Path("chem_pot_diag.json").touch()
        
        args = ["macer_pydefect", "cpd", "-f", "ZnO"]
        
        run_cli_command(macer_pydefect_main, args)
        
        # Verify directory structure
        current_dir_name = Path.cwd().name
        assert current_dir_name.startswith("CPD-target=ZnO")
        
        cpd_dir = Path.cwd()
        assert (cpd_dir / "composition_energies.yaml").exists()
        assert (cpd_dir / "relative_energies.yaml").exists()
        assert (cpd_dir / "chem_pot_diag.json").exists()

def test_macer_pydefect_defect(clean_dir):
    """Test 'macer_pydefect defect' workflow."""
    print("\nRunning test_macer_pydefect_defect...")
    
    # Use ZnO for Defect test
    from tests.conftest import POSCAR_ZNO
    if POSCAR_ZNO.exists():
        shutil.copy(POSCAR_ZNO, "POSCAR")

    poscar_content = Path("POSCAR").read_text()
    Path("standard_energies.yaml").touch()
    Path("target_vertices.yaml").touch()
    
    with patch("macer.pydefect.defect.make_supercell") as mock_sc, \
         patch("macer.pydefect.defect.DefectSetMaker") as mock_dsm, \
         patch("macer.pydefect.defect.make_defect_entries") as mock_mde, \
         patch("macer.pydefect.defect.make_calc_results") as mock_mcr, \
         patch("macer.pydefect.defect.make_defect_energy_infos_main_func") as mock_mdei, \
         patch("macer.pydefect.defect.make_defect_energy_summary_main_func") as mock_mdes, \
         patch("macer.pydefect.defect.write_summary_at_vertices") as mock_wsav, \
         patch("macer.pydefect.defect.Unitcell") as mock_unitcell, \
         patch("macer.pydefect.defect.StandardEnergies") as mock_std_energies, \
         patch("macer.pydefect.defect.run_macer_relax") as mock_relax:
         
         mock_relax.return_value = [Path("Va_O1_0")]

         # Write valid JSON to avoid JSONDecodeError
         mock_sc.side_effect = lambda x: Path("supercell_info.json").write_text("{}")
         
         mock_dsm_instance = MagicMock()
         defect_stub = MagicMock()
         defect_stub.name = "Va_O1"
         mock_dsm_instance.defect_set = [defect_stub]
         mock_dsm.return_value = mock_dsm_instance
         
         def mde_se(args):
             d = Path("Va_O1_0")
             d.mkdir()
             (d / "POSCAR").write_text(poscar_content)
             (d / "defect_entry.json").write_text("{}")
             
             dp = Path("perfect")
             dp.mkdir()
             (dp / "POSCAR").write_text(poscar_content)
             (dp / "calc_results.json").write_text("{}")
         mock_mde.side_effect = mde_se
         
         # Unitcell must return an object with composition.reduced_formula
         mock_uc = MagicMock()
         mock_uc.composition.reduced_formula = "Zn1O1"
         mock_unitcell.from_yaml.return_value = mock_uc
         
         args = ["macer_pydefect", "defect", "-p", "POSCAR", "-s", "standard_energies.yaml", "-t", "target_vertices.yaml"]
         
         run_cli_command(macer_pydefect_main, args)
         
         # We check if key functions were called
         mock_sc.assert_called()
         mock_relax.assert_called()
         mock_mdes.assert_called()

def test_macer_pydefect_full(clean_dir):
    """Test 'macer_pydefect full' workflow."""
    print("\nRunning test_macer_pydefect_full...")
    
    # Use ZnO for Full test
    from tests.conftest import POSCAR_ZNO
    if POSCAR_ZNO.exists():
        shutil.copy(POSCAR_ZNO, "POSCAR")

    poscar_content = Path("POSCAR").read_text()
    
    # Mock everything from both CPD and Defect workflows
    with patch("macer.pydefect.full.make_competing_phase_dirs") as mock_mpd, \
         patch("macer.pydefect.full.make_composition_energies") as mock_mce, \
         patch("macer.pydefect.full.make_standard_and_relative_energies") as mock_msre, \
         patch("macer.pydefect.full.make_cpd_and_vertices") as mock_mcv, \
         patch("macer.pydefect.full.make_supercell") as mock_sc, \
         patch("macer.pydefect.full.DefectSetMaker") as mock_dsm, \
         patch("macer.pydefect.full.make_defect_entries") as mock_mde, \
         patch("macer.pydefect.full.make_calc_results") as mock_mcr, \
         patch("macer.pydefect.full.make_defect_energy_infos_main_func") as mock_mdei, \
         patch("macer.pydefect.full.make_defect_energy_summary_main_func") as mock_mdes, \
         patch("macer.pydefect.full.write_summary_at_vertices") as mock_wsav, \
         patch("macer.pydefect.full.Unitcell") as mock_unitcell, \
         patch("macer.pydefect.full.StandardEnergies") as mock_std_energies, \
         patch("macer.pydefect.full.run_macer_relax") as mock_relax:

        # Mock relax return
        mock_relax.return_value = [Path("Zn_host"), Path("Va_O1_0")]

        # CPD mocks
        def mpd_se(args):
            d = Path("Zn_host")
            d.mkdir()
            (d / "POSCAR").write_text(poscar_content)
            (d / "prior_info.yaml").write_text("band_gap: 0.0\n")
        mock_mpd.side_effect = mpd_se
        mock_mce.side_effect = lambda x: Path("composition_energies.yaml").write_text("ZnO: {energy: -5.0}")
        mock_msre.side_effect = lambda x: Path("relative_energies.yaml").write_text("ZnO: -2.5")
        
        # Defect mocks
        # Write valid JSON to avoid JSONDecodeError
        mock_sc.side_effect = lambda x: Path("supercell_info.json").write_text("{}")
        
        mock_dsm_instance = MagicMock()
        defect_stub = MagicMock()
        defect_stub.name = "Va_O1"
        mock_dsm_instance.defect_set = [defect_stub]
        mock_dsm.return_value = mock_dsm_instance
        
        def mde_se(args):
            d = Path("Va_O1_0")
            d.mkdir()
            (d / "POSCAR").write_text(poscar_content)
            (d / "defect_entry.json").write_text("{}")
            
            dp = Path("perfect")
            dp.mkdir()
            (dp / "POSCAR").write_text(poscar_content)
            (dp / "calc_results.json").write_text("{}") 
        mock_mde.side_effect = mde_se
        
        mock_mdes.side_effect = lambda x: Path("defect_energy_summary.json").touch()
        
        # Mock Unitcell and StandardEnergies for analysis steps
        mock_uc = MagicMock()
        mock_uc.composition.reduced_formula = "ZnO" 
        mock_unitcell.from_yaml.return_value = mock_uc
        
        mock_std_energies_obj = MagicMock()
        mock_std_energies.from_yaml.return_value = mock_std_energies_obj 

        args = ["macer_pydefect", "full", "-p", "POSCAR"]
        
        run_cli_command(macer_pydefect_main, args)
        
        # Verify structure
        # The workflow ends inside the 'defect' directory
        if Path.cwd().name == "defect":
            work_dir = Path.cwd().parent
        else:
            work_dir = Path.cwd()
            
        current_dir_name = work_dir.name
        assert current_dir_name.startswith("DEFECT-POSCAR-formula=ZnO")
        
        # Verify CPD outputs
        assert (work_dir / "cpd" / "composition_energies.yaml").exists()
        assert (work_dir / "cpd" / "relative_energies.yaml").exists()

        # Verify defect outputs
        assert (work_dir / "defect" / "Va_O1_0" / "defect_entry.json").exists()
        assert (work_dir / "defect" / "defect_energy_summary.json").exists()

        