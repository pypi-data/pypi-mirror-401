_ORB_AVAILABLE = False
try:
    from orb_models.forcefield import pretrained
    from orb_models.forcefield.calculator import ORBCalculator
    _ORB_AVAILABLE = True
except Exception:
    pass

def get_orb_calculator(model_path="orb-v2", device="cpu", **kwargs):
    """
    Constructs ORB calculator from a pretrained model name.
    The model_path corresponds to a function name in orb_models.forcefield.pretrained.
    """
    if not _ORB_AVAILABLE:
        raise RuntimeError("orb-models is not installed. Please install with 'pip install .[orb]'")

    if hasattr(pretrained, model_path):
        # Get the function from the pretrained module, e.g., pretrained.orb_v2
        model_func = getattr(pretrained, model_path)
        print(f"Loading ORB pretrained model: {model_path}")
        # Call the function to get the force field object
        orbff = model_func(device=device)
    else:
        available_models = [name for name in dir(pretrained) if not name.startswith('_') and callable(getattr(pretrained, name))]
        raise ValueError(f"Unsupported ORB model: '{model_path}'.\nAvailable models in orb_models.forcefield.pretrained are: {available_models}")

    return ORBCalculator(orbff, device=device)