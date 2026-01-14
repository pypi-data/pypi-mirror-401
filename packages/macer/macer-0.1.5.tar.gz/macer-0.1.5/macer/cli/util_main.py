
import argparse
import sys
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

def main():
    parser = argparse.ArgumentParser(
        description=MACER_LOGO + f"\nmacer_util (v{__version__}): Utility suite for post-processing and model management.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--version", "-v", action="version", version=f"macer_util {__version__}")

    subparsers = parser.add_subparsers(dest="category", help="Utility categories")

    # --- MD Category ---
    md_parser = subparsers.add_parser("md", help="MD post-processing utilities")
    md_subparsers = md_parser.add_subparsers(dest="action", help="MD actions")

    # md traj2xdatcar
    t2x_parser = md_subparsers.add_parser("traj2xdatcar", help="Convert md.traj to VASP XDATCAR")
    t2x_parser.add_argument("-i", "--input", required=True, help="Input .traj file")
    t2x_parser.add_argument("-o", "--output", default="XDATCAR", help="Output XDATCAR file (default: XDATCAR)")
    t2x_parser.add_argument("--interval", type=int, default=1, help="Sampling interval used during MD (e.g. 100).")

    # md summary
    summary_parser = md_subparsers.add_parser("summary", help="Print statistical summary of md.csv")
    summary_parser.add_argument("-i", "--input", default="md.csv", help="Input md.csv file (default: md.csv)")

    # md conductivity
    cond_parser = md_subparsers.add_parser("conductivity", help="Calculate ionic conductivity")
    cond_parser.add_argument("-i", "--input", required=True, help="Input trajectory (md.traj or XDATCAR)")
    cond_parser.add_argument("-t", "--temp", type=float, required=True, help="Temperature (K)")
    cond_parser.add_argument("--dt", type=float, default=2.0, help="Timestep (fs)")
    cond_parser.add_argument("--interval", type=int, default=1, help="Sampling interval used during MD (e.g. 50).")
    cond_parser.add_argument("--charges", help="Oxidation states (e.g. \"Li:1,S:-2\")")

    # md plot
    pmd_parser = md_subparsers.add_parser("plot", help="Plot MD trajectory data (T, E, P)")
    pmd_parser.add_argument("-i", "--input", default="md.csv", help="Input md.csv")
    pmd_parser.add_argument("-o", "--output", default="md_plot", help="Output PDF prefix")

    # md rdf
    rdf_parser = md_subparsers.add_parser("rdf", help="Plot Radial Distribution Function (RDF)")
    rdf_parser.add_argument("-i", "--input", required=True, help="Input trajectory (md.traj or XDATCAR)")
    rdf_parser.add_argument("-o", "--output", default="rdf_plot", help="Output PDF prefix")
    rdf_parser.add_argument("--rmax", type=float, default=10.0, help="Maximum radius (Å)")
    rdf_parser.add_argument("--bins", type=int, default=200, help="Number of bins")

    # --- Model Category ---
    model_parser = subparsers.add_parser("model", help="Model management utilities")
    model_subparsers = model_parser.add_subparsers(dest="action", help="Model actions")

    # model fp32
    fp32_parser = model_subparsers.add_parser("fp32", help="Convert model to float32 precision")
    fp32_parser.add_argument("-i", "--input", required=True, help="Input model file (.pth or .model)")
    fp32_parser.add_argument("-o", "--output", help="Output model file (optional)")

    # model list
    model_subparsers.add_parser("list", help="List available models in mlff-model/")

    # --- Struct Category ---
    struct_parser = subparsers.add_parser("struct", help="Structure file utilities")
    struct_subparsers = struct_parser.add_subparsers(dest="action", help="Structure actions")

    # struct vasp4to5
    v4to5_parser = struct_subparsers.add_parser("vasp4to5", help="Convert VASP4 POSCAR to VASP5 (add symbols)")
    v4to5_parser.add_argument("-i", "--input", required=True, help="Input VASP4 POSCAR file")
    v4to5_parser.add_argument("-s", "--symbols", help="Element symbols (e.g. \"Li S\"). If omitted, guesses from 1st line.")
    v4to5_parser.add_argument("-o", "--output", help="Output VASP5 POSCAR file (optional)")

    # --- Execute ---
    args = parser.parse_args()

    if args.category == "md":
        from macer.utils.md_tools import traj2xdatcar, md_summary, calculate_conductivity
        from macer.utils.viz_tools import plot_md_log, plot_rdf
        if args.action == "traj2xdatcar":
            traj2xdatcar(args.input, args.output, interval=args.interval)
        elif args.action == "summary":
            md_summary(args.input)
        elif args.action == "conductivity":
            calculate_conductivity(args.input, args.temp, args.dt, interval=args.interval, charges_str=args.charges)
        elif args.action == "plot":
            plot_md_log(args.input, args.output)
        elif args.action == "rdf":
            plot_rdf(args.input, args.output, r_max=args.rmax, n_bins=args.bins)
        else:
            md_parser.print_help()

    elif args.category == "model":
        from macer.utils.model_tools import convert_model_precision, list_models
        if args.action == "fp32":
            convert_model_precision(args.input, args.output)
        elif args.action == "list":
            list_models()
        else:
            model_parser.print_help()

    elif args.category == "struct":
        from macer.utils.struct_tools import vasp4to5
        if args.action == "vasp4to5":
            vasp4to5(args.input, args.symbols, args.output)
        else:
            struct_parser.print_help()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
