__all__ = [
    "batched_sweep_readout",
    "batched_sweep_simplemodel",
]

import time
import numpy as np
import scqubits as scq
import jax.numpy as jnp
import dynamiqs as dq
import qutip as qt
from jax import Array as jax_Array, jit, grad, value_and_grad, hessian
from functools import partial
from typing import Literal, Callable, Tuple
from tqdm.notebook import tqdm
from dynamiqs.method import Tsit5
from chencrafts.cqed.scq_helper import standardize_evec_phase as standardize_evec_phase_func
from chencrafts.cqed.qt_helper import superop_evolve
from chencrafts.projects.reduce_readout_model import simplemodel
from scqubits.utils.cpu_switch import get_map_method
from chencrafts.toolbox.data_processing import order_matelems

from chencrafts.cqed import (
    MEConstructor, cap_spectral_density, ohmic_spectral_density, delta_spectral_density,
    steadystate_floquet_full_dq, steadystate_dq, organize_by_bare_index,
    oprt_in_basis, trans_by_kets, flat_spectral_density, inv_spectral_density,
    ind_spectral_density,
)

# Ingredients ====================================================

def sweep_constructor(
    ps: scq.ParameterSweep,
    idx,
    truncated_dim,
    use_flat_Qcap = False,
    dephasing_spec_dens: Literal["delta", "flat", "inv"] | Callable = "delta",
):
    param_mesh = ps.parameters.meshgrids_by_paramname()
    hspace = ps.hilbertspace
    flxn, osc = hspace.subsystem_list
    
    # initialize the MEConstructor
    constructor = MEConstructor(
        hilbertspace = hspace,
        truncated_dim = truncated_dim,
        regenerate_lookup=False, 
    )

    # add the qubit capacitive noise channel
    if use_flat_Qcap:
        from chencrafts.cqed.clustered_me import (
            thermal_factor, 
            T1_LO_FREQ_CUTOFF,
        )
        def _cap_spec_dens_fun(omega, T, EC, Q_cap):
            omega = np.where(np.abs(omega) < T1_LO_FREQ_CUTOFF, T1_LO_FREQ_CUTOFF, omega)
            
            therm_factor = thermal_factor(omega, T)
            s = (
                2
                * 8
                * EC
                / Q_cap
                * therm_factor
            )
            s *= (
                2 * np.pi
            )  # We assume that system energies are given in units of frequency
            return s
    else:
        _cap_spec_dens_fun = cap_spectral_density
    _cap_spec_dens_kwargs = {
        'T': param_mesh["temp_a"][idx],
        'EC': flxn.EC,
        'Q_cap': param_mesh["Q_cap"][idx],
    }
    
    constructor.add_channel(
        channel = 'flxn_ind',
        op = hspace.op_in_dressed_eigenbasis(
            op_callable_or_tuple = flxn.phi_operator,
            truncated_dim = truncated_dim
        ),
        spec_dens_fun = ind_spectral_density,
        spec_dens_kwargs = {
            'T': param_mesh["temp_a"][idx],
            'EL': flxn.EL,
            'Q_ind': param_mesh["Q_ind"][idx],
        },
        depolarization_only = True,
    )
    
    constructor.add_channel(
        channel = 'flxn_cap',
        op = hspace.op_in_dressed_eigenbasis(
            op_callable_or_tuple = flxn.n_operator,
            truncated_dim = truncated_dim
        ),
        spec_dens_fun = _cap_spec_dens_fun,
        spec_dens_kwargs = _cap_spec_dens_kwargs,
        depolarization_only = True,
    )

    # add the resonator decay & excitation channel
    constructor.add_channel(
        channel = 'res_decay',
        op = hspace.op_in_dressed_eigenbasis(
            op_callable_or_tuple = (
                osc.creation_operator() + osc.annihilation_operator(),
                osc,
            ),
            truncated_dim = truncated_dim,
            op_in_bare_eigenbasis = True,
        ),
        spec_dens_fun = ohmic_spectral_density,
        spec_dens_kwargs = {
            'T': param_mesh["temp_s"][idx],
            'Q': param_mesh["Q_s"][idx],
        },
        depolarization_only = True,
    )
    
    if callable(dephasing_spec_dens):
        _deph_spec_dens_fun = dephasing_spec_dens
        _deph_spec_dens_kwargs = {}
    elif dephasing_spec_dens == "delta":
        _deph_spec_dens_fun = delta_spectral_density
        _deph_spec_dens_kwargs = {
            'peak_value': param_mesh["A_phi"][idx],
        }
    elif dephasing_spec_dens == "flat":
        _deph_spec_dens_fun = flat_spectral_density
        _deph_spec_dens_kwargs = {
            'coeff': param_mesh["A_phi"][idx],
            'T': param_mesh["temp_a"][idx],
        }
    elif dephasing_spec_dens == "inv":
        _deph_spec_dens_fun = inv_spectral_density
        _deph_spec_dens_kwargs = {
            'peak_value': param_mesh["A_phi"][idx],
            'T': param_mesh["temp_a"][idx],
        }
    else:
        raise ValueError(f"Invalid dephasing spec dens: {dephasing_spec_dens}")
        
    
    # add the qubit capacitive noise channel
    constructor.add_channel(
        channel = 'flxn_dephase',
        op = hspace.op_in_dressed_eigenbasis(
            op_callable_or_tuple = flxn.d_hamiltonian_d_flux,
            truncated_dim = truncated_dim
        ),
        spec_dens_fun = _deph_spec_dens_fun,
        spec_dens_kwargs = _deph_spec_dens_kwargs,
        depolarization_only = False,
    )

    return constructor

def sweep_jump_ops(
    ps: scq.ParameterSweep,
    idx,
    use_ULE = False,
    max_jump_nums = 5,  # since we are uding ULE, there aren't too many jumps
):
    constructor: MEConstructor = ps["constructor"][idx]
    
    if not use_ULE:
        c_ops = [dq.asqarray(op) for op in constructor.all_clustered_jump_ops()]
    else:
        c_ops = [dq.asqarray(op) for op in constructor.all_ULE_jump_ops()]
        
    len_c_ops = len(c_ops)
    if len_c_ops > max_jump_nums:
        raise ValueError(f"Too many jumps: {len_c_ops} > {max_jump_nums}")

    result = np.empty(max_jump_nums, dtype=object)
    result[:len_c_ops] = c_ops
    return result

def sweep_decay_time(ps: scq.ParameterSweep, idx):
    jump_ops = ps["jump_ops"][idx]
    decay_times = np.zeros(jump_ops[0].shape)
    for jump_op in jump_ops:
        if jump_op is None:
            continue
        for idx, matelem in np.ndenumerate(jump_op.to_numpy()):
            if matelem is not None:
                decay_times[idx] += np.abs(matelem)**2
    return 1 / decay_times

def sweep_drive_op(
    ps: scq.ParameterSweep,
    idx,
    truncated_dim
):
    param_mesh = ps.parameters.meshgrids_by_paramname()
    hspace = ps.hilbertspace
    flxn, osc = hspace.subsystem_list
    op = hspace.op_in_dressed_eigenbasis(
        op_callable_or_tuple = (
            osc.creation_operator() + osc.annihilation_operator(),
            osc,
        ),
        truncated_dim = truncated_dim,
        op_in_bare_eigenbasis = True,
    )
    drive_strength = param_mesh["drive_strength"][idx]
    
    return op * drive_strength

def sweep_drive_freq(
    ps: scq.ParameterSweep,
    idx,
):
    param_mesh = ps.parameters.meshgrids_by_paramname()
    ocs_freq = (ps.energy_by_bare_index((0, 1)) - ps.energy_by_bare_index((0, 0)))[idx]
    
    return ocs_freq + param_mesh["omega_d_shift"][idx]

def batched_sweep_ingredients(
    ps: scq.ParameterSweep,
    truncated_dim: int,
    use_flat_Qcap = False,
    dephasing_spec_dens: Literal["delta", "flat", "inv"] | Callable = "delta",
    use_ULE = False,
    standardize_evec_phase = True,
):
    if standardize_evec_phase:
        ps.add_sweep(
            standardize_evec_phase_func,
            sweep_name = "evecs",
            zero_phase_component = "max",
        )
    ps.add_sweep(
        sweep_constructor,
        sweep_name = "constructor",
        truncated_dim = truncated_dim,
        use_flat_Qcap = use_flat_Qcap,
        dephasing_spec_dens = dephasing_spec_dens,
    )
    ps.add_sweep(
        sweep_jump_ops,
        sweep_name = "jump_ops",
        use_ULE = use_ULE,
    )
    ps.add_sweep(
        sweep_decay_time,
        sweep_name = "decay_time",
    )
    ps.add_sweep(
        sweep_drive_op,
        sweep_name = "drive_op",
        truncated_dim = truncated_dim,
    )
    ps.add_sweep(
        sweep_drive_freq,
        sweep_name = "drive_freq",
    )
    
# Observable related ==============================================
def sweep_evec_projs(
    ps: scq.ParameterSweep,
    trunc,
):
    """Projectors on the dressed eigenvectors in the dressed basis, ordered by eigenenergies."""
    states = [
        qt.basis(trunc, idx) for idx in range(trunc)
    ]
    evec_projs = np.array([
        s * s.dag() for s in states
    ], dtype=object)
    return evec_projs

def sweep_subsys_proj(
    ps: scq.ParameterSweep,
    idx,
    subsys_idx,
    trunc,
):
    """
    Projectors on the specified dressed subsystem occupying different states.
    Ordered by the state index.
    """
    dims = ps.hilbertspace.subsystem_dims
    subsys_dim = dims[subsys_idx]
    evec_projs = ps["evec_projs"][idx]
    
    subsys_projs = np.array(
        [qt.qzero_like(evec_projs[0])] * subsys_dim,
        dtype=object
    )
    for bare_idx in np.ndindex(tuple(dims)):
        raveled_bare_idx = np.ravel_multi_index(bare_idx, dims)
        dressed_idx = ps["dressed_indices"][idx][raveled_bare_idx]
        
        if dressed_idx is None: 
            continue
        
        if dressed_idx >= trunc:    
            # smaller than the truncated dim during simulation
            continue
        
        # todo: check overlap threshold
        subsys_level_idx = bare_idx[subsys_idx]
        subsys_projs[subsys_level_idx] += evec_projs[dressed_idx]
        
    return subsys_projs

def sweep_res_num_op_dressed(
    ps: scq.ParameterSweep,
    idx,
):
    r"""
    Number op for the "dressed" resonator, represented in the dressed basis:
    
    \sum_{n, m} m |n,m><n,m| 
    
    where |n, m> are EIGENSTATES of the resonator.
    
    
    Must be run after the sweep_subsys_proj and store the resonator projs
    with key "res_projs"
    """
    res_projs = ps["res_projs"][idx]
    num = np.arange(len(res_projs))
    return np.sum(res_projs * num)

def sweep_res_num_op_bare(
    ps: scq.ParameterSweep,
    idx,
    trunc,
):
    r"""
    Number op for the "bare" resonator, represented in the dressed basis:
    
    \sum_{n, m} m |n,m><n,m| 
    
    where |n, m> are BARE STATES of the resonator.
    
    Resonator must be the second subsystem.
    """
    hspace = ps.hilbertspace
    _, osc = hspace.subsystem_list
    a = hspace.annihilate(osc)
    num = a.dag() * a
    
    # basis transformation
    evecs = ps["evecs"][idx]
    num_dressed = oprt_in_basis(num, evecs[:trunc])
    
    return num_dressed
    
def batched_sweep_obs_ops(
    ps: scq.ParameterSweep,
    truncated_dim: int,
):
    ps.add_sweep(
        sweep_evec_projs,
        sweep_name = "evec_projs",
        trunc = truncated_dim,
    )
    ps.add_sweep(
        sweep_subsys_proj,
        sweep_name = "qubit_projs",
        subsys_idx = 0,
        trunc = truncated_dim,
    )
    ps.add_sweep(
        sweep_subsys_proj,
        sweep_name = "res_projs",
        subsys_idx = 1,
        trunc = truncated_dim,
    )
    ps.add_sweep(
        sweep_res_num_op_dressed,
        sweep_name = "res_num_op_dressed",
    )
    ps.add_sweep(
        sweep_res_num_op_bare,
        sweep_name = "res_num_op_bare",
        trunc = truncated_dim,
    )

# Steady state ===================================================
def sweep_undriven_ss(
    ps: scq.ParameterSweep,
    idx,
):
    constructor: MEConstructor = ps["constructor"][idx]
    jump_ops = [
        op for op in ps["jump_ops"][idx] if op is not None
    ]
    
    steadystate = steadystate_dq(
        H_0 = dq.asqarray(constructor.hamiltonian()),  # 2pi already included
        c_ops = jump_ops,
    )
    return steadystate.to_qutip()

@partial(jit, static_argnums=(2, 3))
def apply_mask(
    op: dq.QArray, 
    mask: jnp.ndarray,
    diag_mask: bool = False,
    make_physical: bool = True,
) -> dq.QArray:
    # first separate the op into diag and off-diag parts
    op_jax = op.to_jax()
    op_diag = jnp.diag(jnp.diag(op_jax))
    op_off_diag = op_jax - op_diag
    
    # then apply the mask
    if diag_mask:   # mask is an 1D array
        mask_op = jnp.diag(mask)
        op_off_diag = mask_op @ op_off_diag @ mask_op
    else:   # mask is a 2D array
        if make_physical:
            # make the masked operator physical: Hermitian operators 
            # remain Hermitian; jump operators remain satisfying the 
            # detailed balance condition.
            mask = (mask + mask.T) / 2
        op_off_diag = mask * op_off_diag # element-wise multiplication
    return dq.asqarray(op_diag + op_off_diag, dims=op.dims)

def _me_ingredients_w_mask(
    ham, c_ops, drive_op, mask, 
    diag_mask = False,
    make_physical = True,
):
    ham_masked = apply_mask(ham, mask, diag_mask, make_physical)
    c_ops_masked = [
        apply_mask(c_op, mask, diag_mask, make_physical) 
        for c_op in c_ops
    ]
    drive_op_masked = apply_mask(drive_op, mask, diag_mask, make_physical)
    return ham_masked, c_ops_masked, drive_op_masked

def _flq_ss_w_mask(
    ham, c_ops, drive_op, drive_freq, mask, 
    diag_mask = False,
    n_it=3,
):
    ham_masked, c_ops_masked, drive_op_masked = _me_ingredients_w_mask(
        ham, c_ops, drive_op, mask, diag_mask, make_physical=True
    )
    ss = steadystate_floquet_full_dq(
        ham_masked, 
        c_ops_masked, 
        drive_op_masked * jnp.pi * 2, 
        drive_freq * jnp.pi * 2, 
        n_it=n_it
    )
    return ss

def sweep_flq_ss_grad_hess(
    ps: scq.ParameterSweep,
    idx,
    trunc,
    eps = 1e-6,
    diag_mask = False,
    return_hessian = False,
    metric: Literal["trace_distance", "inversion"] = "trace_distance",
):
    constructor: MEConstructor = ps["constructor"][idx]
    ham = dq.asqarray(constructor.hamiltonian())
    c_ops = [
        op for op in ps["jump_ops"][idx] if op is not None
    ]
    drive_op = dq.asqarray(ps["drive_op"][idx])
    drive_freq = ps["drive_freq"][idx]
    qubit_projs = ps["qubit_projs"][idx]
    qubit_0_proj = dq.asqarray(qubit_projs[0])
    qubit_1_proj = dq.asqarray(qubit_projs[1])
    
    if metric == "trace_distance":
        if diag_mask:
            mask_ref = jnp.ones(trunc)
        else:
            mask_ref = jnp.ones((trunc, trunc))
        ss = _flq_ss_w_mask(
            ham, c_ops, drive_op, drive_freq, mask_ref,
            diag_mask=diag_mask,
        )[0]
        
        def metric_func(mask, ham, c_ops, drive_op, drive_freq):
            ss_perturbed = _flq_ss_w_mask(
                ham, c_ops, drive_op, drive_freq, mask,
                diag_mask=diag_mask,
            )[0]
            error = (ss_perturbed - ss).norm(psd=False).real
            return error
        
        if diag_mask:
            # Use sqrt(1-eps) so that D @ O @ D scales by (1-eps), matching the 2D case
            mask = jnp.ones(trunc) * jnp.sqrt(1 - eps)
        else:
            mask = jnp.ones((trunc, trunc)) * (1 - eps)
        grad_val = grad(metric_func)(
            mask, ham, c_ops, drive_op, drive_freq
        )
        
    elif metric == "inversion":
        def metric_and_ss(mask, ham, c_ops, drive_op, drive_freq):
            ss = _flq_ss_w_mask(
                ham, c_ops, drive_op, drive_freq, mask,
                diag_mask=diag_mask,
            )[0]
            q0 = dq.expect(qubit_0_proj, ss).real
            q1 = dq.expect(qubit_1_proj, ss).real
            return q1 - q0, ss
        def metric_func(mask, ham, c_ops, drive_op, drive_freq):
            return metric_and_ss(mask, ham, c_ops, drive_op, drive_freq)[0] # for potential hessian calculation
        if diag_mask:
            mask = jnp.ones(trunc)
        else:
            mask = jnp.ones((trunc, trunc))
        (_, ss), grad_val = value_and_grad(metric_and_ss, has_aux=True)(
            mask, ham, c_ops, drive_op, drive_freq,
        )
    
    if return_hessian:
        # For hessian, we need a function that returns only the scalar
        hess_val = hessian(metric_func)(
            mask, ham, c_ops, drive_op, drive_freq,
        )
        return np.array([ss.to_qutip(), grad_val, hess_val], dtype=object)
    
    return np.array([ss.to_qutip(), grad_val], dtype=object)

def batched_sweep_steadystate(
    ps: scq.ParameterSweep,
    trunc,
    eps = 1e-6,
    grad_metric = "trace_distance",
    return_hessian = False,
    diag_mask = False,
):
    ps.add_sweep(
        sweep_undriven_ss,
        sweep_name = "ss",
    )
    
    ps.add_sweep(
        sweep_flq_ss_grad_hess,
        sweep_name = "flq_ss_grad_hess",
        trunc = trunc,
        eps = eps,
        metric = grad_metric,
        return_hessian = return_hessian,
        diag_mask = diag_mask,
    )
    
    ps.store_data(
        flq_ss = ps["flq_ss_grad_hess"][..., 0],
        flq_ss_grad = ps["flq_ss_grad_hess"][..., 1],
    )
    if return_hessian:
        ps.store_data(
            flq_ss_hess = ps["flq_ss_grad_hess"][..., 2],
        )
        
# State evolution ==================================================
def sweep_init_state(
    ps: scq.ParameterSweep,
    idx,
    init_state: int | Literal["ss"] | Tuple[int, ...] = "ss",
):
    constructor: MEConstructor = ps["constructor"][idx]
    ham = dq.asqarray(constructor.hamiltonian())
    dim = ham.shape[0]
    
    if init_state == "ss":
        init_state = ps["ss"][idx]
    elif isinstance(init_state, int):
        init_state = qt.basis(dim, init_state)
        init_state = init_state * init_state.dag()
    else:   # tuple -> bare index
        dims = ps.hilbertspace.subsystem_dims
        raveled_bare_idx = np.ravel_multi_index(init_state, dims)
        drs_idx = ps["dressed_indices"][idx][raveled_bare_idx]
        init_state = qt.basis(dim, drs_idx)
        init_state = init_state * init_state.dag()

    return init_state

def sweep_state_evolution(
    ps: scq.ParameterSweep,
    idx,
    init_state: int | Literal["ss"] | Tuple[int, ...] = "ss",
    total_time = None,
    time_steps = 2,
    progress_meter = False,
    use_dq = True,
    tol = 1e-9,
):
    constructor: MEConstructor = ps["constructor"][idx]
    ham = dq.asqarray(constructor.hamiltonian())
    c_ops = [
        op for op in ps["jump_ops"][idx] if op is not None
    ]
    drive_op = dq.asqarray(ps["drive_op"][idx])
    drive_freq = ps["drive_freq"][idx]
    
    init_state = ps["evo_init_state"][idx]
    
    if total_time is None:
        total_time = 1 / drive_freq
    
    if use_dq:
        ham_t = dq.modulated(
            lambda t: jnp.cos(2 * np.pi * drive_freq * t),
            drive_op * jnp.pi * 2
        ) + ham
        res = dq.mesolve(
            H = ham_t,
            rho0 = dq.asqarray(init_state),
            jump_ops = c_ops,
            tsave = np.linspace(0, total_time, time_steps),
            method = Tsit5(max_steps=100000000, rtol=tol, atol=tol),
            options = dq.Options(progress_meter=progress_meter),
        )
    else:
        ham_t = [
            ham.to_qutip(),
            [
                drive_op.to_qutip() * np.pi * 2, 
                lambda t, *args: np.cos(2 * np.pi * drive_freq * t)
            ],
        ]
        res = qt.mesolve(
            H = ham_t,
            rho0 = init_state,
            c_ops = [op.to_qutip() for op in c_ops],
            tlist = np.linspace(0, total_time, time_steps),
            options = dict(
                nsteps=100000000,
                progress_bar=progress_meter,
                rtol=tol,
                atol=tol,
            ),
        )
    
    return res

# def sweep_undriven_prop(
#     ps: scq.ParameterSweep,
#     idx,
#     trunc,
#     total_time = None,
# ):
#     constructor: MEConstructor = ps["constructor"][idx]
#     ham = dq.asqarray(constructor.hamiltonian())
#     c_ops = [dq.asqarray(op) for op in constructor.all_clustered_jump_ops()]

def sweep_extract_evo_states(ps, idx, use_dq = True):
    res = ps["state_evolution"][idx]
    if use_dq:
        return [s.to_qutip() for s in res.states]
    else:
        return np.array(res.states, dtype=object)

def sweep_extract_evo_tsave(ps, idx, use_dq = True):
    res = ps["state_evolution"][idx]
    if use_dq:
        return np.array(res.tsave)
    else:
        return np.array(res.times)

def batched_sweep_state_evolution(
    ps: scq.ParameterSweep,
    init_state = "ss",
    total_time = None,
    time_steps = 2,
    num_cpus = 1,
    progress_meter = False,
    use_dq = True,
):
    ps.add_sweep(
        sweep_init_state,
        sweep_name = "evo_init_state",
        init_state = init_state,
    )
    tmp_num_cpus = ps._num_cpus
    ps._num_cpus = num_cpus    
    ps.add_sweep(
        sweep_state_evolution,
        sweep_name = "state_evolution",
        total_time = total_time,
        time_steps = time_steps,
        progress_meter = progress_meter,
        use_dq = use_dq,
    )
    ps._num_cpus = tmp_num_cpus
    
    ps.add_sweep(
        sweep_extract_evo_states,
        sweep_name = "evo_s",
        use_dq = use_dq,
    )
    ps.add_sweep(
        sweep_extract_evo_tsave,
        sweep_name = "evo_tsave",
        use_dq = use_dq,
    )


# Propagators (w/ drive) =============================================
def _prop_w_mask(
    ham, c_ops, drive_op, drive_freq, mask, 
    total_time = None,
    diag_mask = False,
    tol = 1e-9,
):
    ham_masked, c_ops_masked, drive_op_masked = _me_ingredients_w_mask(
        ham, c_ops, drive_op, mask, diag_mask, make_physical=True
    )
    ham_t = dq.modulated(
        lambda t: jnp.cos(2 * np.pi * drive_freq * t),
        drive_op_masked * jnp.pi * 2
    ) + ham_masked
    prop = dq.mepropagator(
        H = ham_t,
        jump_ops = c_ops_masked,
        tsave = np.linspace(0, total_time, 2),
        method = Tsit5(rtol=tol, atol=tol),
        options = dq.Options(),
    )
    return prop.final_propagator

def sweep_short_prop(
    ps: scq.ParameterSweep,
    idx,
    trunc,
    total_time = None,
    diag_mask = False,
    tol = 1e-9,
):
    """
    Solve the propagator for total_time % T, where T is the period of the drive.
    If total_time is None, solve for one period.
    """
    constructor: MEConstructor = ps["constructor"][idx]
    ham = dq.asqarray(constructor.hamiltonian())
    c_ops = [
        op for op in ps["jump_ops"][idx] if op is not None
    ]
    drive_op = dq.asqarray(ps["drive_op"][idx])
    drive_freq = ps["drive_freq"][idx]
    
    if diag_mask:
        mask = jnp.ones(trunc)
    else:
        mask = jnp.ones((trunc, trunc))
        
    T = 1 / drive_freq
    if total_time is None:
        evo_time = T
    else:
        evo_time = total_time % T
        
    prop = _prop_w_mask(
        ham, c_ops, drive_op, drive_freq, mask, 
        total_time=evo_time, 
        diag_mask=diag_mask,
        tol=tol,
    )
    
    # convert to qutip object
    prop_np = prop.to_numpy()
    prop_qt = qt.Qobj(prop_np, dims = [[[trunc]] * 2] * 2)
    return prop_qt

def sweep_prop_power(
    ps: scq.ParameterSweep,
    idx,
    num_periods,
):
    """
    Must be run after the sweep_prop and store the propagator with key "prop_1period"
    """
    prop_1period = ps["prop_1period"][idx]
    return prop_1period**num_periods

def sweep_subsys_truncator(
    ps: scq.ParameterSweep,
    idx,
    subsys_idx,
    trunc,
):
    """
    Projectors on the specified dressed subsystem occupying different states.
    Ordered by the state index.
    """
    dims = ps.hilbertspace.subsystem_dims
    subsys_dim = dims[subsys_idx]
    
    subsys_vecs = np.ndarray(
        subsys_dim,
        dtype=object
    )
    for bare_idx in np.ndindex(tuple(dims)):
        raveled_bare_idx = np.ravel_multi_index(bare_idx, dims)
        dressed_idx = ps["dressed_indices"][idx][raveled_bare_idx]
        
        if dressed_idx is None: 
            continue
        
        if dressed_idx >= trunc:    
            # smaller than the truncated dim during simulation
            continue
        
        # todo: check overlap threshold
        subsys_level_idx = bare_idx[subsys_idx]
        if subsys_vecs[subsys_level_idx] is None:
            subsys_vecs[subsys_level_idx] = []
            
        subsys_vecs[subsys_level_idx].append(qt.basis(trunc, dressed_idx))
            
    max_len_vecs = max([
        len(vecs) for vecs in subsys_vecs
        if vecs is not None
    ])
            
    subsys_projs = np.ndarray(subsys_dim, dtype=object)
    for i in range(subsys_dim):
        vecs = subsys_vecs[i]
        if vecs is None:
            break
        for _ in range(max_len_vecs - len(vecs)):
            vecs.append(qt.zero_ket(vecs[0].dims[0]))
        
        subsys_projs[i] = trans_by_kets(vecs)
        
    return subsys_projs

def sweep_prop_comps(
    ps: scq.ParameterSweep,
    idx,
):
    """
    Must be run after the sweep_prop and store the propagator with key "prop_1period"
    as well as the projectors with key "qubit_projs"
    """
    prop_1period = ps["prop_1period"][idx]
    qubit_truncs = ps["qubit_truncator"][idx]
    len_projs = len(qubit_truncs)
    
    qubit_proj_maps = np.ndarray((len_projs,) * 2, dtype=object)
    for i in range(len_projs):
        for j in range(len_projs):
            proj_i = qubit_truncs[i]
            proj_j = qubit_truncs[j]
            if proj_i is None or proj_j is None:
                continue
            qubit_proj_maps[i, j] = qt.sprepost(proj_i, proj_j.dag())
    
    prop_comps = np.ndarray((len_projs,) * 4, dtype=object)
    for (i, j), proj_map_ij in np.ndenumerate(qubit_proj_maps):
        for (k, l), proj_map_kl in np.ndenumerate(qubit_proj_maps):
            if proj_map_ij is None or proj_map_kl is None:
                continue
            prop_comps[i, j, k, l] = proj_map_ij.dag() * prop_1period * proj_map_kl
    
    return prop_comps

def sweep_prop_comps_norm(
    ps: scq.ParameterSweep,
    idx,
    norm_type: Literal["tr", "dnorm", "max", "one", "fro"] = "1norm",
    progress_bar = False,
):
    """
    Must be run after the sweep_prop_comps and store the propagator with key "prop_comps"
    """
    prop_comps = ps["prop_comps"][idx]
    norms = np.zeros_like(prop_comps)
    for idx, comp in tqdm(
        np.ndenumerate(prop_comps), 
        total=prop_comps.size, 
        desc="Calculating norms", 
        disable=not progress_bar,
    ):
        if comp is None:
            continue
        if norm_type == "dnorm":
            norms[idx] = qt.dnorm(comp, solver="MOSEK")
        else:
            norms[idx] = comp.norm(norm_type)
    return norms

def sweep_prop_eigendecomp(
    ps: scq.ParameterSweep,
    idx,
):
    prop_1period = ps["prop_1period"][idx]
    prop_data = prop_1period.full()
    eigvals, V = np.linalg.eig(prop_data)
    V_inv = np.linalg.inv(V)
    return {
        "eigvals": eigvals,
        "V": V,
        "V_inv": V_inv,
    }

def sweep_state_propagation(
    ps: scq.ParameterSweep,
    idx,
    total_time = 30e3,
    period_per_step = 100000,
):
    freq = ps["drive_freq"][idx]
    T = 1 / freq
    time_steps = np.arange(0, total_time, T * period_per_step)
    final_prop_time = total_time - total_time % T     # add the remainder of the period
    time_steps = np.append(time_steps, final_prop_time)

    init_state = ps["prop_init_state"][idx]
    states = [init_state]
    
    # Eigendecompose the propagator once for fast matrix powers
    prop_1period = ps["prop_1period"][idx]
    eigvals = ps["prop_eigendecomp"][idx]["eigvals"]
    V = ps["prop_eigendecomp"][idx]["V"]
    V_inv = ps["prop_eigendecomp"][idx]["V_inv"]
    V_qobj = qt.Qobj(V, dims=prop_1period.dims)
    V_inv_qobj = qt.Qobj(V_inv, dims=prop_1period.dims)
    
    for time_step in time_steps[1:]:
        num_periods = time_step / T
        assert np.isclose(num_periods, np.round(num_periods))
        n = int(np.round(num_periods))
        
        eigval_power_qobj = qt.Qobj(np.diag(eigvals ** n), dims=prop_1period.dims)
        
        state = superop_evolve(
            V_qobj, 
            superop_evolve(
                eigval_power_qobj,
                superop_evolve(
                    V_inv_qobj,
                    init_state,
                ),
            ),
        )
        states.append(state)
        
    # final state at t_max
    time_steps = np.append(time_steps, total_time)
    prop = ps["prop_remainder"][idx]
    states.append(superop_evolve(prop, states[-1]))

    return {
        "states": np.array(states, dtype=object),
        "time_steps": time_steps,
    }
    
def sweep_extract_prop_states(ps, idx, len_steps):
    res = ps["state_propagation"][idx]
    states = np.ndarray((len_steps,), dtype=object)
    len_states = len(res["states"])
    states[:len_states] = res["states"]
    return states

def sweep_extract_prop_tsave(ps, idx, len_steps):
    res = ps["state_propagation"][idx]
    time_steps = np.zeros((len_steps,), dtype=float) * np.nan
    len_time_steps = len(res["time_steps"])
    time_steps[:len_time_steps] = res["time_steps"]
    return time_steps

def batched_sweep_propagator(
    ps: scq.ParameterSweep,
    trunc,
    num_periods = None,
    diag_mask = False,
    run_analysis = False,
    total_time = None,
    init_state = "ss",
    period_per_step = 100000,
    tol = 1e-9,
):
    ps.add_sweep(
        sweep_short_prop,
        sweep_name = "prop_1period",
        trunc = trunc,
        total_time = None,
        diag_mask = diag_mask,
        tol = tol,
    )
    if isinstance(num_periods, int):
        ps.add_sweep(
            sweep_prop_power,
            sweep_name = f"prop_{num_periods}periods",
            num_periods = num_periods,
        )
    if run_analysis:
        ps.add_sweep(
            sweep_subsys_truncator,
            sweep_name = f"qubit_truncator",
            subsys_idx = 0,
            trunc = trunc,
        )
        ps.add_sweep(
            sweep_prop_comps,
            sweep_name = "prop_comps",
        )
        ps.add_sweep(
            sweep_prop_comps_norm,
            sweep_name = "prop_comps_norm",
            norm_type = "1norm",
        )
    if total_time is not None:
        ps.add_sweep(
            sweep_init_state,
            sweep_name = "prop_init_state",
            init_state = init_state,
        )
        ps.add_sweep(
            sweep_short_prop,
            sweep_name = "prop_remainder",
            trunc = trunc,
            total_time = total_time,
            diag_mask = diag_mask,
            tol = tol,
        )
        ps.add_sweep(
            sweep_prop_eigendecomp,
            sweep_name = "prop_eigendecomp",
        )
        ps.add_sweep(
            sweep_state_propagation,
            sweep_name = "state_propagation",
            total_time = total_time,
            period_per_step = period_per_step,
        )
        len_steps = max([
            len(res["time_steps"]) for res in ps["state_propagation"].flat
        ])
        ps.add_sweep(
            sweep_extract_prop_states,
            sweep_name = "prop_s",
            len_steps = len_steps,
        )
        ps.add_sweep(
            sweep_extract_prop_tsave,
            sweep_name = "prop_tsave",
            len_steps = len_steps,
        )
        
# Observables =====================================================
def sweep_evec_occ(
    ps: scq.ParameterSweep,
    idx,
    state_key,
    for_multi_states = False,
):
    """Must be run after the sweep_evec_projs and store the evec_projs with key "evec_projs"
    """
    evec_projs = ps["evec_projs"][idx]
    state = ps[state_key][idx]
    
    if not for_multi_states:
        return np.array([
            dq.expect(proj, state).real      # dq accept both qt and dq objects
            for proj in evec_projs
        ])
    else:
        return np.array([
            [
                dq.expect(proj, st).real if st is not None else np.nan
                for proj in evec_projs
            ] for st in state
        ])

def sweep_subsys_occ(
    ps: scq.ParameterSweep,
    idx,
    state_key,
    subsys_idx, 
    for_multi_states = False,
):
    f"""Must be run after the sweep_subsys_proj and store the subsys_projs with key "<qubit/res>_projs"
    """
    if subsys_idx == 0:
        subsys_projs = ps["qubit_projs"][idx]
    elif subsys_idx == 1:
        subsys_projs = ps["res_projs"][idx]
    else:
        raise ValueError(f"Invalid subsys_idx: {subsys_idx}")
    state = ps[state_key][idx]
    
    if not for_multi_states:
        return np.array([
            qt.expect(proj, state)
            for proj in subsys_projs
        ])
    else:
        return np.array([
            [
                qt.expect(proj, st) if st is not None else np.nan 
                for proj in subsys_projs
            ] for st in state
        ])

def sweep_res_num_dressed(
    ps: scq.ParameterSweep,
    idx,
    state_key,
    for_multi_states = False,
):
    """Must be run after the sweep_res_num_op_dressed and store the dressed number op with key "res_num_op_dressed"
    """
    res_num_op_dressed = ps["res_num_op_dressed"][idx]
    state = ps[state_key][idx]
    
    if not for_multi_states:
        return qt.expect(res_num_op_dressed, state)
    else:
        return np.array([
            qt.expect(res_num_op_dressed, st) if st is not None else np.nan
            for st in state
        ])

def sweep_res_num_bare(
    ps: scq.ParameterSweep,
    idx,
    state_key,
    for_multi_states = False,
):
    """Must be run after the sweep_res_num_op_bare and store the bare number op with key "res_num_op_bare"
    """
    res_num_op_bare = ps["res_num_op_bare"][idx]
    state = ps[state_key][idx]
    
    if not for_multi_states:
        return qt.expect(res_num_op_bare, state)
    else:
        return np.array([
            qt.expect(res_num_op_bare, st) if st is not None else np.nan
            for st in state
        ])
        
def to_numpy(data):
    if isinstance(data, qt.Qobj):
        data = data.full()
    elif isinstance(data, dq.QArray):
        data = data.to_numpy()
    elif isinstance(data, jax_Array):
        data = np.asarray(data)
    elif isinstance(data, np.ndarray):
        pass
    else:
        raise ValueError(f"Invalid data type: {type(data)}")
    return data

def organize_data_by_bare_index(
    ps: scq.ParameterSweep,
    idx,
    key,
    dim_to_organize = 0,
    fill_value=np.nan,
    for_multi_states = False,
):
    data = ps[key][idx]
    if not for_multi_states:
        return organize_by_bare_index(
            to_numpy(data), 
            ps.hilbertspace, 
            ps["dressed_indices"][idx], 
            fill_value=fill_value,
            dim_to_organize=dim_to_organize,
        )
    else:
        return np.array([
            organize_by_bare_index(
                to_numpy(dt), 
                ps.hilbertspace, 
                ps["dressed_indices"][idx], 
                fill_value=fill_value,
                dim_to_organize=dim_to_organize,
            ) for dt in data
        ])
        
def batched_sweep_obs_exps(
    ps: scq.ParameterSweep,
    diag_mask = False,
    state_keys = ["ss", "flq_ss", "evo_s", "prop_s"],
):
    for state_key in state_keys:
        if state_key in ["evo_s", "prop_s"]:
            for_multi_states = True
        else:
            for_multi_states = False
            
        if state_key not in ps.keys():
            continue
        
        ps.add_sweep(
            sweep_evec_occ,
            sweep_name = f"{state_key}_evec_occ",
            state_key = state_key,
            for_multi_states = for_multi_states,
        )
        ps.add_sweep(
            organize_data_by_bare_index,
            sweep_name = f"{state_key}_evec_occ_arr",
            key = f"{state_key}_evec_occ",
            for_multi_states = for_multi_states,
        )
        ps.add_sweep(
            sweep_subsys_occ,
            sweep_name = f"{state_key}_qubit_occ",
            state_key = state_key,
            subsys_idx = 0,
            for_multi_states = for_multi_states,
        )
        ps.add_sweep(
            sweep_subsys_occ,
            sweep_name = f"{state_key}_res_occ",
            state_key = state_key,
            subsys_idx = 1,
            for_multi_states = for_multi_states,
        )
        ps.add_sweep(
            sweep_res_num_dressed,
            sweep_name = f"{state_key}_res_num_dressed",
            state_key = state_key,
            for_multi_states = for_multi_states,
        )
        ps.add_sweep(
            sweep_res_num_bare,
            sweep_name = f"{state_key}_res_num_bare",
            state_key = state_key,
            for_multi_states = for_multi_states,
        )
      
    if diag_mask:
        dim_to_organize = 0
    else:
        dim_to_organize = (0, 1)
        
    if "flq_ss_grad" in ps.keys():
        ps.add_sweep(
            organize_data_by_bare_index,
            sweep_name = "grad_arr",
            key = "flq_ss_grad",
            dim_to_organize = dim_to_organize,
            for_multi_states = False,
        )

    if "flq_ss_hess" in ps.keys():
        ps.add_sweep(
            organize_data_by_bare_index,
            sweep_name = "hess_arr",
            key = "flq_ss_hess",
            for_multi_states = False,
        )

    ps.add_sweep(
        organize_data_by_bare_index,
        sweep_name = "eval_arr",
        key = "evals",
        for_multi_states = False,
    )
    
# Analyze large matrices ==========================================
def sweep_order_matelems(
    ps: scq.ParameterSweep,
    idx,
    key,
    order: Literal["ascending", "descending"] = "descending",
    matelems_count: int | None = None,
    return_mod_square: bool = False,
):
    array = ps[key][idx]
    ordered_matelems = order_matelems(
        to_numpy(array), 
        order=order,
        matelems_count=matelems_count, 
        return_mod_square=return_mod_square,
    )
    return ordered_matelems

def batched_sweep_analyze_matrices(
    ps: scq.ParameterSweep,
):
    ps.add_sweep(
        organize_data_by_bare_index,
        sweep_name = "drive_op_arr",
        key = "drive_op",
        dim_to_organize = (0, 1),
        for_multi_states = False,
    )
    ps.add_sweep(
        sweep_order_matelems,
        sweep_name = "drive_op_matelems",
        key = "drive_op_arr",
        order = "descending",
        matelems_count = None,
        return_mod_square = False,
    )
    
    ps.add_sweep(
        organize_data_by_bare_index,
        sweep_name = f"decay_time_arr",
        key = f"decay_time",
        dim_to_organize = (0, 1),
        )
    ps.add_sweep(
        sweep_order_matelems,
        sweep_name = f"decay_time_matelems",
        key = f"decay_time_arr",
        order = "ascending",
        matelems_count = None,
        return_mod_square = False,
    )
    
    ps.add_sweep(
        sweep_order_matelems,
        sweep_name = f"grad_matelems",
        key = f"grad_arr",
        order = "descending",
        matelems_count = None,
        return_mod_square = False,
    )
    
# Simple model from Darren ========================================
def sweep_simplemodel(
    ps: scq.ParameterSweep,
    idx,
    trunc: int,
):
    """
    Creating the simplemodel object from Darren's code. There are 
    some repeated calculations internally, but let us try to keep his 
    code unchanged as much as possible.
    """
    flxn, res = ps.hilbertspace.subsystem_list
    flxn_dim, res_dim = ps.hilbertspace.subsystem_dims
    coupling = ps.hilbertspace.interaction_list[0]
    param_mesh = ps.parameters.meshgrids_by_paramname()
    
    model = simplemodel(
        EJ=flxn.EJ, 
        EC=flxn.EC, 
        EL=flxn.EL, 
        g=coupling.g_strength, 
        E_osc=res.E_osc, 
        L_osc=res.l_osc, 
        flux=flxn.flux, 
        fdim=flxn_dim, rdim=res_dim, 
        total_truncation=trunc, 
        driveamp=param_mesh["drive_strength"][idx], 
        qubit_temp=param_mesh["temp_a"][idx], 
        resonator_temp=param_mesh["temp_s"][idx], 
        Qcap=param_mesh["Q_cap"][idx], 
        Qohmic=param_mesh["Q_s"][idx],
        atol=1e-8, 
        rtol=1e-8, 
        n_it=10,
    )
    return model

def sweep_reduced_states(
    ps: scq.ParameterSweep,
    idx,
    metric_cutoffs = np.logspace(-6, -4, 10),
    decay_cutoffs = np.logspace(-6, -4, 10),
):
    """
    Must be run after the sweep_simplemodel and store the simplemodel object with key "simplemodel"
    """
    model: simplemodel = ps["simplemodel"][idx]
    df_reduced = model.collect_convergence_grid(
        metric_cutoffs=metric_cutoffs,
        decay_cutoffs=decay_cutoffs,
        numsteps=25
    )
    df_reduced = df_reduced.drop_duplicates(subset='states').reset_index(drop=True)
    df_reduced = df_reduced.sort_values('n_states', ascending=True)
    return {"df":df_reduced}

def sweep_reduced_states_convergence(
    ps: scq.ParameterSweep,
    idx,
    tfinal = 30000,
):
    """
    Must be run after the sweep_reduced_states and store the dataframe with key "df_reduced"
    """
    model: simplemodel = ps["simplemodel"][idx]
    df_reduced = ps["df_reduced"][idx]["df"]
    #MESOLVE STEP FOR ALL THE REDUCED SETS OF STATES
    df_convergence, times, fullresultstates = model.complete_convergence_grid(
        df_reduced, 
        tfinal=tfinal
    )

    return {"df":df_convergence, "times":times, "states":fullresultstates}

def sweep_pathways(
    ps: scq.ParameterSweep,
    idx,
    starting_label = "0,0",
    metric_cutoff = 1e-6,
    decay_cutoff = 1e-6,
    num_steps = 25,
    max_cycles = 3,
):
    """
    Must be run after the sweep_simplemodel and store the simplemodel object with key "simplemodel"
    """
    model: simplemodel = ps["simplemodel"][idx]
    pathways = model.trace_pathways(
        starting_label=starting_label, 
        metriccutoff=metric_cutoff, 
        decaycutoff=decay_cutoff, 
        numsteps=num_steps, 
        max_cycles=max_cycles,
    )
    
    return {"pathways":pathways}
    
def batched_sweep_simplemodel(
    ps: scq.ParameterSweep,
    truncated_dim: int,
    run_convergence = False,
    convergence_tfinal = 30000,
    run_pathways = False,
    pathway_starting_label = "0,0",
    pathway_metric_cutoff = 1e-6,
    pathway_decay_cutoff = 1e-6,
    pathway_num_steps = 25,
    pathway_max_cycles = 3,
):
    """
    Must be run after the sweep_simplemodel and store the simplemodel object with key "simplemodel"
    """
    ps.add_sweep(
        sweep_simplemodel,
        sweep_name = "simplemodel",
        trunc = truncated_dim,
    )
    if run_convergence:
        ps.add_sweep(
            sweep_reduced_states,
            sweep_name = "df_reduced",
        )
        ps.add_sweep(
            sweep_reduced_states_convergence,
            sweep_name = "df_convergence",
            tfinal = convergence_tfinal,
        )
    if run_pathways:
        ps.add_sweep(
            sweep_pathways,
            sweep_name = "pathways",
            starting_label = pathway_starting_label,
            metric_cutoff = pathway_metric_cutoff,
            decay_cutoff = pathway_decay_cutoff,
            num_steps = pathway_num_steps,
            max_cycles = pathway_max_cycles,
        )
        
# Full sweep =====================================================
def batched_sweep_readout(
    ps: scq.ParameterSweep,
    truncated_dim: int,
    use_ULE = False,
    standardize_evec_phase = True,
    use_flat_Qcap = False,
    dephasing_spec_dens: Literal["delta", "flat", "inv"] | Callable = "delta",
    grad_eps = 1e-6,
    grad_metric = "trace_distance",
    return_hessian = False,
    diag_mask = False,
    # State evolution configurations
    run_state_evo = False,
    evo_total_time = None,
    evo_time_steps = 2,
    evo_init_state = "ss",
    evo_num_cpus = 1,
    evo_progress_meter = False,
    evo_use_dq = True,
    # State propagation configurations
    run_state_propagation = False,
    prop_tol = 1e-9,
    prop_total_time = 30e3,
    prop_init_state = "ss",
    prop_period_per_step = 100000,
    run_prop_analysis = False,
    **kwargs,
):
    try:
        print(ps.hilbertspace["evals"][0][0])
        print(ps["constructor"].flat[0].unclustered_jumps["flxn_cap"][1, 0])
    except:
        pass
    batched_sweep_ingredients(
        ps, truncated_dim, use_flat_Qcap, dephasing_spec_dens, use_ULE, standardize_evec_phase,
    )
    print(ps.hilbertspace["evals"][0][0])
    print(ps["constructor"].flat[0].unclustered_jumps["flxn_cap"][1, 0])
    batched_sweep_obs_ops(ps, truncated_dim)
    batched_sweep_steadystate(
        ps, truncated_dim, grad_eps, grad_metric, return_hessian, diag_mask,
    )
    if run_state_evo:
        batched_sweep_state_evolution(
            ps, 
            total_time = evo_total_time, 
            time_steps = evo_time_steps, 
            init_state = evo_init_state,
            num_cpus = evo_num_cpus,
            progress_meter = evo_progress_meter,
            use_dq = evo_use_dq,
        )
    if run_state_propagation:
        batched_sweep_propagator(
            ps, 
            trunc = truncated_dim,
            num_periods = None,     # don't compute power of propagator
            diag_mask = diag_mask,
            run_analysis = run_prop_analysis,
            total_time = prop_total_time,
            tol = prop_tol,
            init_state = prop_init_state,
            period_per_step = prop_period_per_step,
        )
    batched_sweep_obs_exps(ps, diag_mask)
    