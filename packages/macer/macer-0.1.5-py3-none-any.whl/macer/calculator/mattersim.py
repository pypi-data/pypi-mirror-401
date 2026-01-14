import os
import sys
from macer.defaults import DEFAULT_MODELS, _macer_root

try:
    from mattersim.forcefield import MatterSimCalculator
    _MATTERSIM_AVAILABLE = True
except Exception:
    _MATTERSIM_AVAILABLE = False
    MatterSimCalculator = None  # Define as None if import fails

def get_mattersim_calculator(model_path, device="cpu", **kwargs):
    if not _MATTERSIM_AVAILABLE:
        raise RuntimeError("MatterSim is not installed. Please install with 'pip install .[mattersim]'")

    if model_path is None:
        default_mattersim_model_name = DEFAULT_MODELS.get("mattersim")
        if default_mattersim_model_name:
            model_path = os.path.join(_macer_root, "mlff-model", default_mattersim_model_name)
            print(f"No specific MatterSim model path provided; using default: {model_path}")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Default MatterSim model not found at {model_path}. Please provide a valid model path with --model or ensure the default model exists.")
        else:
            raise ValueError("A model path (load_path) is required for MatterSim. No default model found in default-model.yaml.")

    # MatterSimCalculator takes device and load_path arguments.
    return MatterSimCalculator(device=device, load_path=model_path)
