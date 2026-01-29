__all__ = [
    'wavefunc_FT',
    'sweep_data_to_hilbertspace',
    'standardize_evec_phase',
]

import numpy as np
import cmath
from scipy.fft import fft, fftfreq

from scqubits.utils.spectrum_utils import extract_phase
try: 
    from scqubits.utils.spectrum_utils import sweep_data_to_hilbertspace
except ImportError:
    sweep_data_to_hilbertspace = None
from scqubits.core.param_sweep import SpectrumLookupMixin

from typing import List, Tuple, Optional, Literal

def wavefunc_FT(
    x_list: List | np.ndarray, 
    amp_x: List | np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    x_list = np.array(x_list)
    amp_x = np.array(amp_x)

    x0, x1 = x_list[0], x_list[-1]
    dx = x_list[1] - x_list[0]

    amp_p_dft = fft(amp_x)
    n_list = fftfreq(amp_x.size) * 2 * np.pi / dx

    # In order to get a discretisation of the continuous Fourier transform
    # we need to multiply amp_p_dft by a phase factor
    amp_p = amp_p_dft * dx * np.exp(-1j * n_list * x0) / (np.sqrt(2*np.pi))

    return n_list, amp_p

def standardize_evec_phase(
    ps: SpectrumLookupMixin,
    idx = 0,
    state_labels: Optional[List[Tuple[int, ...]]] = None,
    zero_phase_component: Literal["max", "bare"] = "bare",
):
    """
    Standardize the sign of eigenvectors. 
    
    Parameters
    ----------
    ps : scqubits.ParameterSweep
        The parameter sweep object.
    idx : int
        The index of the parameter set to sweep.
    state_labels : List[Tuple[int, ...]]
        The bare labels of the states to be standardized. It is assumed 
        that the dressed states are very close to the bare states.
        
    Returns
    -------
    evecs_std : np.ndarray
        The standardized eigenvectors.
    """
    evecs = ps["evecs"][idx].copy()
    drs_indices = ps["dressed_indices"][idx]
    dims = tuple(ps.hilbertspace.subsystem_dims)
    
    if state_labels is None:
        drs_labels = list(range(np.prod(dims)))
        unravelled_bare_labels = [
            np.where(drs_indices == lbl)[0][0]
            for lbl in drs_labels
        ]
    elif hasattr(state_labels[0], '__iter__'):
        # bare labels with multiple subsystems
        unravelled_bare_labels = [
            np.unravel_index(lbl, dims)
            for lbl in state_labels
        ]
        drs_labels = [
            drs_indices[lbl]
            for lbl in unravelled_bare_labels
        ]
    else:
        drs_labels = state_labels
        unravelled_bare_labels = state_labels
    
    
    for bare_label, drs_label in zip(unravelled_bare_labels, drs_labels):
        
        evec_to_standardize = evecs[drs_label]
        evec_arr = evec_to_standardize.full()
        
        # extract the phase of the "principal" state component
        if zero_phase_component == "max":
            phase = extract_phase(evec_arr)
        elif zero_phase_component == "bare":
            principal_component = evec_arr[bare_label, 0]
            phase = cmath.phase(principal_component)
        else:
            raise ValueError(f"Invalid value for zero_phase_component: {zero_phase_component}")
        
        # standardize the phase
        evecs[drs_label] = evec_to_standardize * np.exp(-1j * phase)
        
    return evecs
