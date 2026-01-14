_CHGNET_AVAILABLE = False
try:
    from chgnet.model import CHGNetCalculator
    _CHGNET_AVAILABLE = True
except Exception:
    pass

def get_chgnet_calculator(model_path=None, device="cpu", **kwargs):
    if not _CHGNET_AVAILABLE:
        raise RuntimeError("CHGNet is not installed. Please install with 'pip install .[chgnet]'")
    
    # From the PDF, CHGNetCalculator might take `use_device`
    # We will pass the device argument to it.
    return CHGNetCalculator(use_device=device)
