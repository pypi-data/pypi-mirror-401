"""
CTMC Solver handler.

Native Python implementation of CTMC (Continuous-Time Markov Chain) solver
handler that analyzes queueing networks through exact state-space enumeration.

The CTMC solver builds the complete state space and infinitesimal generator
matrix, then solves for steady-state probabilities to compute performance metrics.

Port from:

"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple, Any
from itertools import product
import time

import warnings
from ...sn import (
    NetworkStruct,
    SchedStrategy,
    NodeType,
    RoutingStrategy,
    sn_is_open_model,
    sn_is_closed_model,
    sn_has_open_classes,
)
from ....constants import ProcessType
from ...mc import ctmc_solve, ctmc_makeinfgen


def _get_phases_info(sn: NetworkStruct) -> Tuple[np.ndarray, bool]:
    """
    Get number of phases for each (station, class) pair and detect if phase augmentation is needed.

    For phase-type distributions (PH, APH, MAP, MMPP2, Erlang, HyperExp, Coxian),
    the number of phases is determined from the distribution parameters stored in sn.proc.

    Args:
        sn: Network structure

    Returns:
        Tuple of (phases matrix [M x K], needs_phase_augmentation bool)
    """
    M = sn.nstations
    K = sn.nclasses
    phases = np.ones((M, K), dtype=int)
    needs_augmentation = False

    if not hasattr(sn, 'proc') or sn.proc is None:
        return phases, needs_augmentation

    # sn.proc can be a list or dict - handle both
    proc_is_list = isinstance(sn.proc, list)

    for ist in range(M):
        # Check if this station has proc data
        if proc_is_list:
            if ist >= len(sn.proc) or sn.proc[ist] is None:
                continue
            station_proc = sn.proc[ist]
        else:
            if ist not in sn.proc:
                continue
            station_proc = sn.proc[ist]

        for k in range(K):
            # Get proc entry for this (station, class)
            proc_entry = None
            if isinstance(station_proc, (list, tuple)):
                if k < len(station_proc):
                    proc_entry = station_proc[k]
            elif isinstance(station_proc, dict):
                proc_entry = station_proc.get(k)

            if proc_entry is None:
                continue

            n_phases = 1

            # Handle different storage formats
            if isinstance(proc_entry, dict):
                # Erlang: {'k': phases, 'mu': rate}
                if 'k' in proc_entry:
                    n_phases = int(proc_entry['k'])
                # HyperExp: {'probs': [...], 'rates': [...]}
                elif 'probs' in proc_entry and 'rates' in proc_entry:
                    probs = np.array(proc_entry['probs'])
                    proc_rates = np.array(proc_entry['rates'])
                    # Check if rates data is valid (not same as probs)
                    # If rates == probs, this indicates a data bug - treat as single phase
                    if np.allclose(proc_rates, probs):
                        n_phases = 1
                    else:
                        n_phases = len(proc_entry['probs'])
                # Exp: {'rate': ...} - single phase
                else:
                    n_phases = 1
            elif isinstance(proc_entry, (list, tuple)) and len(proc_entry) >= 1:
                # PH/APH/MAP: [alpha/D0, T/D1] where alpha/D0 determines phases
                first_elem = proc_entry[0]
                if isinstance(first_elem, np.ndarray):
                    if first_elem.ndim == 1:
                        # alpha vector
                        n_phases = len(first_elem)
                    else:
                        # D0 matrix
                        n_phases = first_elem.shape[0]
                elif isinstance(first_elem, (list, tuple)):
                    if len(first_elem) > 0 and isinstance(first_elem[0], (list, tuple, np.ndarray)):
                        # 2D structure
                        n_phases = len(first_elem)
                    else:
                        # 1D structure
                        n_phases = len(first_elem)

            phases[ist, k] = max(1, n_phases)
            if n_phases > 1:
                needs_augmentation = True

    return phases, needs_augmentation


def _get_map_fcfs_info(sn: NetworkStruct) -> Tuple[Dict[Tuple[int, int], int], bool]:
    """
    Identify (station, class) pairs that have MAP distributions at FCFS stations.

    For FCFS stations with MAP distributions, the state must include an additional
    variable tracking the MAP modulating phase (the "mode" of the MAP process).

    Args:
        sn: Network structure

    Returns:
        Tuple of (map_fcfs dict mapping (ist, k) to n_phases, has_map_fcfs bool)
    """
    M = sn.nstations
    K = sn.nclasses
    map_fcfs = {}  # (ist, k) -> n_phases for MAP distributions at FCFS stations
    has_map_fcfs = False

    if not hasattr(sn, 'proc') or sn.proc is None:
        return map_fcfs, has_map_fcfs
    if not hasattr(sn, 'sched') or sn.sched is None:
        return map_fcfs, has_map_fcfs
    if not hasattr(sn, 'procid') or sn.procid is None:
        return map_fcfs, has_map_fcfs

    proc_is_list = isinstance(sn.proc, list)

    for ist in range(M):
        # Check if this is an FCFS station
        sched = sn.sched.get(ist, SchedStrategy.FCFS)
        # FCFS variants that need MAP phase tracking
        fcfs_variants = [SchedStrategy.FCFS, SchedStrategy.HOL, SchedStrategy.LCFS]
        # Check for specific FCFS scheduling strategies
        is_fcfs_type = (sched in fcfs_variants or
                       (isinstance(sched, int) and sched in [1, 2, 3]))  # FCFS=1, LCFS=2, etc.

        if not is_fcfs_type:
            continue

        # Check if this station has proc data
        if proc_is_list:
            if ist >= len(sn.proc) or sn.proc[ist] is None:
                continue
            station_proc = sn.proc[ist]
        else:
            if ist not in sn.proc:
                continue
            station_proc = sn.proc[ist]

        for k in range(K):
            # Check process type
            if ist >= sn.procid.shape[0] or k >= sn.procid.shape[1]:
                continue
            procid = sn.procid[ist, k]

            # Check if MAP or MMPP2
            if procid not in [ProcessType.MAP, ProcessType.MMPP2]:
                continue

            # Get number of phases from proc entry
            proc_entry = None
            if isinstance(station_proc, (list, tuple)):
                if k < len(station_proc):
                    proc_entry = station_proc[k]
            elif isinstance(station_proc, dict):
                proc_entry = station_proc.get(k)

            if proc_entry is None:
                continue

            n_phases = 1
            if isinstance(proc_entry, (list, tuple)) and len(proc_entry) >= 2:
                # MAP: [D0, D1]
                D0 = np.atleast_2d(np.array(proc_entry[0], dtype=float))
                n_phases = D0.shape[0]

            if n_phases > 1:
                map_fcfs[(ist, k)] = n_phases
                has_map_fcfs = True

    return map_fcfs, has_map_fcfs


def _generate_phase_distributions(n_jobs: int, n_phases: int) -> List[Tuple[int, ...]]:
    """
    Generate all ways to distribute n_jobs across n_phases.

    This is equivalent to MATLAB's State.spaceClosedSingle.

    Args:
        n_jobs: Number of jobs to distribute
        n_phases: Number of phases

    Returns:
        List of tuples, each tuple has n_phases elements summing to n_jobs
    """
    if n_phases == 1:
        return [(n_jobs,)]
    if n_jobs == 0:
        return [tuple([0] * n_phases)]

    result = []
    for k in range(n_jobs + 1):
        # k jobs in first phase, rest in remaining phases
        for rest in _generate_phase_distributions(n_jobs - k, n_phases - 1):
            result.append((k,) + rest)
    return result


def _get_phase_transition_params(sn: NetworkStruct, ist: int, k: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Get phase transition parameters for a (station, class) pair.

    For PH/APH distributions: Returns (mu, phi, alpha) where
        - mu[i] = service rate in phase i
        - phi[i] = probability of completion from phase i (vs moving to another phase)
        - alpha[i] = initial probability of starting in phase i

    For MAP distributions: Returns (D0, D1, pi) where
        - D0 = transition matrix without completions
        - D1 = transition matrix with completions
        - pi = stationary distribution (initial phases)

    Args:
        sn: Network structure
        ist: Station index
        k: Class index

    Returns:
        For PH/APH: (mu, phi, alpha)
        For MAP: (D0, D1, pi)
    """
    if not hasattr(sn, 'proc') or sn.proc is None:
        return np.array([1.0]), np.array([1.0]), np.array([1.0])

    # Handle both list and dict formats for sn.proc
    proc_is_list = isinstance(sn.proc, list)
    if proc_is_list:
        if ist >= len(sn.proc) or sn.proc[ist] is None:
            rate = sn.rates[ist, k] if hasattr(sn, 'rates') and ist < sn.rates.shape[0] and k < sn.rates.shape[1] else 1.0
            return np.array([rate]), np.array([1.0]), np.array([1.0])
        station_proc = sn.proc[ist]
    else:
        if ist not in sn.proc or sn.proc[ist] is None:
            rate = sn.rates[ist, k] if hasattr(sn, 'rates') and ist < sn.rates.shape[0] and k < sn.rates.shape[1] else 1.0
            return np.array([rate]), np.array([1.0]), np.array([1.0])
        station_proc = sn.proc[ist]

    # Get proc entry for this class
    if isinstance(station_proc, (list, tuple)):
        if k >= len(station_proc) or station_proc[k] is None:
            rate = sn.rates[ist, k] if hasattr(sn, 'rates') and ist < sn.rates.shape[0] and k < sn.rates.shape[1] else 1.0
            return np.array([rate]), np.array([1.0]), np.array([1.0])
        proc_entry = station_proc[k]
    elif isinstance(station_proc, dict):
        if k not in station_proc or station_proc[k] is None:
            rate = sn.rates[ist, k] if hasattr(sn, 'rates') and ist < sn.rates.shape[0] and k < sn.rates.shape[1] else 1.0
            return np.array([rate]), np.array([1.0]), np.array([1.0])
        proc_entry = station_proc[k]
    else:
        rate = sn.rates[ist, k] if hasattr(sn, 'rates') and ist < sn.rates.shape[0] and k < sn.rates.shape[1] else 1.0
        return np.array([rate]), np.array([1.0]), np.array([1.0])

    # Check process type
    procid = None
    if hasattr(sn, 'procid') and sn.procid is not None:
        if ist < sn.procid.shape[0] and k < sn.procid.shape[1]:
            procid = sn.procid[ist, k]

    # Handle different distribution types
    if isinstance(proc_entry, dict):
        # Erlang: {'k': phases, 'mu': rate}
        if 'k' in proc_entry:
            n_phases = int(proc_entry['k'])
            rate = proc_entry.get('mu', 1.0)
            mu = np.full(n_phases, rate)
            phi = np.concatenate([np.zeros(n_phases - 1), [1.0]])  # Only complete from last phase
            alpha = np.zeros(n_phases)
            alpha[0] = 1.0  # Start in first phase
            return mu, phi, alpha
        # HyperExp: {'probs': [...], 'rates': [...]}
        elif 'probs' in proc_entry and 'rates' in proc_entry:
            probs = np.array(proc_entry['probs'])
            proc_rates = np.array(proc_entry['rates'])
            # Check if rates data is valid (not same as probs)
            # If rates == probs, this indicates a data bug - fall back to single-phase
            if np.allclose(proc_rates, probs):
                rate = sn.rates[ist, k] if hasattr(sn, 'rates') and ist < sn.rates.shape[0] and k < sn.rates.shape[1] else 1.0
                return np.array([rate]), np.array([1.0]), np.array([1.0])
            phi = np.ones(len(proc_rates))  # Each phase completes immediately
            return proc_rates, phi, probs
        # Exp: {'rate': ...}
        else:
            rate = proc_entry.get('rate', 1.0)
            return np.array([rate]), np.array([1.0]), np.array([1.0])

    elif isinstance(proc_entry, (list, tuple)) and len(proc_entry) >= 2:
        # PH/APH: [alpha, T]
        # MAP: [D0, D1]
        first = np.atleast_1d(np.array(proc_entry[0], dtype=float))
        second = np.atleast_2d(np.array(proc_entry[1], dtype=float))

        is_map = procid in [ProcessType.MAP, ProcessType.MMPP2] if procid is not None else False

        if is_map or (first.ndim == 2):
            # MAP: [D0, D1]
            D0 = np.atleast_2d(first)
            D1 = second
            # Compute stationary distribution
            Q = D0 + D1
            n = Q.shape[0]
            A = np.vstack([Q.T, np.ones(n)])
            b = np.zeros(n + 1)
            b[-1] = 1.0
            try:
                from scipy import linalg
                pi, _, _, _ = linalg.lstsq(A, b)
                pi = np.maximum(pi, 0)
                pi /= pi.sum() if pi.sum() > 0 else 1
            except:
                pi = np.ones(n) / n
            return D0, D1, pi
        else:
            # PH/APH: [alpha, T]
            alpha = first.flatten()
            T = second
            n_phases = len(alpha)

            # Extract service rates (negative diagonal of T)
            mu = -np.diag(T)

            # Compute exit rates (completion probability)
            exit_rates = -T.sum(axis=1)  # -T * e gives exit rates
            phi = np.zeros(n_phases)
            for i in range(n_phases):
                if mu[i] > 0:
                    phi[i] = exit_rates[i] / mu[i]

            return mu, phi, alpha

    # Default: exponential
    rate = sn.rates[ist, k] if hasattr(sn, 'rates') and ist < sn.rates.shape[0] and k < sn.rates.shape[1] else 1.0
    return np.array([rate]), np.array([1.0]), np.array([1.0])


def _ctmc_stochcomp(Q: np.ndarray, keep_indices: List[int]) -> Tuple[np.ndarray, np.ndarray]:
    """
    Perform stochastic complementation to remove immediate states.

    This removes states where jobs are at non-station stateful nodes
    (like Router) by computing the equivalent transitions that bypass
    these nodes.

    Args:
        Q: Full infinitesimal generator matrix
        keep_indices: Indices of states to keep (non-immediate states)

    Returns:
        Tuple of (reduced Q matrix, transformation matrix for rates)
    """
    n = Q.shape[0]
    all_indices = set(range(n))
    remove_indices = sorted(all_indices - set(keep_indices))

    if not remove_indices:
        return Q, np.eye(n)

    keep_indices = sorted(keep_indices)

    # Partition Q into blocks:
    # Q = [Q11 Q12]  where 1 = keep, 2 = remove
    #     [Q21 Q22]
    Q11 = Q[np.ix_(keep_indices, keep_indices)]
    Q12 = Q[np.ix_(keep_indices, remove_indices)]
    Q21 = Q[np.ix_(remove_indices, keep_indices)]
    Q22 = Q[np.ix_(remove_indices, remove_indices)]

    # Stochastic complement: Q_reduced = Q11 + Q12 * (-Q22)^{-1} * Q21
    # For immediate transitions, Q22 should be invertible
    try:
        # Add small regularization for numerical stability
        Q22_inv = np.linalg.inv(-Q22 + np.eye(len(remove_indices)) * 1e-10)
        Q_reduced = Q11 + Q12 @ Q22_inv @ Q21
    except np.linalg.LinAlgError:
        # Fallback: just return the kept states without complementation
        Q_reduced = Q11

    # Make it a valid generator
    Q_reduced = ctmc_makeinfgen(Q_reduced)

    return Q_reduced, Q12 @ Q22_inv if len(remove_indices) > 0 else np.eye(len(keep_indices))


def _get_rrobin_outlinks(sn: NetworkStruct) -> dict:
    """
    Get outlinks for nodes with RROBIN/WRROBIN routing.

    Returns a dict: {(node_idx, class_idx): [outlink_node_indices]}
    """
    outlinks = {}

    if not hasattr(sn, 'routing') or sn.routing is None:
        return outlinks
    if not hasattr(sn, 'connmatrix') or sn.connmatrix is None:
        return outlinks

    routing = np.asarray(sn.routing)
    connmatrix = np.asarray(sn.connmatrix)

    N = routing.shape[0]  # Number of nodes
    K = routing.shape[1]  # Number of classes

    for ind in range(N):
        for r in range(K):
            strategy = routing[ind, r]
            # Check for RROBIN (3) or WRROBIN (4)
            if strategy == 3 or strategy == 4:  # RROBIN or WRROBIN
                # Get outgoing links from connection matrix
                links = np.where(connmatrix[ind, :] > 0)[0].tolist()
                if links:
                    outlinks[(ind, r)] = links

    return outlinks


def _build_rrobin_state_info(sn: NetworkStruct) -> dict:
    """
    Build information about round-robin state variables.

    Returns a dict with:
        'outlinks': {(node_idx, class_idx): [outlink_indices]}
        'state_vars': List of (node_idx, class_idx, num_outlinks) tuples
        'total_vars': Total number of extra state variables
        'non_station_stateful': Set of node indices that are stateful but not stations
    """
    outlinks = _get_rrobin_outlinks(sn)

    state_vars = []
    for (node_idx, class_idx), links in sorted(outlinks.items()):
        state_vars.append((node_idx, class_idx, len(links)))

    # Identify non-station stateful nodes (like Router)
    non_station_stateful = set()
    if hasattr(sn, 'isstation') and hasattr(sn, 'isstateful'):
        isstation = np.asarray(sn.isstation).flatten()
        isstateful = np.asarray(sn.isstateful).flatten()
        for i in range(len(isstation)):
            if isstateful[i] and not isstation[i]:
                non_station_stateful.add(i)

    return {
        'outlinks': outlinks,
        'state_vars': state_vars,
        'total_vars': len(state_vars),
        'non_station_stateful': non_station_stateful
    }


def _resolve_routing_through_non_stations(
    sn: NetworkStruct,
    src_node: int,
    dst_node: int,
    job_class: int,
    rrobin_info: dict,
    state: np.ndarray,
    rr_var_map: dict,
    M: int,
    K: int
) -> Tuple[int, int, np.ndarray]:
    """
    Resolve routing through non-station stateful nodes.

    When a job routes to a non-station node (like Router) with RROBIN,
    this function finds the final station destination and updates the
    RR pointer.

    Args:
        sn: Network structure
        src_node: Source node index
        dst_node: Destination node index (may be non-station)
        job_class: Job class index
        rrobin_info: Round-robin routing info
        state: Current state vector
        rr_var_map: Map from (node, class) to state variable index
        M: Number of stations
        K: Number of classes

    Returns:
        Tuple of (final_node, final_station, updated_state)
        Returns (-1, -1, state) if destination is a sink or invalid
    """
    non_station_stateful = rrobin_info['non_station_stateful']
    outlinks = rrobin_info['outlinks']

    # Get node to station mapping
    node_to_station = None
    if hasattr(sn, 'nodeToStation') and sn.nodeToStation is not None:
        node_to_station = np.asarray(sn.nodeToStation).flatten()

    current_node = dst_node
    new_state = state.copy()
    max_hops = 10  # Prevent infinite loops

    for _ in range(max_hops):
        # Check if current node is a station
        if node_to_station is not None and current_node < len(node_to_station):
            station_idx = int(node_to_station[current_node])
            if station_idx >= 0:
                return current_node, station_idx, new_state

        # Current node is not a station - check if it's a non-station stateful node
        if current_node not in non_station_stateful:
            # Node is neither station nor stateful (e.g., Sink)
            return -1, -1, new_state

        # It's a non-station stateful node - check for RROBIN routing
        if (current_node, job_class) in outlinks:
            # Apply RROBIN routing
            links = outlinks[(current_node, job_class)]
            rr_var_idx = rr_var_map.get((current_node, job_class))
            if rr_var_idx is not None:
                current_rr_ptr = int(new_state[rr_var_idx])
                next_node = links[current_rr_ptr]
                # Advance RR pointer
                new_state[rr_var_idx] = (current_rr_ptr + 1) % len(links)
                current_node = next_node
            else:
                # No RR state variable - use first outlink
                current_node = links[0]
        else:
            # No RROBIN - use connection matrix to find next node
            if hasattr(sn, 'connmatrix') and sn.connmatrix is not None:
                conn = np.asarray(sn.connmatrix)
                next_nodes = np.where(conn[current_node, :] > 0)[0]
                if len(next_nodes) > 0:
                    current_node = next_nodes[0]
                else:
                    return -1, -1, new_state
            else:
                return -1, -1, new_state

    # Max hops exceeded
    return -1, -1, new_state


@dataclass
class SolverCTMCOptions:
    """Options for CTMC solver."""
    method: str = 'default'
    tol: float = 1e-6
    verbose: bool = False
    cutoff: int = 10  # Cutoff for open class populations
    hide_immediate: bool = True  # Hide immediate transitions
    state_space_gen: str = 'default'  # 'default', 'full', 'reachable'


@dataclass
class SolverCTMCReturn:
    """
    Result of CTMC solver handler.

    Attributes:
        Q: Mean queue lengths (M x K)
        U: Utilizations (M x K)
        R: Response times (M x K)
        T: Throughputs (M x K)
        C: Cycle times (1 x K)
        X: System throughputs (1 x K)
        pi: Steady-state distribution
        infgen: Infinitesimal generator matrix
        space: State space matrix
        runtime: Runtime in seconds
        method: Method used
    """
    Q: Optional[np.ndarray] = None
    U: Optional[np.ndarray] = None
    R: Optional[np.ndarray] = None
    T: Optional[np.ndarray] = None
    C: Optional[np.ndarray] = None
    X: Optional[np.ndarray] = None
    pi: Optional[np.ndarray] = None
    infgen: Optional[np.ndarray] = None
    space: Optional[np.ndarray] = None
    runtime: float = 0.0
    method: str = "default"


def _enumerate_state_space(
    sn: NetworkStruct,
    cutoff = 10,
    rrobin_info: Optional[dict] = None,
    use_phase_augmentation: bool = True
) -> Tuple[np.ndarray, np.ndarray, dict]:
    """
    Enumerate the state space for a queueing network.

    For closed networks, enumerates all valid job distributions.
    For open networks, uses cutoff to bound the state space.

    State vector format (without phase augmentation):
    - First M*K elements: job counts at each (station, class) pair
    - Remaining elements: round-robin pointers for state-dependent routing

    State vector format (with phase augmentation):
    - Phase counts for each (station, class): sum(phases[i,k]) elements per station/class
    - Round-robin pointers
    - MAP phase variables for FCFS stations with MAP distributions

    Args:
        sn: Network structure
        cutoff: Maximum jobs per station for open networks.
                Can be an int (same cutoff for all), or a matrix (M x K)
                with per-station, per-class cutoffs.
        rrobin_info: Optional pre-computed round-robin routing info
        use_phase_augmentation: Whether to use phase-augmented state space

    Returns:
        Tuple of (state_space, state_space_aggr, rrobin_info)
    """
    # Get round-robin routing info if not provided
    if rrobin_info is None:
        rrobin_info = _build_rrobin_state_info(sn)
    M = sn.nstations
    K = sn.nclasses
    # Use sn_has_open_classes instead of sn_is_open_model to properly handle
    # mixed networks (which have both open and closed classes)
    is_open = sn_has_open_classes(sn)

    # Get population constraints
    if sn.njobs is not None:
        N = sn.njobs.flatten()
    else:
        N = np.ones(K)

    # Check if model contains Cache nodes - these require reduced cutoff
    # This matches MATLAB's behavior where cache_replc_routing uses cutoff=1
    # Note: Router nodes with RROBIN do NOT require reduced cutoff - they just need state tracking
    has_cache = False
    if hasattr(sn, 'nodetype') and sn.nodetype is not None:
        for nt in sn.nodetype:
            nt_val = int(nt.value) if hasattr(nt, 'value') else int(nt)
            if nt_val == 6:  # CACHE only (not ROUTER)
                has_cache = True
                break

    # For models with Cache nodes, limit cutoff to 1 to prevent state explosion
    # This matches MATLAB's approach in cache_replc_routing.m which uses cutoff=1
    if has_cache and (np.isscalar(cutoff) or np.atleast_2d(cutoff).size == 1):
        effective_cutoff = min(cutoff, 1) if np.isscalar(cutoff) else min(np.atleast_2d(cutoff).flat[0], 1)
        cutoff = effective_cutoff

    # Handle cutoff as scalar or matrix
    cutoff_arr = np.atleast_2d(cutoff)
    is_matrix_cutoff = cutoff_arr.shape[0] > 1 or cutoff_arr.shape[1] > 1

    # Identify Cache stations - these have immediate processing (capacity 1)
    # This matches MATLAB's spaceGeneratorNodes.m behavior
    # Note: Router nodes are not stations - they're pass-through nodes tracked separately
    # Note: We need to map station indices to node indices since nodetype is indexed by node
    cache_stations = set()
    if hasattr(sn, 'nodetype') and sn.nodetype is not None:
        # Get station to node mapping if available
        station_to_node = None
        if hasattr(sn, 'stationToNode') and sn.stationToNode is not None:
            station_to_node = sn.stationToNode

        for ist in range(M):
            # Get the node index for this station
            if station_to_node is not None and ist < len(station_to_node):
                node_idx = int(station_to_node[ist])
            else:
                node_idx = ist  # Fallback: assume station index = node index

            if node_idx >= 0 and node_idx < len(sn.nodetype):
                nt = sn.nodetype[node_idx]
                # NodeType.CACHE = 6
                nt_val = int(nt.value) if hasattr(nt, 'value') else int(nt)
                if nt_val == 6:  # CACHE only
                    cache_stations.add(ist)

    def get_cutoff(ist: int, k: int) -> int:
        """Get cutoff for station ist and class k."""
        # Cache nodes have capacity 1 (immediate processing)
        # This prevents state space explosion in models with Cache nodes
        if ist in cache_stations:
            return 1

        # Determine base cutoff from options
        if is_matrix_cutoff:
            # Matrix cutoff: index by station and class
            # Handle different matrix layouts
            if cutoff_arr.shape[0] >= M and cutoff_arr.shape[1] >= K:
                base_cutoff = int(cutoff_arr[ist, k])
            elif cutoff_arr.shape[0] >= K and cutoff_arr.shape[1] >= M:
                # Transposed: (K x M) layout
                base_cutoff = int(cutoff_arr[k, ist])
            else:
                # Fallback: use first valid value or default
                base_cutoff = int(cutoff_arr.flat[0]) if cutoff_arr.size > 0 else 10
        else:
            base_cutoff = int(cutoff_arr.flat[0])

        # Also check station capacity from sn.cap
        # Capacity limits the maximum number of jobs that can be at the station
        if hasattr(sn, 'cap') and sn.cap is not None and ist < len(sn.cap):
            station_cap = sn.cap[ist]
            if np.isfinite(station_cap) and station_cap > 0:
                # Use the minimum of cutoff and capacity
                return min(base_cutoff, int(station_cap))

        return base_cutoff

    states = []

    # Helper function for closed class distributions
    def _enumerate_distributions(n_jobs: int, n_stations: int) -> List[List[int]]:
        """Enumerate all ways to distribute n_jobs among n_stations."""
        if n_stations == 1:
            return [[n_jobs]]
        if n_jobs == 0:
            return [[0] * n_stations]

        result = []
        for i in range(n_jobs + 1):
            for rest in _enumerate_distributions(n_jobs - i, n_stations - 1):
                result.append([i] + rest)
        return result

    # Determine which classes are open vs closed
    open_classes = [k for k in range(K) if np.isinf(N[k])]
    closed_classes = [k for k in range(K) if np.isfinite(N[k]) and N[k] > 0]

    # Identify Source and Sink stations (closed class jobs should NOT be there)
    source_station = -1
    sink_station = -1
    if hasattr(sn, 'sched') and sn.sched is not None:
        for ist, sched_val in sn.sched.items():
            if sched_val == SchedStrategy.EXT or (isinstance(sched_val, int) and sched_val == 16):
                source_station = ist
    # Also check nodetype for Sink
    if hasattr(sn, 'nodetype') and sn.nodetype is not None:
        for ist in range(M):
            if ist < len(sn.nodetype) and sn.nodetype[ist] == NodeType.SINK:
                sink_station = ist

    # Stations where closed class jobs can reside (exclude Source/Sink)
    closed_valid_stations = [ist for ist in range(M) if ist != source_station and ist != sink_station]
    n_closed_stations = len(closed_valid_stations)

    if is_open and closed_classes:
        # Mixed network: combine closed class distributions with open class enumeration
        # For closed classes: enumerate valid distributions (conserving population)
        #                     only among valid (non-Source/Sink) stations
        # For open classes: enumerate 0 to cutoff at each station (except Source for arrivals)

        # Generate closed class distributions among valid stations only
        closed_class_dists = []
        for k in closed_classes:
            n_k = int(N[k])
            # Distribute among valid stations only
            class_dists = _enumerate_distributions(n_k, n_closed_stations)
            closed_class_dists.append((k, class_dists))

        # Generate open class ranges (per non-Source station for queue occupancy)
        # Open class jobs can be at any station except Source (which generates arrivals)
        open_class_ranges = []
        for k in open_classes:
            station_ranges = []
            for ist in range(M):
                if ist == source_station:
                    # Source doesn't hold jobs - only range is 0
                    station_ranges.append(range(1))  # Just [0]
                else:
                    c = get_cutoff(ist, k)
                    station_ranges.append(range(c + 1))
            open_class_ranges.append((k, station_ranges))

        # Combine: iterate over closed distributions × open combinations
        from itertools import product as iter_product

        # Get all combinations of closed class distributions
        if closed_class_dists:
            closed_combos = list(iter_product(*[dists for _, dists in closed_class_dists]))
        else:
            closed_combos = [()]

        # Get all combinations of open class values at each station
        if open_class_ranges:
            # Flatten: for each open class, product over stations
            open_station_products = []
            for k, station_ranges in open_class_ranges:
                open_station_products.append(list(iter_product(*station_ranges)))
            open_combos = list(iter_product(*open_station_products))
        else:
            open_combos = [()]

        # Build states from combinations
        for closed_combo in closed_combos:
            for open_combo in open_combos:
                # Build state vector: [n_11, n_12, ..., n_1K, n_21, ..., n_MK]
                state = [0] * (M * K)
                # Fill in closed classes (mapping from valid station indices to full indices)
                for idx, (k, _) in enumerate(closed_class_dists):
                    dist = closed_combo[idx]
                    for valid_idx, ist in enumerate(closed_valid_stations):
                        state[ist * K + k] = dist[valid_idx]
                # Fill in open classes
                for idx, (k, _) in enumerate(open_class_ranges):
                    station_vals = open_combo[idx]
                    for ist in range(M):
                        state[ist * K + k] = station_vals[ist]
                states.append(state)

    elif is_open:
        # Pure open network: enumerate all valid job distributions
        # State has M*K dimensions: jobs at each (station, class) pair
        # Must respect station capacity: sum of jobs across all classes <= capacity

        def _enumerate_station_states(ist: int, nclasses: int) -> List[List[int]]:
            """Enumerate valid job distributions at a station respecting capacity."""
            # Get per-class cutoffs
            class_cutoffs = [get_cutoff(ist, k) for k in range(nclasses)]

            # Get station capacity (total jobs limit)
            station_cap = float('inf')
            if hasattr(sn, 'cap') and sn.cap is not None and ist < len(sn.cap):
                cap_val = sn.cap[ist]
                if np.isfinite(cap_val) and cap_val > 0:
                    station_cap = int(cap_val)

            # If no capacity limit, use Cartesian product of class ranges
            if station_cap == float('inf'):
                ranges = [range(c + 1) for c in class_cutoffs]
                return [list(combo) for combo in product(*ranges)]

            # With capacity limit, enumerate valid distributions where total <= capacity
            valid_states = []

            def _enumerate_with_budget(class_idx: int, remaining: int, current: List[int]):
                """Recursively enumerate distributions with remaining budget."""
                if class_idx == nclasses:
                    valid_states.append(current[:])
                    return

                # Max jobs for this class is min(cutoff, remaining budget)
                max_jobs = min(class_cutoffs[class_idx], remaining)
                for n in range(max_jobs + 1):
                    current.append(n)
                    _enumerate_with_budget(class_idx + 1, remaining - n, current)
                    current.pop()

            _enumerate_with_budget(0, station_cap, [])
            return valid_states

        # Enumerate states for each station
        station_states_list = []
        for ist in range(M):
            station_states = _enumerate_station_states(ist, K)
            station_states_list.append(station_states)

        # Combine across stations
        for combo in product(*station_states_list):
            # combo is tuple of (station states), each station state is list of K values
            state = []
            for ist_state in combo:
                state.extend(ist_state)
            states.append(state)
    else:
        # Pure closed network: enumerate valid distributions
        # Check for class switching (chains) - classes in the same chain can exchange jobs
        has_chains = (hasattr(sn, 'chains') and sn.chains is not None and
                      hasattr(sn, 'inchain') and sn.inchain is not None and
                      hasattr(sn, 'nchains') and sn.nchains is not None)

        # Determine if class switching exists (some chain has multiple classes)
        has_class_switching = False
        if has_chains and sn.nchains < K:
            for chain_id in range(sn.nchains):
                if chain_id in sn.inchain and len(sn.inchain[chain_id]) > 1:
                    has_class_switching = True
                    break

        if has_class_switching:
            # Class switching exists - enumerate based on chain populations
            # For each chain, enumerate all ways to distribute the chain population
            # across (station, class) pairs within the chain
            all_chain_dists = []

            for chain_id in range(sn.nchains):
                if chain_id not in sn.inchain:
                    continue
                chain_classes = list(sn.inchain[chain_id])  # Array of class indices in this chain

                # Chain population = sum of N[k] for all k in chain
                chain_pop = sum(int(N[k]) for k in chain_classes if np.isfinite(N[k]))

                if chain_pop == 0:
                    # No jobs in this chain - single empty distribution
                    n_pairs = M * len(chain_classes)
                    chain_dists = [[0] * n_pairs]
                else:
                    # Number of (station, class) pairs in this chain
                    n_pairs = M * len(chain_classes)

                    # Enumerate all ways to distribute chain_pop among n_pairs
                    chain_dists = _enumerate_distributions(chain_pop, n_pairs)

                all_chain_dists.append((chain_id, chain_classes, chain_dists))

            # Combine distributions across chains
            for combo in product(*[dists for _, _, dists in all_chain_dists]):
                state = [0] * (M * K)
                for idx, (chain_id, chain_classes, _) in enumerate(all_chain_dists):
                    dist = combo[idx]
                    # Map distribution back to (station, class) pairs
                    # The distribution is ordered by station first, then by class within chain
                    pair_idx = 0
                    for ist in range(M):
                        for k in chain_classes:
                            state[ist * K + k] = dist[pair_idx]
                            pair_idx += 1
                states.append(state)
        else:
            # No class switching - original per-class enumeration
            all_class_dists = []
            for k in range(K):
                n_k = int(N[k]) if np.isfinite(N[k]) else 0
                class_dists = _enumerate_distributions(n_k, M)
                all_class_dists.append(class_dists)

            # Combine all class distributions
            for combo in product(*all_class_dists):
                # combo is tuple of distributions, one per class
                # Convert to state vector: [n_11, n_12, ..., n_1K, n_21, ..., n_MK]
                state = []
                for ist in range(M):
                    for k in range(K):
                        state.append(combo[k][ist])
                states.append(state)

    if not states:
        states = [[0] * (M * K)]

    # Filter states to respect station capacity constraints
    # For each station, sum of jobs across all classes must be <= capacity
    if hasattr(sn, 'cap') and sn.cap is not None:
        filtered_states = []
        for state in states:
            valid = True
            for ist in range(M):
                if ist < len(sn.cap):
                    cap_val = sn.cap[ist]
                    if np.isfinite(cap_val) and cap_val > 0:
                        # Sum jobs at this station across all classes
                        total_at_station = sum(state[ist * K + k] for k in range(K))
                        if total_at_station > cap_val:
                            valid = False
                            break
            if valid:
                filtered_states.append(state)
        states = filtered_states if filtered_states else [[0] * (M * K)]

    # Get phase information for phase-type state augmentation
    phases, needs_phase_augmentation = _get_phases_info(sn)

    # Compute phase-related state offsets for later use
    # phase_offset[ist, k] = starting index of phases for (ist, k) in phase-augmented state
    total_phases = int(np.sum(phases))
    phase_offset = np.zeros((M, K), dtype=int)
    idx = 0
    for ist in range(M):
        for k in range(K):
            phase_offset[ist, k] = idx
            idx += phases[ist, k]

    # Store phase information in rrobin_info for use by generator
    rrobin_info['phases'] = phases
    rrobin_info['phase_offset'] = phase_offset
    rrobin_info['total_phases'] = total_phases
    rrobin_info['needs_phase_augmentation'] = needs_phase_augmentation and use_phase_augmentation

    # If phase augmentation is needed and enabled, expand states with phase distributions
    if needs_phase_augmentation and use_phase_augmentation:
        # For each basic state (job counts), expand to all possible phase distributions
        phase_augmented_states = []

        for base_state in states:
            # base_state has format [n_11, n_12, ..., n_1K, n_21, ..., n_MK]
            # We need to expand each n_ik into phase distribution

            # Generate all phase distribution combinations
            phase_combos_per_station_class = []
            for ist in range(M):
                for k in range(K):
                    n_ik = int(base_state[ist * K + k])
                    n_phases = phases[ist, k]

                    if n_phases > 1:
                        # Generate all ways to distribute n_ik jobs across n_phases phases
                        phase_dists = _generate_phase_distributions(n_ik, n_phases)
                    else:
                        # Single phase: just the job count
                        phase_dists = [(n_ik,)]

                    phase_combos_per_station_class.append(phase_dists)

            # Cartesian product of all phase distributions
            for combo in product(*phase_combos_per_station_class):
                # combo is tuple of phase distributions, one per (station, class)
                # Flatten to create the phase-augmented state
                phase_state = []
                for phase_dist in combo:
                    phase_state.extend(phase_dist)
                phase_augmented_states.append(phase_state)

        states = phase_augmented_states
        state_dim = total_phases
    else:
        # No phase augmentation - use simple job counts
        state_dim = M * K

    rrobin_info['state_dim'] = state_dim

    # Get MAP FCFS information for additional state variables
    map_fcfs, has_map_fcfs = _get_map_fcfs_info(sn)
    rrobin_info['map_fcfs'] = map_fcfs
    rrobin_info['has_map_fcfs'] = has_map_fcfs

    # Augment states with MAP phase variables for FCFS stations with MAP distributions
    # The MAP phase tracks the "mode" of the MAP process (separate from service phase counts)
    if has_map_fcfs:
        map_augmented_states = []
        # Sort the map_fcfs keys for consistent ordering
        map_fcfs_keys = sorted(map_fcfs.keys())
        rrobin_info['map_fcfs_keys'] = map_fcfs_keys

        # Create map offset mapping: position in state vector where each MAP phase var starts
        map_var_offset = {}
        offset = state_dim  # MAP vars start after the job count variables
        for (ist, k) in map_fcfs_keys:
            map_var_offset[(ist, k)] = offset
            offset += 1  # Each MAP phase is a single integer (the current phase)
        rrobin_info['map_var_offset'] = map_var_offset
        rrobin_info['map_var_count'] = len(map_fcfs_keys)

        # Generate all possible MAP phase combinations
        map_ranges = []
        for (ist, k) in map_fcfs_keys:
            n_phases = map_fcfs[(ist, k)]
            # MAP phase can be any of 0 to n_phases-1
            map_ranges.append(range(n_phases))

        # Expand each base state with all possible MAP phase combinations
        for base_state in states:
            for map_combo in product(*map_ranges):
                augmented_state = list(base_state) + list(map_combo)
                map_augmented_states.append(augmented_state)

        states = map_augmented_states
        # Note: state_dim stays the same - it's only the job count variables
        # MAP phase variables are stored separately after state_dim
    else:
        rrobin_info['map_fcfs_keys'] = []
        rrobin_info['map_var_offset'] = {}
        rrobin_info['map_var_count'] = 0

    # Augment states with round-robin pointers if there are RROBIN routing nodes
    # Each RROBIN (node, class) adds a state variable that tracks which outlink
    # the round-robin pointer is pointing to
    if rrobin_info['total_vars'] > 0:
        augmented_states = []
        # Get all possible round-robin pointer combinations
        rr_ranges = []
        for node_idx, class_idx, num_outlinks in rrobin_info['state_vars']:
            # Each pointer can be any of the outlinks (0 to num_outlinks-1)
            rr_ranges.append(range(num_outlinks))

        # Expand each base state with all possible RR pointer combinations
        for base_state in states:
            for rr_combo in product(*rr_ranges):
                augmented_state = list(base_state) + list(rr_combo)
                augmented_states.append(augmented_state)
        states = augmented_states

    state_space = np.array(states, dtype=np.float64)

    # Aggregated state space: sum over classes at each station (exclude RR pointers)
    # For phase-augmented states, we sum over phases to get job counts
    state_space_aggr = np.zeros((len(states), M))
    for i, state in enumerate(states):
        for ist in range(M):
            for k in range(K):
                if needs_phase_augmentation and use_phase_augmentation:
                    # Sum over phases for this (station, class)
                    start_idx = phase_offset[ist, k]
                    end_idx = start_idx + phases[ist, k]
                    state_space_aggr[i, ist] += sum(state[start_idx:end_idx])
                else:
                    state_space_aggr[i, ist] += state[ist * K + k]

    return state_space, state_space_aggr, rrobin_info


def _build_state_index_map(state_space: np.ndarray) -> dict:
    """
    Build a hash map from state tuples to indices for O(1) lookup.

    Args:
        state_space: Enumerated state space (n_states x state_dim)

    Returns:
        Dictionary mapping state tuples to their indices
    """
    state_map = {}
    for i, state in enumerate(state_space):
        # Convert to tuple of integers for hashing
        state_key = tuple(int(x) for x in state)
        state_map[state_key] = i
    return state_map


def _find_state_index_fast(state_map: dict, state: np.ndarray) -> int:
    """
    Find index of state using hash map (O(1) lookup).

    Args:
        state_map: Hash map from state tuples to indices
        state: State vector to find

    Returns:
        Index of state, or -1 if not found
    """
    state_key = tuple(int(x) for x in state)
    return state_map.get(state_key, -1)


def _build_generator(
    sn: NetworkStruct,
    state_space: np.ndarray,
    options: SolverCTMCOptions,
    rrobin_info: Optional[dict] = None
) -> np.ndarray:
    """
    Build the infinitesimal generator matrix for the queueing network.

    Supports state-dependent routing (RROBIN, WRROBIN) by using routing state
    variables in the state vector to determine destinations.

    Also supports phase-type distributions (PH, APH, MAP, etc.) when phase
    augmentation is enabled in rrobin_info.

    Args:
        sn: Network structure
        state_space: Enumerated state space
        options: Solver options
        rrobin_info: Round-robin routing information (also contains phase info)

    Returns:
        Infinitesimal generator matrix Q
    """
    M = sn.nstations
    K = sn.nclasses
    n_states = state_space.shape[0]

    Q = np.zeros((n_states, n_states))

    # Get round-robin info if not provided
    if rrobin_info is None:
        rrobin_info = _build_rrobin_state_info(sn)

    # Check if phase augmentation is used
    use_phase_aug = rrobin_info.get('needs_phase_augmentation', False)
    phases = rrobin_info.get('phases', np.ones((M, K), dtype=int))
    phase_offset = rrobin_info.get('phase_offset', None)
    state_dim = rrobin_info.get('state_dim', M * K)

    # Get MAP FCFS info
    map_fcfs = rrobin_info.get('map_fcfs', {})
    has_map_fcfs = rrobin_info.get('has_map_fcfs', False)
    map_var_offset = rrobin_info.get('map_var_offset', {})
    map_var_count = rrobin_info.get('map_var_count', 0)

    # Build mapping from (node_idx, class_idx) to state variable index
    # RR pointers come after state variables AND MAP phase variables
    rr_state_offset = state_dim + map_var_count  # RR pointers start after MAP vars
    rr_var_map = {}  # Maps (node_idx, class_idx) -> index in state vector
    for i, (node_idx, class_idx, _) in enumerate(rrobin_info['state_vars']):
        rr_var_map[(node_idx, class_idx)] = rr_state_offset + i

    def get_map_matrices(ist: int, k: int) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """Get MAP D0 and D1 matrices for (station, class)."""
        if not hasattr(sn, 'proc') or sn.proc is None:
            return None, None
        proc_is_list = isinstance(sn.proc, list)
        if proc_is_list:
            if ist >= len(sn.proc) or sn.proc[ist] is None:
                return None, None
            station_proc = sn.proc[ist]
        else:
            if ist not in sn.proc:
                return None, None
            station_proc = sn.proc[ist]

        proc_entry = None
        if isinstance(station_proc, (list, tuple)):
            if k < len(station_proc):
                proc_entry = station_proc[k]
        elif isinstance(station_proc, dict):
            proc_entry = station_proc.get(k)

        if proc_entry is None:
            return None, None

        # Handle direct D0/D1 matrices
        if isinstance(proc_entry, (list, tuple)) and len(proc_entry) >= 2:
            D0 = np.atleast_2d(np.array(proc_entry[0], dtype=float))
            D1 = np.atleast_2d(np.array(proc_entry[1], dtype=float))
            return D0, D1

        # Handle Erlang distribution stored as dict with 'k' and 'mu'
        if isinstance(proc_entry, dict):
            if 'k' in proc_entry and 'mu' in proc_entry:
                n_phases = int(proc_entry['k'])
                mu = float(proc_entry['mu'])  # per-phase rate
                if n_phases > 1:
                    # Construct Erlang D0/D1 matrices
                    # D0: diagonal = -mu (absorption), off-diagonal D0[i,i+1] = mu (phase transition)
                    # D1: D1[k-1,0] = mu (completion from last phase)
                    D0 = np.zeros((n_phases, n_phases))
                    D1 = np.zeros((n_phases, n_phases))
                    for p in range(n_phases):
                        D0[p, p] = -mu
                        if p < n_phases - 1:
                            D0[p, p + 1] = mu  # phase transition
                    D1[n_phases - 1, 0] = mu  # completion from last phase
                    return D0, D1
                else:
                    # Single phase: exponential
                    D0 = np.array([[-mu]])
                    D1 = np.array([[mu]])
                    return D0, D1
            elif 'probs' in proc_entry and 'rates' in proc_entry:
                # HyperExp distribution: each phase completes independently
                probs = np.array(proc_entry['probs'])
                rates = np.array(proc_entry['rates'])
                n_phases = len(rates)
                # D0: diagonal with -rate_i (no inter-phase transitions in HyperExp)
                D0 = np.diag(-rates)
                # D1: completion from phase i, restart in phase j with prob_j
                # D1[i,j] = rate_i * prob_j
                D1 = np.outer(rates, probs)
                return D0, D1
            elif 'rate' in proc_entry:
                # Exponential distribution
                mu = float(proc_entry['rate'])
                D0 = np.array([[-mu]])
                D1 = np.array([[mu]])
                return D0, D1

        return None, None

    def get_map_phase(state: np.ndarray, ist: int, k: int) -> int:
        """Get current MAP phase for (station, class) from state vector."""
        if (ist, k) not in map_var_offset:
            return 0
        idx = map_var_offset[(ist, k)]
        return int(state[idx])

    def set_map_phase(state: np.ndarray, ist: int, k: int, phase: int) -> np.ndarray:
        """Set MAP phase for (station, class) in state vector."""
        new_state = state.copy()
        if (ist, k) in map_var_offset:
            idx = map_var_offset[(ist, k)]
            new_state[idx] = phase
        return new_state

    def get_job_count(state: np.ndarray, ist: int, k: int) -> int:
        """Get total job count for (station, class) from state vector."""
        if use_phase_aug and phase_offset is not None:
            start_idx = phase_offset[ist, k]
            end_idx = start_idx + phases[ist, k]
            return int(sum(state[start_idx:end_idx]))
        else:
            return int(state[ist * K + k])

    def get_phase_counts(state: np.ndarray, ist: int, k: int) -> np.ndarray:
        """Get phase counts for (station, class) from state vector."""
        if use_phase_aug and phase_offset is not None:
            start_idx = phase_offset[ist, k]
            end_idx = start_idx + phases[ist, k]
            return np.array([int(x) for x in state[start_idx:end_idx]])
        else:
            # Single phase
            return np.array([int(state[ist * K + k])])

    def set_job_count(state: np.ndarray, ist: int, k: int, delta: int, phase_idx: int = -1) -> np.ndarray:
        """
        Modify job count for (station, class) in state vector.

        Args:
            state: Current state vector
            ist: Station index
            k: Class index
            delta: Change in job count (+1 for arrival, -1 for departure)
            phase_idx: Phase index to modify. If -1:
                       - For arrivals (delta > 0): use first phase (phase 0)
                       - For departures (delta < 0): find first phase with jobs

        Returns:
            New state vector with modified job count
        """
        new_state = state.copy()
        if use_phase_aug and phase_offset is not None:
            if phase_idx < 0:
                # Auto-select phase
                start_idx = phase_offset[ist, k]
                n_phases = phases[ist, k]
                if delta > 0:
                    # Arrival: add to first phase
                    phase_idx = 0
                else:
                    # Departure: find first phase with jobs
                    for p in range(n_phases):
                        if new_state[start_idx + p] > 0:
                            phase_idx = p
                            break
                    else:
                        # No jobs found - use first phase (will create invalid state)
                        phase_idx = 0
            idx = phase_offset[ist, k] + phase_idx
            new_state[idx] += delta
        else:
            new_state[ist * K + k] += delta
        return new_state

    def get_entry_probs(ist: int, k: int) -> np.ndarray:
        """
        Get entry probabilities for (station, class).

        For HyperExp: returns probs array (distributed across phases)
        For Erlang: returns [1, 0, 0, ...] (always start in phase 0)
        For Exp: returns [1.0]
        """
        if not use_phase_aug or phase_offset is None:
            return np.array([1.0])

        n_phases = phases[ist, k]
        if n_phases <= 1:
            return np.array([1.0])

        # Get proc entry for this (station, class)
        if not hasattr(sn, 'proc') or sn.proc is None:
            return np.array([1.0] + [0.0] * (n_phases - 1))

        proc_is_list = isinstance(sn.proc, list)
        if proc_is_list:
            if ist >= len(sn.proc) or sn.proc[ist] is None:
                return np.array([1.0] + [0.0] * (n_phases - 1))
            station_proc = sn.proc[ist]
        else:
            if ist not in sn.proc:
                return np.array([1.0] + [0.0] * (n_phases - 1))
            station_proc = sn.proc[ist]

        proc_entry = None
        if isinstance(station_proc, (list, tuple)):
            if k < len(station_proc):
                proc_entry = station_proc[k]
        elif isinstance(station_proc, dict):
            proc_entry = station_proc.get(k)

        if proc_entry is None:
            return np.array([1.0] + [0.0] * (n_phases - 1))

        if isinstance(proc_entry, dict):
            if 'probs' in proc_entry and 'rates' in proc_entry:
                # HyperExp: entry probability = probs
                return np.array(proc_entry['probs'])
            elif 'k' in proc_entry:
                # Erlang: always enter phase 0
                return np.array([1.0] + [0.0] * (n_phases - 1))
            else:
                # Exp: single phase
                return np.array([1.0])

        # For MAP/PH with D0/D1 matrices, use uniform entry (simplified)
        # TODO: Extract proper entry probabilities from PH representation
        return np.array([1.0] + [0.0] * (n_phases - 1))

    def get_state_matrix(state: np.ndarray) -> np.ndarray:
        """Get job counts as (M, K) matrix from state vector."""
        result = np.zeros((M, K))
        for ist in range(M):
            for k in range(K):
                result[ist, k] = get_job_count(state, ist, k)
        return result

    # Get station to node mapping
    station_to_node = None
    if hasattr(sn, 'stationToNode') and sn.stationToNode is not None:
        station_to_node = np.asarray(sn.stationToNode).flatten()

    # Get node to station mapping
    node_to_station = None
    if hasattr(sn, 'nodeToStation') and sn.nodeToStation is not None:
        node_to_station = np.asarray(sn.nodeToStation).flatten()

    # Handle cutoff as scalar or matrix for state validation
    cutoff = options.cutoff
    cutoff_arr = np.atleast_2d(cutoff)
    is_matrix_cutoff = cutoff_arr.shape[0] > 1 or cutoff_arr.shape[1] > 1

    def is_within_cutoff(new_state: np.ndarray) -> bool:
        """Check if state is within cutoff bounds."""
        if is_matrix_cutoff:
            # Reshape state to (M, K) and compare with cutoff matrix
            state_matrix = new_state.reshape(M, K)
            # Handle different cutoff matrix layouts
            if cutoff_arr.shape[0] >= M and cutoff_arr.shape[1] >= K:
                return np.all(state_matrix <= cutoff_arr[:M, :K])
            elif cutoff_arr.shape[0] >= K and cutoff_arr.shape[1] >= M:
                return np.all(state_matrix <= cutoff_arr[:K, :M].T)
            else:
                # Fallback: use scalar comparison
                return np.all(new_state <= cutoff_arr.flat[0])
        else:
            return np.all(new_state <= cutoff_arr.flat[0])

    # Build hash map for O(1) state lookup instead of O(n) linear search
    state_map = _build_state_index_map(state_space)

    # Get service rates
    if hasattr(sn, 'rates') and sn.rates is not None:
        rates = np.asarray(sn.rates)
    else:
        rates = np.ones((M, K))

    # Get routing probabilities
    if hasattr(sn, 'rt') and sn.rt is not None:
        P = np.asarray(sn.rt)
    else:
        # Default: uniform routing
        P = np.ones((M * K, M * K)) / (M * K)

    # Get number of servers
    if hasattr(sn, 'nservers') and sn.nservers is not None:
        nservers = np.asarray(sn.nservers).flatten()
    else:
        nservers = np.ones(M)

    # Get load-dependent scaling
    lldscaling = None
    if hasattr(sn, 'lldscaling') and sn.lldscaling is not None:
        lldscaling = np.asarray(sn.lldscaling)

    # Track which stations are infinite servers
    inf_server_stations = set()
    if hasattr(sn, 'sched') and sn.sched is not None:
        for ist, sched_val in sn.sched.items():
            if sched_val == SchedStrategy.INF:
                inf_server_stations.add(ist)

    def get_load_scaling(ist: int, total_jobs: int) -> float:
        """Get service rate scaling factor for station ist with total_jobs present."""
        if total_jobs <= 0:
            return 0.0  # No jobs, no service
        # For infinite servers, each job gets its own server
        if ist in inf_server_stations:
            return float(total_jobs)
        if lldscaling is not None and ist < lldscaling.shape[0]:
            # lldscaling[ist, n-1] gives scaling when n jobs present
            idx = total_jobs - 1
            if lldscaling.ndim > 1 and idx < lldscaling.shape[1]:
                return lldscaling[ist, idx]
            elif lldscaling.ndim > 1:
                return lldscaling[ist, -1]  # Use last value if beyond range
        # Fall back to min(n, c) behavior
        c = nservers[ist] if ist < len(nservers) else 1
        return min(total_jobs, c)

    # Identify Source station (EXT scheduling) for open network arrivals
    # Use sn_has_open_classes to properly handle mixed networks
    is_open = sn_has_open_classes(sn)
    source_station = -1
    if is_open and hasattr(sn, 'sched'):
        for ist, sched_val in sn.sched.items():
            # Check for EXT scheduling (Source station)
            if sched_val == SchedStrategy.EXT or (isinstance(sched_val, int) and sched_val == 11):
                source_station = ist
                break

    # Build transitions
    for s, state in enumerate(state_space):
        # Get job counts as (M, K) matrix from state vector
        state_matrix = get_state_matrix(state)

        # === External arrivals from Source ===
        # For open networks, Source generates arrivals that enter the next station
        # Handle routing through non-station nodes (like Router with RROBIN)
        if source_station >= 0:
            source_node = int(station_to_node[source_station]) if station_to_node is not None and source_station < len(station_to_node) else source_station

            for k in range(K):
                # Arrival rate at source
                arrival_rate = rates[source_station, k] if source_station < rates.shape[0] and k < rates.shape[1] else 0

                if arrival_rate <= 0:
                    continue

                # Get direct destinations from connection matrix
                conn = np.asarray(sn.connmatrix) if hasattr(sn, 'connmatrix') and sn.connmatrix is not None else None
                if conn is not None:
                    direct_dests = np.where(conn[source_node, :] > 0)[0]
                else:
                    direct_dests = []

                for dest_node in direct_dests:
                    # Resolve routing through non-station nodes
                    final_node, final_station, new_state = _resolve_routing_through_non_stations(
                        sn, source_node, dest_node, k, rrobin_info, state, rr_var_map, M, K
                    )

                    if final_station >= 0 and final_station < M and final_station != source_station:
                        # Arrival to final station, same class (no class switching at Router)
                        # Get entry probabilities for destination
                        entry_probs = get_entry_probs(final_station, k)
                        for entry_phase, entry_prob in enumerate(entry_probs):
                            if entry_prob <= 0:
                                continue
                            # Use phase-aware state modification with entry phase
                            arrival_state = set_job_count(new_state, final_station, k, +1, phase_idx=entry_phase)

                            # Check if within cutoff (only for open networks)
                            ns = _find_state_index_fast(state_map, arrival_state)
                            if ns >= 0:
                                # Probability is 1/num_direct_dests if no RROBIN at source
                                # (RROBIN state already handled in resolve function)
                                p = 1.0 / len(direct_dests) if len(direct_dests) > 1 else 1.0
                                Q[s, ns] += arrival_rate * p * entry_prob
                    elif final_station == -1:
                        # Destination is Sink - this shouldn't happen for arrivals
                        pass

        # === MAP phase transitions (D0 off-diagonal, no service completion) ===
        # These are transitions within the MAP process that don't complete service
        if has_map_fcfs:
            for (ist, k) in map_fcfs.keys():
                n_ik = state_matrix[ist, k]
                if n_ik <= 0:
                    continue  # No jobs, no MAP transitions

                D0, D1 = get_map_matrices(ist, k)
                if D0 is None:
                    continue

                current_map_phase = get_map_phase(state, ist, k)
                n_phases = D0.shape[0]

                # For multi-class FCFS: scale by probability this class is in service
                total_jobs = np.sum(state_matrix[ist, :])
                class_fraction = (n_ik / total_jobs) if total_jobs > 0 else 0
                scaling_d0 = get_load_scaling(ist, int(total_jobs)) if total_jobs > 0 else 0

                # D0 off-diagonal entries: phase transitions without completion
                # Scaled for multi-class approximation
                for j in range(n_phases):
                    if j == current_map_phase:
                        continue  # Skip diagonal
                    rate = D0[current_map_phase, j] * scaling_d0 * class_fraction
                    if rate <= 0:
                        continue

                    # Create new state with updated MAP phase (no job movement)
                    new_state = set_map_phase(state, ist, k, j)

                    ns = _find_state_index_fast(state_map, new_state)
                    if ns >= 0:
                        Q[s, ns] += rate

        # === Service completions and internal routing ===
        for ist in range(M):
            # Skip source station - it doesn't hold jobs for service
            if ist == source_station:
                continue

            for k in range(K):
                n_ik = state_matrix[ist, k]
                if n_ik <= 0:
                    continue

                # Service completion at station ist, class k
                # Rate depends on scheduling discipline
                if hasattr(sn, 'sched') and sn.sched is not None:
                    sched = sn.sched.get(ist, SchedStrategy.FCFS)
                else:
                    sched = SchedStrategy.FCFS

                # Check if this is a MAP distribution at FCFS station
                is_map_fcfs_class = (ist, k) in map_fcfs
                mu = rates[ist, k] if ist < rates.shape[0] and k < rates.shape[1] else 1.0

                if sched == SchedStrategy.INF:
                    # Infinite server: rate depends on phase-type distribution
                    n_phases_ik = phases[ist, k]
                    if use_phase_aug and n_phases_ik > 1:
                        # Phase-type distribution: need separate transitions for each completing phase
                        D0, D1 = get_map_matrices(ist, k)
                        if D0 is not None and D1 is not None:
                            phase_counts = get_phase_counts(state, ist, k)
                            # For each phase with completions, create separate routing transitions
                            for p in range(n_phases_ik):
                                n_p = int(phase_counts[p])
                                if n_p <= 0:
                                    continue
                                completion_rate_p = np.sum(D1[p, :])
                                if completion_rate_p <= 0:
                                    continue
                                # Rate for completions from this phase
                                rate_p = n_p * completion_rate_p
                                # Create transitions for each destination
                                src_idx = ist * K + k
                                for jst in range(M):
                                    if jst == source_station:
                                        continue
                                    for r in range(K):
                                        dst_idx = jst * K + r
                                        if src_idx < P.shape[0] and dst_idx < P.shape[1]:
                                            prob = P[src_idx, dst_idx]
                                        else:
                                            prob = 0
                                        if prob <= 0:
                                            continue
                                        # Get entry probabilities for destination
                                        entry_probs = get_entry_probs(jst, r)
                                        for entry_phase, entry_prob in enumerate(entry_probs):
                                            if entry_prob <= 0:
                                                continue
                                            # Create new state: remove from phase p, add to destination entry phase
                                            new_state = state.copy()
                                            start_idx = phase_offset[ist, k]
                                            new_state[start_idx + p] -= 1  # Remove from completing phase
                                            new_state = set_job_count(new_state, jst, r, +1, phase_idx=entry_phase)
                                            if np.any(new_state[:state_dim] < 0):
                                                continue
                                            ns = _find_state_index_fast(state_map, new_state)
                                            if ns >= 0:
                                                Q[s, ns] += rate_p * prob * entry_prob
                            # Skip the normal routing below since we handled it here
                            continue
                        else:
                            # Fallback to aggregate rate
                            rate = n_ik * mu
                    else:
                        # Single phase (exponential): rate = n * mu
                        rate = n_ik * mu
                elif sched == SchedStrategy.DPS:
                    # Discriminatory Processor Sharing: weighted by schedparam
                    total_jobs = np.sum(state_matrix[ist, :])
                    if total_jobs > 0:
                        # Get weight for this class (default 1.0)
                        w_k = 1.0
                        if hasattr(sn, 'schedparam') and sn.schedparam is not None:
                            if ist < sn.schedparam.shape[0] and k < sn.schedparam.shape[1]:
                                w_k = sn.schedparam[ist, k]
                        # Compute weighted share: sum of w_j * n_j for all classes
                        weighted_total = 0.0
                        for kk in range(K):
                            n_kk = state_matrix[ist, kk]
                            w_kk = 1.0
                            if hasattr(sn, 'schedparam') and sn.schedparam is not None:
                                if ist < sn.schedparam.shape[0] and kk < sn.schedparam.shape[1]:
                                    w_kk = sn.schedparam[ist, kk]
                            weighted_total += w_kk * n_kk
                        # Rate = (w_k * n_k / weighted_total) * scaling * mu
                        scaling = get_load_scaling(ist, int(total_jobs))
                        if weighted_total > 0:
                            rate = (w_k * n_ik / weighted_total) * scaling * mu
                        else:
                            rate = 0
                    else:
                        rate = 0
                elif sched == SchedStrategy.PSPRIO:
                    # PS with Priority: only jobs at highest priority level get service
                    total_jobs = np.sum(state_matrix[ist, :])
                    if total_jobs <= 0:
                        rate = 0
                    else:
                        scaling = get_load_scaling(ist, int(total_jobs))
                        nservers_ist = nservers[ist] if ist < len(nservers) else 1

                        # Get class priorities (lower value = higher priority)
                        classprio = None
                        if hasattr(sn, 'classprio') and sn.classprio is not None:
                            classprio = np.asarray(sn.classprio).flatten()

                        if classprio is None or total_jobs <= nservers_ist:
                            # No priorities or all jobs get service: regular PS
                            rate = scaling * mu * (n_ik / total_jobs)
                        else:
                            # Find minimum priority value among classes with jobs present
                            present_classes = [kk for kk in range(K) if state_matrix[ist, kk] > 0]
                            min_prio = min(classprio[kk] for kk in present_classes)

                            if classprio[k] == min_prio:
                                # This class is at highest priority - gets PS among same priority
                                niprio = sum(state_matrix[ist, kk] for kk in range(K)
                                           if classprio[kk] == min_prio)
                                scaling_prio = min(niprio, nservers_ist)
                                rate = scaling_prio * mu * (n_ik / niprio)
                            else:
                                # Not highest priority: rate = 0
                                rate = 0

                elif sched == SchedStrategy.GPSPRIO:
                    # GPS with Priority: weighted sharing among highest priority jobs
                    total_jobs = np.sum(state_matrix[ist, :])
                    if total_jobs <= 0:
                        rate = 0
                    else:
                        nservers_ist = nservers[ist] if ist < len(nservers) else 1

                        # Get class priorities
                        classprio = None
                        if hasattr(sn, 'classprio') and sn.classprio is not None:
                            classprio = np.asarray(sn.classprio).flatten()

                        # Get weights from schedparam
                        weights = np.ones(K)
                        if hasattr(sn, 'schedparam') and sn.schedparam is not None:
                            if ist < sn.schedparam.shape[0]:
                                weights = sn.schedparam[ist, :K].flatten()
                        weights = weights / np.sum(weights)  # Normalize

                        if classprio is None or total_jobs <= nservers_ist:
                            # No priorities or all jobs get service: regular GPS
                            # cir = min(nir, 1) - indicator of presence
                            cir = np.minimum(state_matrix[ist, :], 1)
                            weighted_total = np.sum(weights * cir)
                            if weighted_total > 0:
                                rate = mu * (n_ik / state_matrix[ist, k]) * weights[k] / weighted_total if state_matrix[ist, k] > 0 else 0
                            else:
                                rate = 0
                        else:
                            # Find minimum priority value among classes with jobs present
                            present_classes = [kk for kk in range(K) if state_matrix[ist, kk] > 0]
                            min_prio = min(classprio[kk] for kk in present_classes)

                            if classprio[k] == min_prio:
                                # This class is at highest priority - GPS among same priority
                                nirprio = np.zeros(K)
                                for kk in range(K):
                                    if classprio[kk] == min_prio:
                                        nirprio[kk] = state_matrix[ist, kk]

                                cir = np.minimum(nirprio, 1)
                                weighted_total = np.sum(weights * cir)
                                if weighted_total > 0 and nirprio[k] > 0:
                                    rate = mu * (n_ik / nirprio[k]) * weights[k] / weighted_total
                                else:
                                    rate = 0
                            else:
                                # Not highest priority: rate = 0
                                rate = 0
                else:
                    # FCFS, PS, etc.: rate = scaling * mu
                    total_jobs = np.sum(state_matrix[ist, :])
                    scaling = get_load_scaling(ist, int(total_jobs))
                    rate = scaling * mu * (n_ik / total_jobs) if total_jobs > 0 else 0

                # === Special handling for MAP distributions at FCFS stations ===
                # For MAP, service completions use D1 matrix with phase-dependent rates
                if is_map_fcfs_class:
                    D0, D1 = get_map_matrices(ist, k)
                    if D0 is not None and D1 is not None:
                        current_map_phase = get_map_phase(state, ist, k)
                        n_phases = D1.shape[0]

                        # For multi-class FCFS: scale by probability this class is in service
                        # In FCFS with single server, the job at queue head is served
                        # Without tracking queue order, we approximate by n_k / total_jobs
                        total_jobs = np.sum(state_matrix[ist, :])
                        scaling = get_load_scaling(ist, int(total_jobs))
                        class_fraction = (n_ik / total_jobs) if total_jobs > 0 else 0

                        # Service completion rate from phase i = sum of D1[i, :] (row sum)
                        # Scaled by class fraction for multi-class approximation
                        total_d1_rate = np.sum(D1[current_map_phase, :]) * scaling * class_fraction

                        if total_d1_rate <= 0:
                            continue

                        # Calculate routing probabilities
                        src_idx = ist * K + k
                        total_routing = 0.0

                        # Get node index for this station
                        node_idx = int(station_to_node[ist]) if station_to_node is not None and ist < len(station_to_node) else ist

                        # Check if this node has RROBIN routing for class k
                        is_rrobin = (node_idx, k) in rrobin_info['outlinks']

                        # For each destination MAP phase j, the rate is D1[current_phase, j]
                        # Scaled by class fraction for multi-class approximation
                        for new_map_phase in range(n_phases):
                            d1_rate = D1[current_map_phase, new_map_phase] * scaling * class_fraction
                            if d1_rate <= 0:
                                continue

                            if is_rrobin:
                                # RROBIN routing with MAP
                                outlinks = rrobin_info['outlinks'][(node_idx, k)]
                                rr_var_idx = rr_var_map[(node_idx, k)]
                                current_rr_ptr = int(state[rr_var_idx])
                                dest_node = outlinks[current_rr_ptr]
                                next_rr_ptr = (current_rr_ptr + 1) % len(outlinks)

                                if node_to_station is not None and dest_node < len(node_to_station):
                                    dest_station = int(node_to_station[dest_node])
                                else:
                                    dest_station = dest_node

                                r = k  # No class switching for RROBIN

                                if dest_station >= 0 and dest_station < M:
                                    # Get entry probabilities for destination
                                    entry_probs = get_entry_probs(dest_station, r)
                                    for entry_phase, entry_prob in enumerate(entry_probs):
                                        if entry_prob <= 0:
                                            continue
                                        new_state = set_job_count(state, ist, k, -1)
                                        new_state = set_job_count(new_state, dest_station, r, +1, phase_idx=entry_phase)
                                        new_state = set_map_phase(new_state, ist, k, new_map_phase)
                                        new_state[rr_var_idx] = next_rr_ptr

                                        if np.all(new_state[:state_dim] >= 0):
                                            ns = _find_state_index_fast(state_map, new_state)
                                            if ns >= 0:
                                                Q[s, ns] += d1_rate * entry_prob
                                                total_routing += d1_rate * entry_prob
                                else:
                                    # Destination is Sink
                                    new_state = set_job_count(state, ist, k, -1)
                                    new_state = set_map_phase(new_state, ist, k, new_map_phase)
                                    new_state[rr_var_idx] = next_rr_ptr

                                    if np.all(new_state[:state_dim] >= 0):
                                        ns = _find_state_index_fast(state_map, new_state)
                                        if ns >= 0:
                                            Q[s, ns] += d1_rate
                                            total_routing += d1_rate
                            else:
                                # Standard probabilistic routing with MAP
                                for jst in range(M):
                                    if jst == source_station:
                                        continue
                                    for r in range(K):
                                        dst_idx = jst * K + r

                                        if src_idx < P.shape[0] and dst_idx < P.shape[1]:
                                            p = P[src_idx, dst_idx]
                                        else:
                                            p = 0

                                        if p <= 0:
                                            continue

                                        # Get entry probabilities for destination
                                        entry_probs = get_entry_probs(jst, r)
                                        for entry_phase, entry_prob in enumerate(entry_probs):
                                            if entry_prob <= 0:
                                                continue
                                            # Create new state with job movement and MAP phase update
                                            new_state = set_job_count(state, ist, k, -1)
                                            new_state = set_job_count(new_state, jst, r, +1, phase_idx=entry_phase)
                                            new_state = set_map_phase(new_state, ist, k, new_map_phase)

                                            if np.any(new_state[:state_dim] < 0):
                                                continue

                                            ns = _find_state_index_fast(state_map, new_state)
                                            if ns >= 0:
                                                Q[s, ns] += d1_rate * p * entry_prob
                                                total_routing += d1_rate * p * entry_prob

                        # Handle departures to sink for open networks
                        if is_open and total_routing < total_d1_rate:
                            exit_rate = total_d1_rate - total_routing
                            if exit_rate > 0:
                                for new_map_phase in range(n_phases):
                                    d1_rate_raw = D1[current_map_phase, new_map_phase] * scaling * class_fraction
                                    if d1_rate_raw <= 0:
                                        continue
                                    new_state = set_job_count(state, ist, k, -1)
                                    new_state = set_map_phase(new_state, ist, k, new_map_phase)

                                    if np.all(new_state[:state_dim] >= 0):
                                        ns = _find_state_index_fast(state_map, new_state)
                                        if ns >= 0:
                                            # Exit probability proportional to D1 rate
                                            Q[s, ns] += d1_rate_raw * (1.0 - total_routing / total_d1_rate) if total_d1_rate > 0 else 0

                        continue  # Skip the standard routing code for MAP distributions

                if rate <= 0:
                    continue

                # Calculate routing probabilities
                src_idx = ist * K + k
                total_routing = 0.0

                # Get node index for this station
                node_idx = int(station_to_node[ist]) if station_to_node is not None and ist < len(station_to_node) else ist

                # Check if this node has RROBIN routing for class k
                is_rrobin = (node_idx, k) in rrobin_info['outlinks']

                if is_rrobin:
                    # === State-dependent routing (RROBIN) ===
                    outlinks = rrobin_info['outlinks'][(node_idx, k)]
                    rr_var_idx = rr_var_map[(node_idx, k)]
                    current_rr_ptr = int(state[rr_var_idx])  # Index into outlinks array
                    dest_node = outlinks[current_rr_ptr]

                    # Advance round-robin pointer for the next job (wraps around)
                    next_rr_ptr = (current_rr_ptr + 1) % len(outlinks)

                    # Get destination station from destination node
                    if node_to_station is not None and dest_node < len(node_to_station):
                        dest_station = int(node_to_station[dest_node])
                    else:
                        dest_station = dest_node  # Fallback

                    # For RROBIN, routing is deterministic: probability 1.0 to current destination
                    # No class switching for RROBIN (r = k)
                    r = k
                    if dest_station >= 0 and dest_station < M:
                        # Get entry probabilities for destination
                        entry_probs = get_entry_probs(dest_station, r)
                        for entry_phase, entry_prob in enumerate(entry_probs):
                            if entry_prob <= 0:
                                continue
                            # Create new state with job movement and updated RR pointer
                            # Use phase-aware state modification
                            new_state = set_job_count(state, ist, k, -1)  # Departure from ist, class k
                            new_state = set_job_count(new_state, dest_station, r, +1, phase_idx=entry_phase)
                            new_state[rr_var_idx] = next_rr_ptr  # Advance RR pointer

                            if np.all(new_state[:state_dim] >= 0):
                                ns = _find_state_index_fast(state_map, new_state)
                                if ns >= 0:
                                    Q[s, ns] += rate * 1.0 * entry_prob
                                    total_routing += entry_prob
                    else:
                        # Destination is Sink (exit system) - for open networks
                        new_state = set_job_count(state, ist, k, -1)
                        new_state[rr_var_idx] = next_rr_ptr  # Still advance RR pointer

                        if np.all(new_state[:state_dim] >= 0):
                            ns = _find_state_index_fast(state_map, new_state)
                            if ns >= 0:
                                Q[s, ns] += rate * 1.0
                                total_routing = 1.0
                else:
                    # === Standard probabilistic routing ===
                    # Find destination states based on routing
                    for jst in range(M):
                        if jst == source_station:
                            continue  # Can't route to source
                        for r in range(K):
                            # Routing probability from (ist, k) to (jst, r)
                            dst_idx = jst * K + r

                            if src_idx < P.shape[0] and dst_idx < P.shape[1]:
                                p = P[src_idx, dst_idx]
                            else:
                                p = 0

                            if p <= 0:
                                continue

                            total_routing += p

                            # Get entry probabilities for destination
                            entry_probs = get_entry_probs(jst, r)
                            for entry_phase, entry_prob in enumerate(entry_probs):
                                if entry_prob <= 0:
                                    continue
                                # Create new state using phase-aware state modification
                                new_state = set_job_count(state, ist, k, -1)  # Departure from ist, class k
                                new_state = set_job_count(new_state, jst, r, +1, phase_idx=entry_phase)  # Arrival to entry phase

                                # Check if new state is valid
                                if np.any(new_state[:state_dim] < 0):
                                    continue

                                # Find new state index using O(1) hash lookup
                                ns = _find_state_index_fast(state_map, new_state)
                                if ns >= 0:
                                    Q[s, ns] += rate * p * entry_prob

                # === Departures to sink (for open networks) ===
                # If routing doesn't sum to 1, remaining probability exits to sink
                if is_open and total_routing < 1.0:
                    exit_prob = 1.0 - total_routing
                    if exit_prob > 0:
                        # Create new state with job leaving the system
                        new_state = set_job_count(state, ist, k, -1)

                        if np.all(new_state[:state_dim] >= 0):
                            ns = _find_state_index_fast(state_map, new_state)
                            if ns >= 0:
                                Q[s, ns] += rate * exit_prob

    # === Phase-to-phase transitions for INF stations with phase-type distributions ===
    # These are internal transitions (D0 off-diagonal) that don't involve departures
    if use_phase_aug:
        for s, state in enumerate(state_space):
            for ist in range(M):
                # Only handle INF (infinite server) stations
                if hasattr(sn, 'sched') and sn.sched is not None:
                    sched = sn.sched.get(ist, SchedStrategy.FCFS)
                else:
                    continue

                if sched != SchedStrategy.INF:
                    continue

                for k in range(K):
                    n_phases_ik = phases[ist, k]
                    if n_phases_ik <= 1:
                        continue  # No phase transitions for single-phase distributions

                    # Get D0 matrix for phase transitions
                    D0, D1 = get_map_matrices(ist, k)
                    if D0 is None:
                        continue

                    # Get current phase counts
                    phase_counts = get_phase_counts(state, ist, k)

                    # For each source phase with jobs
                    for p_src in range(n_phases_ik):
                        n_src = int(phase_counts[p_src])
                        if n_src <= 0:
                            continue

                        # For each destination phase (D0 off-diagonal)
                        for p_dst in range(n_phases_ik):
                            if p_src == p_dst:
                                continue  # Skip diagonal (absorbed into overall departure rate)

                            # D0 off-diagonal: phase transition rate
                            phase_transition_rate = D0[p_src, p_dst]
                            if phase_transition_rate <= 0:
                                continue

                            # Total rate = n_src * phase_transition_rate
                            total_rate = n_src * phase_transition_rate

                            # Create new state: one job moves from p_src to p_dst
                            new_state = state.copy()
                            start_idx = phase_offset[ist, k]
                            new_state[start_idx + p_src] -= 1
                            new_state[start_idx + p_dst] += 1

                            # Add transition to Q
                            if np.all(new_state[:state_dim] >= 0):
                                ns = _find_state_index_fast(state_map, new_state)
                                if ns >= 0:
                                    Q[s, ns] += total_rate

    # Make valid generator (set diagonal)
    Q = ctmc_makeinfgen(Q)

    return Q


def _compute_metrics_from_distribution(
    sn: NetworkStruct,
    pi: np.ndarray,
    state_space: np.ndarray,
    rrobin_info: Optional[dict] = None
) -> Dict[str, np.ndarray]:
    """
    Compute performance metrics from steady-state distribution.

    Args:
        sn: Network structure
        pi: Steady-state probability distribution
        state_space: State space matrix (may include RR state variables at end)
        rrobin_info: Round-robin routing information

    Returns:
        Dictionary with Q, U, R, T matrices
    """
    M = sn.nstations
    K = sn.nclasses

    # Check if phase augmentation is used
    use_phase_aug = rrobin_info.get('needs_phase_augmentation', False) if rrobin_info else False
    phases = rrobin_info.get('phases', np.ones((M, K), dtype=int)) if rrobin_info else np.ones((M, K), dtype=int)
    phase_offset = rrobin_info.get('phase_offset', None) if rrobin_info else None
    state_dim = rrobin_info.get('state_dim', M * K) if rrobin_info else M * K

    # Get MAP FCFS info for throughput computation
    map_fcfs = rrobin_info.get('map_fcfs', {}) if rrobin_info else {}
    map_var_offset = rrobin_info.get('map_var_offset', {}) if rrobin_info else {}

    def get_job_count(state: np.ndarray, ist: int, k: int) -> float:
        """Get total job count for (station, class) from state vector."""
        if use_phase_aug and phase_offset is not None:
            start_idx = phase_offset[ist, k]
            end_idx = start_idx + phases[ist, k]
            return float(sum(state[start_idx:end_idx]))
        else:
            return float(state[ist * K + k])

    def get_state_matrix(state: np.ndarray) -> np.ndarray:
        """Get job counts as (M, K) matrix from state vector."""
        result = np.zeros((M, K))
        for ist in range(M):
            for k in range(K):
                result[ist, k] = get_job_count(state, ist, k)
        return result

    def get_phase_counts_metrics(state: np.ndarray, ist: int, k: int) -> np.ndarray:
        """Get phase counts for (station, class) from state vector."""
        if use_phase_aug and phase_offset is not None:
            start_idx = phase_offset[ist, k]
            end_idx = start_idx + phases[ist, k]
            return np.array([int(x) for x in state[start_idx:end_idx]])
        else:
            # Single phase
            return np.array([int(state[ist * K + k])])

    def get_d1_matrix(ist: int, k: int) -> Optional[np.ndarray]:
        """Get D1 matrix for (station, class)."""
        if not hasattr(sn, 'proc') or sn.proc is None:
            return None
        proc_is_list = isinstance(sn.proc, list)
        if proc_is_list:
            if ist >= len(sn.proc) or sn.proc[ist] is None:
                return None
            station_proc = sn.proc[ist]
        else:
            if ist not in sn.proc:
                return None
            station_proc = sn.proc[ist]

        proc_entry = None
        if isinstance(station_proc, (list, tuple)):
            if k < len(station_proc):
                proc_entry = station_proc[k]
        elif isinstance(station_proc, dict):
            proc_entry = station_proc.get(k)

        if proc_entry is None:
            return None

        # Handle direct D0/D1 matrices
        if isinstance(proc_entry, (list, tuple)) and len(proc_entry) >= 2:
            return np.atleast_2d(np.array(proc_entry[1], dtype=float))

        # Handle Erlang distribution stored as dict with 'k' and 'mu'
        if isinstance(proc_entry, dict):
            if 'k' in proc_entry and 'mu' in proc_entry:
                n_phases = int(proc_entry['k'])
                mu = float(proc_entry['mu'])  # per-phase rate
                if n_phases > 1:
                    # Construct Erlang D1 matrix: D1[k-1,0] = mu (completion from last phase)
                    D1 = np.zeros((n_phases, n_phases))
                    D1[n_phases - 1, 0] = mu
                    return D1
                else:
                    # Single phase: exponential
                    return np.array([[mu]])
            elif 'probs' in proc_entry and 'rates' in proc_entry:
                # HyperExp distribution
                probs = np.array(proc_entry['probs'])
                rates = np.array(proc_entry['rates'])
                # D1: completion from phase i, restart in phase j with prob_j
                D1 = np.outer(rates, probs)
                return D1
            elif 'rate' in proc_entry:
                # Exponential distribution
                mu = float(proc_entry['rate'])
                return np.array([[mu]])

        return None

    def get_map_phase(state: np.ndarray, ist: int, k: int) -> int:
        """Get current MAP phase for (station, class) from state vector."""
        if (ist, k) not in map_var_offset:
            return 0
        idx = map_var_offset[(ist, k)]
        return int(state[idx])

    def get_map_d1_rate(ist: int, k: int, map_phase: int) -> float:
        """Get MAP D1 service completion rate from current phase."""
        if not hasattr(sn, 'proc') or sn.proc is None:
            return 1.0
        proc_is_list = isinstance(sn.proc, list)
        if proc_is_list:
            if ist >= len(sn.proc) or sn.proc[ist] is None:
                return 1.0
            station_proc = sn.proc[ist]
        else:
            if ist not in sn.proc:
                return 1.0
            station_proc = sn.proc[ist]

        proc_entry = None
        if isinstance(station_proc, (list, tuple)):
            if k < len(station_proc):
                proc_entry = station_proc[k]
        elif isinstance(station_proc, dict):
            proc_entry = station_proc.get(k)

        if proc_entry is None:
            return 1.0

        # Handle direct D0/D1 matrices
        if isinstance(proc_entry, (list, tuple)) and len(proc_entry) >= 2:
            D1 = np.atleast_2d(np.array(proc_entry[1], dtype=float))
            # Total completion rate from this phase = row sum of D1
            return np.sum(D1[map_phase, :])

        # Handle Erlang distribution stored as dict with 'k' and 'mu'
        if isinstance(proc_entry, dict):
            if 'k' in proc_entry and 'mu' in proc_entry:
                n_phases = int(proc_entry['k'])
                mu = float(proc_entry['mu'])  # per-phase rate
                # For Erlang, only last phase completes
                if map_phase == n_phases - 1:
                    return mu
                else:
                    return 0.0
            elif 'probs' in proc_entry and 'rates' in proc_entry:
                # HyperExp distribution: completion rate from phase = rate for that phase
                rates = np.array(proc_entry['rates'])
                if map_phase < len(rates):
                    return rates[map_phase]
                return 0.0
            elif 'rate' in proc_entry:
                # Exponential distribution
                return float(proc_entry['rate'])

        return 1.0

    # Initialize metrics
    QN = np.zeros((M, K))
    UN = np.zeros((M, K))
    RN = np.zeros((M, K))
    TN = np.zeros((M, K))

    # Get service rates
    if hasattr(sn, 'rates') and sn.rates is not None:
        rates = np.asarray(sn.rates)
    else:
        rates = np.ones((M, K))

    # Get number of servers
    if hasattr(sn, 'nservers') and sn.nservers is not None:
        nservers = np.asarray(sn.nservers).flatten()
    else:
        nservers = np.ones(M)

    # Get load-dependent scaling
    lldscaling = None
    if hasattr(sn, 'lldscaling') and sn.lldscaling is not None:
        lldscaling = np.asarray(sn.lldscaling)

    # Track which stations are infinite servers
    inf_server_stations = set()
    if hasattr(sn, 'sched') and sn.sched is not None:
        for ist, sched_val in sn.sched.items():
            if sched_val == SchedStrategy.INF:
                inf_server_stations.add(ist)

    def get_load_scaling(ist: int, total_jobs: int) -> float:
        """Get service rate scaling factor for station ist with total_jobs present."""
        if total_jobs <= 0:
            return 0.0  # No jobs, no service
        # For infinite servers, each job gets its own server
        if ist in inf_server_stations:
            return float(total_jobs)
        if lldscaling is not None and ist < lldscaling.shape[0]:
            idx = total_jobs - 1
            if lldscaling.ndim > 1 and idx < lldscaling.shape[1]:
                return lldscaling[ist, idx]
            elif lldscaling.ndim > 1:
                return lldscaling[ist, -1]
        c = nservers[ist] if ist < len(nservers) else 1
        return min(total_jobs, c)

    def get_max_scaling(ist: int) -> float:
        """Get maximum scaling factor for station (for utilization normalization)."""
        if lldscaling is not None and ist < lldscaling.shape[0]:
            if lldscaling.ndim > 1:
                return np.max(lldscaling[ist, :])
            return lldscaling[ist]
        c = nservers[ist] if ist < len(nservers) else 1
        return c

    # Compute expected queue lengths E[n_ik]
    for s, state in enumerate(state_space):
        state_matrix = get_state_matrix(state)
        for ist in range(M):
            for k in range(K):
                QN[ist, k] += pi[s] * state_matrix[ist, k]

    # Compute throughputs from expected service completions
    # T_i,k = E[service rate for class k at station i]
    for s, state in enumerate(state_space):
        state_matrix = get_state_matrix(state)
        for ist in range(M):
            total_at_station = np.sum(state_matrix[ist, :])
            if total_at_station <= 0:
                continue

            scaling = get_load_scaling(ist, int(total_at_station))

            if hasattr(sn, 'sched') and sn.sched is not None:
                sched = sn.sched.get(ist, SchedStrategy.FCFS)
            else:
                sched = SchedStrategy.FCFS

            for k in range(K):
                n_k = state_matrix[ist, k]
                if n_k <= 0:
                    continue

                mu = rates[ist, k] if ist < rates.shape[0] and k < rates.shape[1] else 1.0

                if sched == SchedStrategy.INF:
                    # Infinite server: rate depends on phase-type distribution
                    n_phases_ik = phases[ist, k]
                    if use_phase_aug and n_phases_ik > 1:
                        # Phase-type: compute departure rate from D1 matrix
                        D1 = get_d1_matrix(ist, k)
                        if D1 is not None:
                            # Get phase counts for this state
                            phase_counts = get_phase_counts_metrics(state, ist, k)
                            # Departure rate = sum over phases p of: n_p * sum(D1[p,:])
                            departure_rate = 0.0
                            for p in range(n_phases_ik):
                                n_p = phase_counts[p]
                                if n_p > 0:
                                    completion_rate_p = np.sum(D1[p, :])
                                    departure_rate += n_p * completion_rate_p
                            TN[ist, k] += pi[s] * departure_rate
                        else:
                            # Fallback to aggregate rate
                            TN[ist, k] += pi[s] * n_k * mu
                    else:
                        # Single phase (exponential): rate = n * mu
                        TN[ist, k] += pi[s] * n_k * mu
                elif sched == SchedStrategy.PSPRIO:
                    # PS with Priority
                    nservers_ist = nservers[ist] if ist < len(nservers) else 1
                    classprio = None
                    if hasattr(sn, 'classprio') and sn.classprio is not None:
                        classprio = np.asarray(sn.classprio).flatten()

                    if classprio is None or total_at_station <= nservers_ist:
                        TN[ist, k] += pi[s] * scaling * mu * (n_k / total_at_station)
                    else:
                        present_classes = [kk for kk in range(K) if state_matrix[ist, kk] > 0]
                        min_prio = min(classprio[kk] for kk in present_classes)
                        if classprio[k] == min_prio:
                            niprio = sum(state_matrix[ist, kk] for kk in range(K)
                                       if classprio[kk] == min_prio)
                            scaling_prio = min(niprio, nservers_ist)
                            TN[ist, k] += pi[s] * scaling_prio * mu * (n_k / niprio)
                        # else: rate = 0, no contribution to throughput
                elif sched == SchedStrategy.GPSPRIO:
                    # GPS with Priority
                    nservers_ist = nservers[ist] if ist < len(nservers) else 1
                    classprio = None
                    if hasattr(sn, 'classprio') and sn.classprio is not None:
                        classprio = np.asarray(sn.classprio).flatten()

                    weights = np.ones(K)
                    if hasattr(sn, 'schedparam') and sn.schedparam is not None:
                        if ist < sn.schedparam.shape[0]:
                            weights = sn.schedparam[ist, :K].flatten()
                    weights = weights / np.sum(weights)

                    if classprio is None or total_at_station <= nservers_ist:
                        cir = np.minimum(state_matrix[ist, :], 1)
                        weighted_total = np.sum(weights * cir)
                        if weighted_total > 0 and state_matrix[ist, k] > 0:
                            TN[ist, k] += pi[s] * mu * (n_k / state_matrix[ist, k]) * weights[k] / weighted_total
                    else:
                        present_classes = [kk for kk in range(K) if state_matrix[ist, kk] > 0]
                        min_prio = min(classprio[kk] for kk in present_classes)
                        if classprio[k] == min_prio:
                            nirprio = np.zeros(K)
                            for kk in range(K):
                                if classprio[kk] == min_prio:
                                    nirprio[kk] = state_matrix[ist, kk]
                            cir = np.minimum(nirprio, 1)
                            weighted_total = np.sum(weights * cir)
                            if weighted_total > 0 and nirprio[k] > 0:
                                TN[ist, k] += pi[s] * mu * (n_k / nirprio[k]) * weights[k] / weighted_total
                else:
                    # PS, FCFS, etc.: share of capacity proportional to number of jobs
                    # For MAP distributions at FCFS, use D1 rate instead of mu
                    if (ist, k) in map_fcfs:
                        map_phase = get_map_phase(state, ist, k)
                        d1_rate = get_map_d1_rate(ist, k, map_phase)
                        TN[ist, k] += pi[s] * scaling * d1_rate * (n_k / total_at_station)
                    else:
                        TN[ist, k] += pi[s] * scaling * mu * (n_k / total_at_station)

    # Compute expected capacity (E[scaling]) at each station
    # E[scaling] = sum over states of pi(s) * lldscaling(station, n)
    expected_scaling = np.zeros(M)
    for s, state in enumerate(state_space):
        state_matrix = get_state_matrix(state)
        for ist in range(M):
            total_at_station = np.sum(state_matrix[ist, :])
            scaling = get_load_scaling(ist, int(total_at_station))
            expected_scaling[ist] += pi[s] * scaling
    # Ensure no division by zero
    expected_scaling = np.maximum(expected_scaling, 1e-10)

    # Compute utilizations using MATLAB's formulas
    # For INF servers: UN = QN
    # For LLD PS/DPS/etc: UN = E[n_k / n_total] (expected fraction of jobs that are class k)
    for ist in range(M):
        if hasattr(sn, 'sched') and sn.sched is not None:
            sched = sn.sched.get(ist, SchedStrategy.FCFS)
        else:
            sched = SchedStrategy.FCFS

        if sched == SchedStrategy.INF:
            # For infinite servers, utilization = queue length
            for k in range(K):
                UN[ist, k] = QN[ist, k]
        elif sched in [SchedStrategy.PS, SchedStrategy.DPS, SchedStrategy.GPS]:
            # For PS/DPS/GPS: UN = E[n_k / n_total]
            # This is already computed below via state iteration
            pass
        elif sched in [SchedStrategy.PSPRIO, SchedStrategy.GPSPRIO]:
            # For priority variants: UN = T / (c * mu) like FCFS
            c = nservers[ist] if ist < len(nservers) else 1
            for k in range(K):
                mu = rates[ist, k] if ist < rates.shape[0] and k < rates.shape[1] else 1.0
                if mu > 0 and c > 0:
                    UN[ist, k] = TN[ist, k] / (c * mu)
        else:
            # For FCFS and others: UN = T / (c * mu) where c is number of servers
            # For MAP distributions, use expected D1 rate instead of mu
            c = nservers[ist] if ist < len(nservers) else 1
            for k in range(K):
                if (ist, k) in map_fcfs:
                    # For MAP: compute expected D1 rate across states
                    expected_d1 = 0.0
                    total_weight = 0.0
                    for s, state in enumerate(state_space):
                        state_matrix = get_state_matrix(state)
                        n_k = state_matrix[ist, k]
                        if n_k > 0:
                            map_phase = get_map_phase(state, ist, k)
                            d1_rate = get_map_d1_rate(ist, k, map_phase)
                            expected_d1 += pi[s] * d1_rate
                            total_weight += pi[s]
                    if total_weight > 0:
                        expected_d1 = expected_d1 / total_weight
                    if expected_d1 > 0 and c > 0:
                        UN[ist, k] = TN[ist, k] / (c * expected_d1)
                else:
                    mu = rates[ist, k] if ist < rates.shape[0] and k < rates.shape[1] else 1.0
                    if mu > 0 and c > 0:
                        UN[ist, k] = TN[ist, k] / (c * mu)

    # For PS/DPS with LLD, compute UN = E[n_k / n_total]
    for s, state in enumerate(state_space):
        state_matrix = get_state_matrix(state)
        for ist in range(M):
            if hasattr(sn, 'sched') and sn.sched is not None:
                sched = sn.sched.get(ist, SchedStrategy.FCFS)
            else:
                sched = SchedStrategy.FCFS

            if sched in [SchedStrategy.PS, SchedStrategy.DPS, SchedStrategy.GPS]:
                n_total = np.sum(state_matrix[ist, :])
                if n_total > 0:
                    for k in range(K):
                        n_k = state_matrix[ist, k]
                        # With equal schedparam weights: n_k / n_total
                        UN[ist, k] += pi[s] * n_k / n_total

    # Compute response times: R = Q / T (Little's law)
    for ist in range(M):
        for k in range(K):
            if TN[ist, k] > 0:
                RN[ist, k] = QN[ist, k] / TN[ist, k]
            else:
                RN[ist, k] = 0

    # Handle Source station metrics for open networks
    # Source doesn't hold jobs - QLen represents cutoff buffer which should be 0 for reporting
    # Throughput should be the arrival rate
    if hasattr(sn, 'sched') and sn.sched is not None:
        for ist, sched_val in sn.sched.items():
            # Check for EXT scheduling (Source station)
            is_source = (sched_val == SchedStrategy.EXT or
                        (isinstance(sched_val, int) and sched_val == 11))
            if is_source and ist < M:
                for k in range(K):
                    # Source doesn't hold jobs in the traditional sense
                    QN[ist, k] = 0.0
                    UN[ist, k] = 0.0
                    RN[ist, k] = 0.0
                    # Throughput is the arrival rate
                    if ist < rates.shape[0] and k < rates.shape[1]:
                        TN[ist, k] = rates[ist, k]

    return {
        'Q': QN,
        'U': UN,
        'R': RN,
        'T': TN
    }


def solver_ctmc_basic(
    sn: NetworkStruct,
    options: Optional[SolverCTMCOptions] = None
) -> SolverCTMCReturn:
    """
    Basic CTMC solver using state-space enumeration.

    Enumerates all valid states, builds the infinitesimal generator,
    and solves for steady-state distribution.

    Args:
        sn: Network structure
        options: Solver options

    Returns:
        SolverCTMCReturn with performance metrics
    """
    start_time = time.time()

    if options is None:
        options = SolverCTMCOptions()

    M = sn.nstations
    K = sn.nclasses

    # Enumerate state space
    state_space, state_space_aggr, rrobin_info = _enumerate_state_space(sn, options.cutoff)

    # Mandatory truncation warning for open/mixed models
    if sn_has_open_classes(sn):
        print(f"CTMC solver using state space cutoff = {options.cutoff} for open/mixed model.")
        warnings.warn(
            "State space truncation may cause inaccurate results. "
            "Consider varying cutoff to assess sensitivity.",
            UserWarning
        )

    if options.verbose:
        print(f"CTMC state space size: {len(state_space)}")
        if rrobin_info['total_vars'] > 0:
            print(f"  Including {rrobin_info['total_vars']} round-robin state variables")

    # Build generator matrix
    Q = _build_generator(sn, state_space, options, rrobin_info)

    # Solve for steady-state distribution
    pi = ctmc_solve(Q)

    # Compute performance metrics
    metrics = _compute_metrics_from_distribution(sn, pi, state_space, rrobin_info)

    QN = metrics['Q']
    UN = metrics['U']
    RN = metrics['R']
    TN = metrics['T']

    # Compute cycle times and system throughput
    CN = np.sum(RN, axis=0).reshape(1, -1)
    XN = np.zeros((1, K))
    for k in range(K):
        ref_stat = int(sn.refstat[k]) if hasattr(sn, 'refstat') and k < len(sn.refstat) else 0
        if ref_stat < M:
            XN[0, k] = TN[ref_stat, k]

    # Clean up NaN values
    QN = np.nan_to_num(QN, nan=0.0)
    UN = np.nan_to_num(UN, nan=0.0)
    RN = np.nan_to_num(RN, nan=0.0)
    TN = np.nan_to_num(TN, nan=0.0)
    CN = np.nan_to_num(CN, nan=0.0)
    XN = np.nan_to_num(XN, nan=0.0)

    result = SolverCTMCReturn()
    result.Q = QN
    result.U = UN
    result.R = RN
    result.T = TN
    result.C = CN
    result.X = XN
    result.pi = pi
    result.infgen = Q
    result.space = state_space
    result.runtime = time.time() - start_time
    result.method = "basic"

    return result


def solver_ctmc(
    sn: NetworkStruct,
    options: Optional[SolverCTMCOptions] = None
) -> SolverCTMCReturn:
    """
    Main CTMC solver handler.

    Routes to appropriate method based on options and network characteristics.

    Args:
        sn: Network structure
        options: Solver options

    Returns:
        SolverCTMCReturn with performance metrics
    """
    if options is None:
        options = SolverCTMCOptions()

    method = options.method.lower()

    if method in ['default', 'basic']:
        return solver_ctmc_basic(sn, options)
    else:
        # Unknown method - use basic
        if options.verbose:
            print(f"Warning: Unknown CTMC method '{method}'. Using basic.")
        return solver_ctmc_basic(sn, options)


__all__ = [
    'solver_ctmc',
    'solver_ctmc_basic',
    'SolverCTMCReturn',
    'SolverCTMCOptions',
]
