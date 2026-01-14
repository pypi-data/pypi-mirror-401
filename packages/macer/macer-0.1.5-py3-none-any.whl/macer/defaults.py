
"""
Macer: Machine-learning accelerated Atomic Computational Environment for automated Research workflows
Copyright (c) 2025 The Macer Package Authors
Author: Soungmin Bae <soungminbae@gmail.com>
License: MIT
"""

import yaml
import os
from pathlib import Path

_current_dir = os.path.dirname(os.path.abspath(__file__))
_macer_root = os.path.join(_current_dir, "..")
_model_root = os.path.join(_current_dir, "mlff-model")
_default_yaml_path = Path(_current_dir) / "default.yaml"

DEFAULT_SETTINGS = {}
DEFAULT_MODELS = {}
DEFAULT_DEVICE = "cpu" # Default to CPU

if _default_yaml_path.exists():
    with open(_default_yaml_path, 'r') as f:
        config = yaml.safe_load(f)
        if config:
            DEFAULT_SETTINGS = config
            DEFAULT_MODELS = config.get("models", {}) # Assuming models are nested under 'models' key
            DEFAULT_DEVICE = config.get("device", "cpu") # Get device, default to "cpu"
else:
    print(f"Warning: default.yaml not found at {_default_yaml_path}. Default settings and models will not be loaded.")

# These are now dynamically loaded from DEFAULT_MODELS
# DEFAULT_MACE_MODEL_PATH = os.path.join(
#     _macer_root, "mlff-model", "mace-omat-0-small-fp32.model"
# )
# DEFAULT_SEVENNET_MODEL_PATH = os.path.join(
#     _macer_root, "mlff-model", "checkpoint_sevennet_0.pth"
# )
# DEFAULT_ALLEGRO_MODEL_PATH = os.path.join(
#     _macer_root, "mlff-model", "Allegro-OAM-L-0.1.ase.nequip.pth"
# )

