from chencrafts.version import version as __version__

# import submodules
# when changed, remember to change setup.py
import chencrafts.bsqubits as bsq
import chencrafts.cqed as cqed
import chencrafts.fluxonium as fx
import chencrafts.projects as prj
import chencrafts.toolbox as tb
import chencrafts.settings as settings
from chencrafts.version import __version__, __version_tuple__

# set figure format in jupyter notebook
try:
    get_ipython()
    import matplotlib_inline.backend_inline as _backend_inline
    _backend_inline.set_matplotlib_formats("png")
except NameError:
    pass

# set matplotlib 
import matplotlib as _mpl
import matplotlib.font_manager as _mpl_font
from chencrafts.toolbox.plot import color_cyclers as _color_cyclers
_mpl.rcParams = _mpl.rcParamsDefault.copy()

# color cycle
_mpl.rcParams["axes.prop_cycle"] = _color_cyclers["PGL"]
_mpl.rcParams['text.usetex'] = False

# disable font warning message
font_selected = None
try:
    font_names = _mpl_font.get_font_names()
    for font in ["IBM Plex Sans", "Roboto", "Arial", "Helvetica"]:
        if font in font_names:
            font_selected = font
            break
    if not font_selected:
        font_selected = "sans-serif"
except AttributeError:
    font_selected = "sans-serif"
_mpl.rcParams["font.family"] = font_selected

# set numpy print options
import numpy as _np
_print_options = {
    "precision": 6,
    "linewidth": 130,
}
if _np.__version__ >= "2":
    _print_options["legacy"] = "1.25"
_np.set_printoptions(**_print_options)

# scqubits settings
import scqubits as scq
scq.set_units('GHz')
scq.settings.T1_DEFAULT_WARNING = False
scq.settings.PROGRESSBAR_DISABLED = True
scq.settings.FUZZY_SLICING = True
scq.settings.OVERLAP_THRESHOLD = 0.853

# reload all modules
def reload_all(module_name="chencrafts"):
    """Dynamically reload all modules under the given module name."""
    import sys
    import importlib
    # Get all loaded chencrafts modules
    modules = [m for m in sys.modules if m.startswith(module_name + '.')]
    # Sort by dependency (deeper modules first)
    modules.sort(key=lambda m: m.count('.'), reverse=True)
    # Reload each module
    for module in modules:
        if module_name in sys.modules:
            importlib.reload(sys.modules[module])
    print(f"Reloaded {len(modules)} modules!")

# public modules
__all__ = [
    "bsq", "cqed", "prj", "sf", "tb", "fx",
    "settings",
    "__version__", "__version_tuple__"
]