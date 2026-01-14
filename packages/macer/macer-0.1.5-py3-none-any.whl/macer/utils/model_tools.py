import torch
import os
from pathlib import Path

def convert_model_precision(input_path: str, output_path: str = None):
    """
    Converts a MACE/MLFF model from float64 to float32 precision.
    """
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        return

    if output_path is None:
        p = Path(input_path)
        output_path = f"{p.stem}-fp32{p.suffix}"

    print(f"Loading model from '{input_path}'...")
    try:
        # Load the model on the CPU
        model_fp64 = torch.load(input_path, map_location=torch.device('cpu'), weights_only=False)

        print("Converting model to float32 precision...")
        model_fp32 = model_fp64.to(dtype=torch.float32)

        print(f"Saving converted model to '{output_path}'...")
        torch.save(model_fp32, output_path)
        print("Conversion complete!")
    except Exception as e:
        print(f"Error during model conversion: {e}")

def list_models():
    """
    List available models in the mlff-model directory.
    """
    from macer.defaults import _macer_root
    model_dir = Path(_macer_root) / "mlff-model"
    
    if not model_dir.exists():
        print(f"Error: Model directory '{model_dir}' not found.")
        return

    print(f"\nAvailable models in {model_dir}:")
    print("-" * 50)
    models = sorted(list(model_dir.glob("*.pth")) + list(model_dir.glob("*.model")))
    if not models:
        print("  (No models found)")
    else:
        for m in models:
            size_mb = m.stat().st_size / (1024 * 1024)
            print(f"  - {m.name:<40} ({size_mb:>6.1f} MB)")
    print("-" * 50)

