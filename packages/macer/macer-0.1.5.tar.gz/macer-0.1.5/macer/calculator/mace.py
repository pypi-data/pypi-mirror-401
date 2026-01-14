import os
from pathlib import Path

_MACE_AVAILABLE = False
try:
    from mace.calculators import MACECalculator, mace_mp
    _MACE_AVAILABLE = True
except Exception:
    pass

from macer.defaults import DEFAULT_MODELS, _macer_root

def get_mace_calculator(model_paths, device="cpu", **kwargs):
    """Construct MACE calculator (use float32 for MPS compatibility)."""
    if not _MACE_AVAILABLE:
        raise RuntimeError("MACE related libraries are not installed. Please install with 'pip install \"macer[mace]\"'")

    dtype = "float32" if device == "mps" else "float64"

    # Determine the default MACE model path from DEFAULT_MODELS
    default_mace_model_name = DEFAULT_MODELS.get("mace")
    default_mace_model_path = os.path.join(_macer_root, "mlff-model", default_mace_model_name) if default_mace_model_name else None

    # If no model path is explicitly provided via --model argument (model_paths is [None])
    if not model_paths or (len(model_paths) == 1 and model_paths[0] is None):
        if default_mace_model_name:
            # Use the model specified in default-model.yaml
            print(f"No specific MACE model path provided; using default from default-model.yaml: {default_mace_model_name}.")
            actual_model_paths = [default_mace_model_path]
        else:
            # Fallback to mace_mp "small" if no default is specified in default-model.yaml
            print("No specific MACE model path provided and no default in default-model.yaml; using `mace_mp` 'small' model.")
            return mace_mp(
                model="small",
                device=device,
                default_dtype=dtype
            )
    else:
        # If a specific model path is provided via --model argument
        actual_model_paths = [p for p in model_paths if p is not None]
        if not actual_model_paths:
            raise ValueError("No valid MACE model path provided.")

    return MACECalculator(
        model_paths=actual_model_paths,
        device=device,
        default_dtype=dtype,
    )
