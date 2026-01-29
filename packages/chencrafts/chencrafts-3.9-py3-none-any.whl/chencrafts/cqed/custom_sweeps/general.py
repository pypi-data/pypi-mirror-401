__all__ = [
    'sweep_convergence',
    'sweep_hamiltonian',
]

import numpy as np
import qutip as qt
from scipy.sparse import csr_matrix
from scqubits.core.param_sweep import ParameterSweep

from typing import List, Tuple, Optional

# ##############################################################################
def sweep_convergence(
    paramsweep: ParameterSweep, paramindex_tuple, paramvals_tuple, mode_idx
):
    bare_evecs = paramsweep["bare_evecs"]["subsys": mode_idx][paramindex_tuple]
    return np.max(np.abs(bare_evecs[-3:, :]))

def sweep_hamiltonian(
    ps:ParameterSweep,
    paramindex_tuple, paramvals_tuple,
):
    bare_esys = {
        subsys_index: [
            ps["bare_evals"][subsys_index][paramindex_tuple],
            ps["bare_evecs"][subsys_index][paramindex_tuple],
        ]
        for subsys_index, _ in enumerate(ps.hilbertspace)
    }
    
    ham = ps.hilbertspace.hamiltonian(bare_esys=bare_esys)
    dims = ham.dims
    
    ham = qt.Qobj(csr_matrix(ham.full()), dims=dims)
    
    return ham
