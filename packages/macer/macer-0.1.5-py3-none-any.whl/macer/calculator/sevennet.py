import os
from macer.defaults import DEFAULT_MODELS, _macer_root

_SEVENNET_AVAILABLE = False
try:
    from sevenn.calculator import SevenNetCalculator
    _SEVENNET_AVAILABLE = True
except Exception:
    pass

def get_sevennet_calculator(model_path: str, device: str = "cpu", modal: str = None):
    """Construct SevenNet calculator."""
    if not _SEVENNET_AVAILABLE:
        raise RuntimeError("SevenNet related libraries are not installed. Please install with 'pip install \"macer[sevennet]\"'")

    if model_path is None:
        # Use the default SevenNet model path from DEFAULT_MODELS
        default_sevennet_model_name = DEFAULT_MODELS.get("sevennet")
        if default_sevennet_model_name:
            model_path = os.path.join(_macer_root, "mlff-model", default_sevennet_model_name)
            print(f"No specific SevenNet model path provided; using default: {model_path}")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Default SevenNet model not found at {model_path}. Please provide a valid model path with --model or ensure the default model exists.")
        else:
            raise ValueError("No default SevenNet model specified in default-model.yaml and no model_path provided.")

    calc_args = {
        "model": model_path,
        "device": device,
    }
    if modal:
        calc_args["modal"] = modal

    return SevenNetCalculator(**calc_args)

