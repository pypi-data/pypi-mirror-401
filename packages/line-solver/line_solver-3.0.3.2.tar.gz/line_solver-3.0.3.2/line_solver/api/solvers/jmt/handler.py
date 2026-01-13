"""
JMT Solver handler - Native Python implementation.

Calls JMT via subprocess.

Port from:



Note: This is a simplified implementation supporting basic queueing networks.
Complex features (caches, transitions, etc.) may require the Java implementation.
"""

import numpy as np
import subprocess
import tempfile
import os
import shutil
import platform
import urllib.request
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict, Any
from xml.etree import ElementTree as ET
from xml.dom import minidom
import time

from ...sn import (
    NetworkStruct,
    NodeType,
    SchedStrategy,
    sn_get_demands_chain,
    sn_deaggregate_chain_results,
)
from ....constants import ProcessType, PollingType


@dataclass
class SolverJMTOptions:
    """Options for JMT solver."""
    method: str = 'jsim'
    samples: int = 10000
    seed: int = 23000
    max_simulated_time: float = float('inf')
    conf_int: float = 0.99
    max_rel_err: float = 0.03
    verbose: bool = False


@dataclass
class SolverJMTReturn:
    """
    Result of JMT solver handler.

    Attributes:
        Q: Mean queue lengths (M x K)
        U: Utilizations (M x K)
        R: Response times (M x K)
        T: Throughputs (M x K)
        A: Arrival rates (M x K)
        W: Waiting times (M x K)
        C: Cycle times (1 x K)
        X: System throughputs (1 x K)
        runtime: Runtime in seconds
        method: Method used
    """
    Q: Optional[np.ndarray] = None
    U: Optional[np.ndarray] = None
    R: Optional[np.ndarray] = None
    T: Optional[np.ndarray] = None
    A: Optional[np.ndarray] = None
    W: Optional[np.ndarray] = None
    C: Optional[np.ndarray] = None
    X: Optional[np.ndarray] = None
    runtime: float = 0.0
    method: str = "jsim"


def _get_jmt_jar_path() -> str:
    """Get path to JMT.jar, downloading if necessary."""
    # Look in common/ directory
    package_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    python_dir = os.path.dirname(package_dir)
    root_dir = os.path.dirname(python_dir)
    common_dir = os.path.join(root_dir, 'common')
    jmt_path = os.path.join(common_dir, 'JMT.jar')

    if os.path.isfile(jmt_path):
        return jmt_path

    # Try to download
    os.makedirs(common_dir, exist_ok=True)
    jmt_url = 'https://line-solver.sourceforge.net/latest/JMT.jar'
    try:
        urllib.request.urlretrieve(jmt_url, jmt_path)
        return jmt_path
    except Exception as e:
        raise RuntimeError(
            f"JMT.jar not found and download failed: {e}\n"
            f"Please manually download from {jmt_url} and place in {common_dir}"
        )


def is_jmt_available() -> bool:
    """Check if JMT is available."""
    # Check for JMT
    try:
        result = subprocess.run(
            ['java', '-version'],
            capture_output=True,
            timeout=5
        )
        if result.returncode != 0:
            return False
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return False

    # Check for JMT.jar
    try:
        jmt_path = _get_jmt_jar_path()
        return os.path.isfile(jmt_path)
    except RuntimeError:
        return False


def _get_sched_strategy_class(sched: SchedStrategy) -> str:
    """Map scheduling strategy to JMT QueueGetStrategy class name.

    Note: JMT handles PS/GPS/DPS through PSStrategies, not QueueGetStrategies.
    For QueueGetStrategies, only FCFS and LCFS are available.
    PS and other strategies are handled by the Server section's PSStrategy.
    """
    strategy_map = {
        SchedStrategy.FCFS: "jmt.engine.NetStrategies.QueueGetStrategies.FCFSstrategy",
        SchedStrategy.LCFS: "jmt.engine.NetStrategies.QueueGetStrategies.LCFSstrategy",
        # PS/SIRO/INF use FCFS queue get strategy - actual scheduling is in PSStrategy
        SchedStrategy.PS: "jmt.engine.NetStrategies.QueueGetStrategies.FCFSstrategy",
        SchedStrategy.SIRO: "jmt.engine.NetStrategies.QueueGetStrategies.FCFSstrategy",
        SchedStrategy.INF: "jmt.engine.NetStrategies.QueueGetStrategies.FCFSstrategy",
    }
    return strategy_map.get(sched, "jmt.engine.NetStrategies.QueueGetStrategies.FCFSstrategy")


def _get_polling_get_strategy_class(polling_type: PollingType) -> str:
    """Map polling type to JMT QueueGetStrategy class name for polling queues.

    Args:
        polling_type: PollingType enum value

    Returns:
        JMT class path for the polling get strategy
    """
    if polling_type == PollingType.GATED:
        return "jmt.engine.NetStrategies.QueueGetStrategies.GatedPollingGetStrategy"
    elif polling_type == PollingType.EXHAUSTIVE:
        return "jmt.engine.NetStrategies.QueueGetStrategies.ExhaustivePollingGetStrategy"
    elif polling_type == PollingType.KLIMITED:
        return "jmt.engine.NetStrategies.QueueGetStrategies.LimitedPollingGetStrategy"
    else:
        return "jmt.engine.NetStrategies.QueueGetStrategies.ExhaustivePollingGetStrategy"


def _write_polling_get_strategy(queue_elem: ET.Element, polling_type: PollingType, polling_k: int = 1):
    """Write polling get strategy to JMT Queue section.

    Args:
        queue_elem: Queue XML section element
        polling_type: PollingType enum value
        polling_k: K value for KLIMITED polling
    """
    strategy_param = ET.SubElement(queue_elem, 'parameter')
    strategy_param.set('classPath', _get_polling_get_strategy_class(polling_type))
    strategy_param.set('name', 'FCFSstrategy')

    # For KLIMITED polling, add the pollingKValue subparameter
    if polling_type == PollingType.KLIMITED:
        polling_k_param = ET.SubElement(strategy_param, 'subParameter')
        polling_k_param.set('classPath', 'java.lang.Integer')
        polling_k_param.set('name', 'pollingKValue')
        value = ET.SubElement(polling_k_param, 'value')
        value.text = str(int(polling_k))


def _write_switchover_service_time_strategy(parent: ET.Element, procid: int, proc, rate: float, scv: float = 1.0):
    """Write service time strategy for switchover distributions.

    Args:
        parent: Parent XML element for the subParameter
        procid: ProcessType ID for the distribution
        proc: Process data (distribution parameters, e.g., list of matrices for PH)
        rate: Service rate (for simple distributions)
        scv: Squared coefficient of variation (for distributions that need it)
    """
    service_time_node = ET.SubElement(parent, 'subParameter')

    if procid == ProcessType.DISABLED:
        service_time_node.set('classPath', 'jmt.engine.NetStrategies.ServiceStrategies.DisabledServiceTimeStrategy')
        service_time_node.set('name', 'DisabledServiceTimeStrategy')
        return

    if procid == ProcessType.IMMEDIATE:
        service_time_node.set('classPath', 'jmt.engine.NetStrategies.ServiceStrategies.ZeroServiceTimeStrategy')
        service_time_node.set('name', 'ZeroServiceTimeStrategy')
        return

    service_time_node.set('classPath', 'jmt.engine.NetStrategies.ServiceStrategies.ServiceTimeStrategy')
    service_time_node.set('name', 'ServiceTimeStrategy')

    # Distribution node
    distr_node = ET.SubElement(service_time_node, 'subParameter')
    distr_par_node = ET.SubElement(service_time_node, 'subParameter')

    if procid == ProcessType.EXP:
        distr_node.set('classPath', 'jmt.engine.random.Exponential')
        distr_node.set('name', 'Exponential')
        distr_par_node.set('classPath', 'jmt.engine.random.ExponentialPar')
        distr_par_node.set('name', 'distrPar')

        lambda_param = ET.SubElement(distr_par_node, 'subParameter')
        lambda_param.set('classPath', 'java.lang.Double')
        lambda_param.set('name', 'lambda')
        value = ET.SubElement(lambda_param, 'value')
        value.text = f'{rate:.12f}'

    elif procid == ProcessType.DET:
        distr_node.set('classPath', 'jmt.engine.random.DeterministicDistr')
        distr_node.set('name', 'Deterministic')
        distr_par_node.set('classPath', 'jmt.engine.random.DeterministicDistrPar')
        distr_par_node.set('name', 'distrPar')

        t_param = ET.SubElement(distr_par_node, 'subParameter')
        t_param.set('classPath', 'java.lang.Double')
        t_param.set('name', 't')
        value = ET.SubElement(t_param, 'value')
        value.text = f'{1.0/rate:.12f}' if rate > 0 else '0.0'

    elif procid == ProcessType.ERLANG:
        phases = len(proc[0]) if proc and isinstance(proc, (list, tuple)) and len(proc) > 0 else 2
        distr_node.set('classPath', 'jmt.engine.random.Erlang')
        distr_node.set('name', 'Erlang')
        distr_par_node.set('classPath', 'jmt.engine.random.ErlangPar')
        distr_par_node.set('name', 'distrPar')

        alpha_param = ET.SubElement(distr_par_node, 'subParameter')
        alpha_param.set('classPath', 'java.lang.Double')
        alpha_param.set('name', 'alpha')
        value = ET.SubElement(alpha_param, 'value')
        value.text = f'{rate * phases:.12f}'

        r_param = ET.SubElement(distr_par_node, 'subParameter')
        r_param.set('classPath', 'java.lang.Long')
        r_param.set('name', 'r')
        value = ET.SubElement(r_param, 'value')
        value.text = str(phases)

    elif procid == ProcessType.HYPEREXP:
        distr_node.set('classPath', 'jmt.engine.random.HyperExp')
        distr_node.set('name', 'Hyperexponential')
        distr_par_node.set('classPath', 'jmt.engine.random.HyperExpPar')
        distr_par_node.set('name', 'distrPar')

        # Extract parameters from proc (PH representation)
        if proc and isinstance(proc, (list, tuple)) and len(proc) >= 2:
            T_mat = np.asarray(proc[0], dtype=np.float64)
            alpha = np.asarray(proc[1], dtype=np.float64) if len(proc) > 1 else None
            if alpha is None:
                alpha = np.array([1.0, 0.0])
            p = alpha[0] if len(alpha) > 0 else 0.5
            lambda1 = -T_mat[0, 0] if T_mat.shape[0] > 0 else rate
            lambda2 = -T_mat[1, 1] if T_mat.shape[0] > 1 else rate
        else:
            p = 0.5
            lambda1 = rate
            lambda2 = rate

        p_param = ET.SubElement(distr_par_node, 'subParameter')
        p_param.set('classPath', 'java.lang.Double')
        p_param.set('name', 'p')
        value = ET.SubElement(p_param, 'value')
        value.text = f'{p:.12f}'

        l1_param = ET.SubElement(distr_par_node, 'subParameter')
        l1_param.set('classPath', 'java.lang.Double')
        l1_param.set('name', 'lambda1')
        value = ET.SubElement(l1_param, 'value')
        value.text = f'{lambda1:.12f}'

        l2_param = ET.SubElement(distr_par_node, 'subParameter')
        l2_param.set('classPath', 'java.lang.Double')
        l2_param.set('name', 'lambda2')
        value = ET.SubElement(l2_param, 'value')
        value.text = f'{lambda2:.12f}'

    else:
        # Default to exponential for unsupported types
        distr_node.set('classPath', 'jmt.engine.random.Exponential')
        distr_node.set('name', 'Exponential')
        distr_par_node.set('classPath', 'jmt.engine.random.ExponentialPar')
        distr_par_node.set('name', 'distrPar')

        lambda_param = ET.SubElement(distr_par_node, 'subParameter')
        lambda_param.set('classPath', 'java.lang.Double')
        lambda_param.set('name', 'lambda')
        value = ET.SubElement(lambda_param, 'value')
        value.text = f'{rate:.12f}'


def _write_switchover_strategy(server_elem: ET.Element, node_idx: int, sn: NetworkStruct, classnames: List[str]):
    """Write switchover strategy for polling queues.

    Writes the SwitchoverStrategy parameter to the Server section for polling queues.

    Args:
        server_elem: Server XML section element
        node_idx: Node index in the network
        sn: NetworkStruct containing nodeparam with switchover info
        classnames: List of class names
    """
    K = len(classnames)
    is_polling_queue = False
    has_switchover = False

    # Check if this is a polling queue with switchover
    if sn.nodeparam and node_idx in sn.nodeparam:
        nodeparam = sn.nodeparam[node_idx]
        if isinstance(nodeparam, dict):
            # Check if any class has switchover
            for r in range(K):
                if r in nodeparam and isinstance(nodeparam[r], dict):
                    if 'pollingType' in nodeparam[r]:
                        is_polling_queue = True
                    if 'switchoverTime' in nodeparam[r]:
                        has_switchover = True
                    if is_polling_queue:
                        break

    if not is_polling_queue:
        return

    param_node = ET.SubElement(server_elem, 'parameter')
    param_node.set('array', 'true')

    if has_switchover:
        param_node.set('classPath', 'jmt.engine.NetStrategies.ServiceStrategy')
        param_node.set('name', 'SwitchoverStrategy')

        nodeparam = sn.nodeparam[node_idx]
        for r in range(K):
            ref_class = ET.SubElement(param_node, 'refClass')
            ref_class.text = classnames[r]

            # Get switchover distribution for this class
            switchover_time = None
            switchover_proc_id = ProcessType.DISABLED
            rate = 1.0

            if r in nodeparam and isinstance(nodeparam[r], dict):
                switchover_times = nodeparam[r].get('switchoverTime', {})
                switchover_proc_ids = nodeparam[r].get('switchoverProcId', {})

                # For polling, switchover is typically uniform across class transitions
                # Use first available switchover or default
                if switchover_times:
                    first_key = list(switchover_times.keys())[0]
                    switchover_time = switchover_times[first_key]
                    switchover_proc_id = switchover_proc_ids.get(first_key, ProcessType.EXP)

                    # Get rate from distribution
                    if hasattr(switchover_time, 'getMean'):
                        mean = switchover_time.getMean()
                        rate = 1.0 / mean if mean > 0 else 1.0
                    elif hasattr(switchover_time, 'get_mean'):
                        mean = switchover_time.get_mean()
                        rate = 1.0 / mean if mean > 0 else 1.0
                    elif hasattr(switchover_time, '_rate'):
                        rate = switchover_time._rate

            # Get proc data for complex distributions
            proc = None
            if switchover_time and hasattr(switchover_time, 'get_representation'):
                proc = switchover_time.get_representation()
            elif switchover_time and hasattr(switchover_time, '_representation'):
                proc = switchover_time._representation

            _write_switchover_service_time_strategy(param_node, switchover_proc_id, proc, rate)
    else:
        # No switchover - write empty strategy
        param_node.set('classPath', 'java.lang.Object')
        param_node.set('name', 'SwitchoverStrategy')

        for r in range(K):
            ref_class = ET.SubElement(param_node, 'refClass')
            ref_class.text = classnames[r]

            # Empty subparameter for each class with class-to-class structure
            sub_param_row = ET.SubElement(param_node, 'subParameter')
            sub_param_row.set('array', 'true')
            sub_param_row.set('classPath', 'jmt.engine.NetStrategies.ServiceStrategy')
            sub_param_row.set('name', 'SwitchoverStrategy')

            for s in range(K):
                ref_class_s = ET.SubElement(sub_param_row, 'refClass')
                ref_class_s.text = classnames[s]

                # Disabled switchover
                _write_switchover_service_time_strategy(sub_param_row, ProcessType.DISABLED, None, 1.0)


def _detect_class_switches(sn: NetworkStruct) -> Dict[Tuple[int, int], np.ndarray]:
    """
    Detect node pairs that require ClassSwitch nodes for JMT.

    For each pair of connected nodes (i, j), check if there's class switching
    in the routing. If the class transition matrix from i to j is not diagonal,
    a ClassSwitch node needs to be inserted.

    Args:
        sn: NetworkStruct object

    Returns:
        Dictionary mapping (source_idx, dest_idx) to class switching matrix (K x K)
        where matrix[r][s] is the probability of switching from class r to class s
        when routing from source to dest.
    """
    if sn.rtnodes is None or sn.connmatrix is None:
        return {}

    K = sn.nclasses
    nnodes = sn.nnodes
    cs_nodes = {}

    # For each connected node pair, check if there's class switching
    for i in range(nnodes):
        # Skip if source node is already a ClassSwitch - it already handles class transitions
        if sn.nodetype is not None and len(sn.nodetype) > i:
            if sn.nodetype[i] == NodeType.CLASSSWITCH:
                continue

        for j in range(nnodes):
            if sn.connmatrix[i, j] <= 0:
                continue

            # Build the class switching matrix for this node pair
            cs_matrix = np.zeros((K, K))
            has_nonzero = False

            for r in range(K):
                row_sum = 0.0
                for s in range(K):
                    src_idx = i * K + r
                    dst_idx = j * K + s
                    if src_idx < sn.rtnodes.shape[0] and dst_idx < sn.rtnodes.shape[1]:
                        prob = sn.rtnodes[src_idx, dst_idx]
                        cs_matrix[r, s] = prob
                        row_sum += prob
                        if prob > 0:
                            has_nonzero = True

                # Normalize row if it has non-zero entries
                if row_sum > 0:
                    cs_matrix[r, :] /= row_sum

            if not has_nonzero:
                continue

            # Check if matrix is not diagonal (i.e., has class switching)
            is_diagonal = True
            for r in range(K):
                for s in range(K):
                    if r != s and cs_matrix[r, s] > 1e-10:
                        is_diagonal = False
                        break
                if not is_diagonal:
                    break

            if not is_diagonal:
                cs_nodes[(i, j)] = cs_matrix

    return cs_nodes


def _write_auto_classswitch_node(
    sim: ET.Element,
    cs_name: str,
    cs_matrix: np.ndarray,
    dest_node: str,
    classnames: List[str]
) -> None:
    """
    Write an auto-generated ClassSwitch node for handling class switching in routing.

    Args:
        sim: Parent XML element (sim)
        cs_name: Name for the ClassSwitch node (e.g., "CS_Queue1_to_Delay")
        cs_matrix: K x K class switching probability matrix
        dest_node: Name of destination node to route to
        classnames: List of class names
    """
    K = len(classnames)

    node_elem = ET.SubElement(sim, 'node')
    node_elem.set('name', cs_name)

    # 1. Queue section (input buffer)
    queue = ET.SubElement(node_elem, 'section')
    queue.set('className', 'Queue')

    size_param = ET.SubElement(queue, 'parameter')
    size_param.set('classPath', 'java.lang.Integer')
    size_param.set('name', 'size')
    value = ET.SubElement(size_param, 'value')
    value.text = '-1'

    # Drop strategies
    drop_strategy = ET.SubElement(queue, 'parameter')
    drop_strategy.set('array', 'true')
    drop_strategy.set('classPath', 'java.lang.String')
    drop_strategy.set('name', 'dropStrategies')

    for r in range(K):
        ref_class = ET.SubElement(drop_strategy, 'refClass')
        ref_class.text = classnames[r]

        sub_param = ET.SubElement(drop_strategy, 'subParameter')
        sub_param.set('classPath', 'java.lang.String')
        sub_param.set('name', 'dropStrategy')
        value = ET.SubElement(sub_param, 'value')
        value.text = 'drop'

    # Queue get strategy (FCFS)
    strategy_param = ET.SubElement(queue, 'parameter')
    strategy_param.set('classPath', 'jmt.engine.NetStrategies.QueueGetStrategies.FCFSstrategy')
    strategy_param.set('name', 'FCFSstrategy')

    # Queue put strategy
    put_strategy = ET.SubElement(queue, 'parameter')
    put_strategy.set('array', 'true')
    put_strategy.set('classPath', 'jmt.engine.NetStrategies.QueuePutStrategy')
    put_strategy.set('name', 'QueuePutStrategy')

    for r in range(K):
        ref_class = ET.SubElement(put_strategy, 'refClass')
        ref_class.text = classnames[r]

        sub_param = ET.SubElement(put_strategy, 'subParameter')
        sub_param.set('classPath', 'jmt.engine.NetStrategies.QueuePutStrategies.TailStrategy')
        sub_param.set('name', 'TailStrategy')

    # 2. ClassSwitch section
    cs_section = ET.SubElement(node_elem, 'section')
    cs_section.set('className', 'ClassSwitch')

    matrix_param = ET.SubElement(cs_section, 'parameter')
    matrix_param.set('array', 'true')
    matrix_param.set('classPath', 'java.lang.Object')
    matrix_param.set('name', 'matrix')

    for r in range(K):
        ref_class = ET.SubElement(matrix_param, 'refClass')
        ref_class.text = classnames[r]

        row_param = ET.SubElement(matrix_param, 'subParameter')
        row_param.set('array', 'true')
        row_param.set('classPath', 'java.lang.Float')
        row_param.set('name', 'row')

        for s in range(K):
            ref_class_col = ET.SubElement(row_param, 'refClass')
            ref_class_col.text = classnames[s]

            cell_param = ET.SubElement(row_param, 'subParameter')
            cell_param.set('classPath', 'java.lang.Float')
            cell_param.set('name', 'cell')
            cell_value = ET.SubElement(cell_param, 'value')
            cell_value.text = f'{cs_matrix[r, s]:.12f}'

    # 3. Router section - always route to destination with Random strategy
    router = ET.SubElement(node_elem, 'section')
    router.set('className', 'Router')

    routing_param = ET.SubElement(router, 'parameter')
    routing_param.set('array', 'true')
    routing_param.set('classPath', 'jmt.engine.NetStrategies.RoutingStrategy')
    routing_param.set('name', 'RoutingStrategy')

    for r in range(K):
        ref_class = ET.SubElement(routing_param, 'refClass')
        ref_class.text = classnames[r]

        sub_param = ET.SubElement(routing_param, 'subParameter')
        sub_param.set('classPath', 'jmt.engine.NetStrategies.RoutingStrategies.RandomStrategy')
        sub_param.set('name', 'Random')


def _write_jsim_file(sn: NetworkStruct, model_path: str, options: SolverJMTOptions, model: Any = None) -> None:
    """
    Write the network model to JSIM XML format.

    This is a simplified version supporting basic queueing networks.

    Args:
        sn: NetworkStruct containing network configuration
        model_path: Path to write the JSIM file
        options: Solver options
        model: Optional Network model (for FCR regions)
    """
    M = sn.nstations
    K = sn.nclasses

    from datetime import datetime
    timestamp = datetime.now().strftime('%a %b %d %H:%M:%S %Y')

    # Create archive root element
    archive = ET.Element('archive')
    archive.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    archive.set('name', os.path.basename(model_path))
    archive.set('timestamp', timestamp)
    archive.set('xsi:noNamespaceSchemaLocation', 'Archive.xsd')

    # Create sim element inside archive
    sim = ET.SubElement(archive, 'sim')
    sim.set('disableStatisticStop', 'true')
    sim.set('logDecimalSeparator', '.')
    sim.set('logDelimiter', ';')
    sim.set('logPath', os.path.dirname(model_path))
    sim.set('logReplaceMode', '0')
    sim.set('maxEvents', '-1')
    sim.set('maxSamples', str(options.samples))
    sim.set('name', os.path.basename(model_path))
    sim.set('polling', '1.0')
    sim.set('seed', str(options.seed))
    sim.set('xsi:noNamespaceSchemaLocation', 'SIMmodeldefinition.xsd')

    # Create class definitions
    njobs = sn.njobs.flatten() if sn.njobs is not None else np.zeros(K)
    classnames = sn.classnames if sn.classnames else [f'Class{i+1}' for i in range(K)]
    nodenames = sn.nodenames if sn.nodenames else [f'Node{i+1}' for i in range(sn.nnodes)]
    refstat = sn.refstat.flatten() if hasattr(sn, 'refstat') and sn.refstat is not None else np.zeros(K, dtype=int)

    for r in range(K):
        class_elem = ET.SubElement(sim, 'userClass')
        class_elem.set('name', classnames[r])
        class_elem.set('priority', '0')

        if np.isinf(njobs[r]):
            # Open class - reference source is Source node
            class_elem.set('referenceSource', 'Source')
            class_elem.set('type', 'open')
        else:
            # Closed class - reference source is the station where jobs start
            # refstat contains station indices, convert to node index using stationToNode
            ref_station = int(refstat[r])
            if hasattr(sn, 'stationToNode') and sn.stationToNode is not None and ref_station < len(sn.stationToNode):
                ref_node_idx = int(sn.stationToNode[ref_station])
            else:
                ref_node_idx = ref_station
            ref_name = nodenames[ref_node_idx] if ref_node_idx < len(nodenames) else classnames[r] + '_RefStation'
            class_elem.set('referenceSource', ref_name)
            class_elem.set('type', 'closed')
            class_elem.set('customers', str(int(njobs[r])))

    # Detect class switches in routing - JMT requires ClassSwitch nodes for class transitions
    cs_nodes = _detect_class_switches(sn)
    # Map (source, dest) -> ClassSwitch node name
    cs_node_names = {}
    for (src_idx, dst_idx), cs_matrix in cs_nodes.items():
        cs_name = f"CS_{nodenames[src_idx]}_to_{nodenames[dst_idx]}"
        cs_node_names[(src_idx, dst_idx)] = cs_name

    # Create nodes
    nodenames = sn.nodenames if sn.nodenames else [f'Node{i+1}' for i in range(sn.nnodes)]

    for i in range(sn.nnodes):
        node_type = sn.nodetype[i] if sn.nodetype is not None and len(sn.nodetype) > i else NodeType.QUEUE
        node_name = nodenames[i]

        node_elem = ET.SubElement(sim, 'node')
        node_elem.set('name', node_name)

        if node_type == NodeType.SOURCE:
            _write_source_node(node_elem, i, sn, classnames, cs_node_names)
        elif node_type == NodeType.SINK:
            _write_sink_node(node_elem, sn, classnames)
        elif node_type == NodeType.DELAY:
            _write_delay_node(node_elem, i, sn, classnames, cs_node_names)
        elif node_type == NodeType.QUEUE:
            # Check if this is actually a Delay (infinite server) queue by checking SchedStrategy.INF
            ist = int(sn.nodeToStation[i]) if hasattr(sn, 'nodeToStation') and sn.nodeToStation is not None and i < len(sn.nodeToStation) else i
            sched = sn.sched.get(ist, SchedStrategy.FCFS) if sn.sched else SchedStrategy.FCFS
            if sched == SchedStrategy.INF:
                _write_delay_node(node_elem, i, sn, classnames, cs_node_names)
            else:
                _write_queue_node(node_elem, i, sn, classnames, options, cs_node_names)
        elif node_type == NodeType.ROUTER:
            _write_router_node(node_elem, i, sn, classnames, cs_node_names)
        elif node_type == NodeType.FORK:
            _write_fork_node(node_elem, i, sn, classnames, cs_node_names)
        elif node_type == NodeType.JOIN:
            _write_join_node(node_elem, i, sn, classnames, cs_node_names)
        elif node_type == NodeType.CLASSSWITCH:
            _write_classswitch_node(node_elem, i, sn, classnames)
        elif node_type == NodeType.PLACE:
            _write_place_node(node_elem, i, sn, classnames)
        elif node_type == NodeType.TRANSITION:
            _write_transition_node(node_elem, i, sn, classnames)

    # Create auto-generated ClassSwitch nodes for class switching in routing
    for (src_idx, dst_idx), cs_matrix in cs_nodes.items():
        cs_name = cs_node_names[(src_idx, dst_idx)]
        dest_name = nodenames[dst_idx]
        _write_auto_classswitch_node(sim, cs_name, cs_matrix, dest_name, classnames)

    # Metrics (must come before connections per JMT schema)
    for i in range(M):
        node_idx = int(sn.stationToNode[i]) if sn.stationToNode is not None else i
        node_name = nodenames[node_idx]
        node_type = sn.nodetype[node_idx] if sn.nodetype is not None and len(sn.nodetype) > node_idx else NodeType.QUEUE

        if node_type == NodeType.SOURCE or node_type == NodeType.SINK:
            continue

        # Format alpha to avoid floating-point precision issues (e.g., 1-0.99 = 0.010000000000000009)
        alpha_str = f'{round(1 - options.conf_int, 10)}'

        for r in range(K):
            # Queue length
            metric = ET.SubElement(sim, 'measure')
            metric.set('alpha', alpha_str)
            metric.set('name', f'{node_name}_{classnames[r]}_QLen')
            metric.set('nodeType', 'station')
            metric.set('precision', str(options.max_rel_err))
            metric.set('referenceNode', node_name)
            metric.set('referenceUserClass', classnames[r])
            metric.set('type', 'Number of Customers')
            metric.set('verbose', 'false')

            # Response time
            metric = ET.SubElement(sim, 'measure')
            metric.set('alpha', alpha_str)
            metric.set('name', f'{node_name}_{classnames[r]}_RespT')
            metric.set('nodeType', 'station')
            metric.set('precision', str(options.max_rel_err))
            metric.set('referenceNode', node_name)
            metric.set('referenceUserClass', classnames[r])
            metric.set('type', 'Response Time')
            metric.set('verbose', 'false')

            # Utilization
            metric = ET.SubElement(sim, 'measure')
            metric.set('alpha', alpha_str)
            metric.set('name', f'{node_name}_{classnames[r]}_Util')
            metric.set('nodeType', 'station')
            metric.set('precision', str(options.max_rel_err))
            metric.set('referenceNode', node_name)
            metric.set('referenceUserClass', classnames[r])
            metric.set('type', 'Utilization')
            metric.set('verbose', 'false')

            # Throughput
            metric = ET.SubElement(sim, 'measure')
            metric.set('alpha', alpha_str)
            metric.set('name', f'{node_name}_{classnames[r]}_Tput')
            metric.set('nodeType', 'station')
            metric.set('precision', str(options.max_rel_err))
            metric.set('referenceNode', node_name)
            metric.set('referenceUserClass', classnames[r])
            metric.set('type', 'Throughput')
            metric.set('verbose', 'false')

    # Create connections (must come after metrics per JMT schema)
    # When class switching exists between i and j, route through ClassSwitch node:
    # i -> CS_i_to_j -> j instead of i -> j
    if sn.connmatrix is not None:
        for i in range(sn.nnodes):
            for j in range(sn.nnodes):
                if sn.connmatrix[i, j] > 0:
                    if (i, j) in cs_node_names:
                        # Route through ClassSwitch node
                        cs_name = cs_node_names[(i, j)]
                        # Connection: source -> ClassSwitch
                        conn = ET.SubElement(sim, 'connection')
                        conn.set('source', nodenames[i])
                        conn.set('target', cs_name)
                        # Connection: ClassSwitch -> dest
                        conn = ET.SubElement(sim, 'connection')
                        conn.set('source', cs_name)
                        conn.set('target', nodenames[j])
                    else:
                        # Direct connection (no class switching)
                        conn = ET.SubElement(sim, 'connection')
                        conn.set('source', nodenames[i])
                        conn.set('target', nodenames[j])

    # Add blocking regions (FCR - Finite Capacity Regions)
    # Reference: MATLAB saveRegions.m
    if model is not None:
        regions = []
        if hasattr(model, 'get_regions'):
            regions = model.get_regions()
        elif hasattr(model, 'regions'):
            regions = model.regions

        for r_idx, region in enumerate(regions):
            blocking_region = ET.SubElement(sim, 'blockingRegion')
            region_name = region.get_name() if hasattr(region, 'get_name') else f'FCRegion{r_idx + 1}'
            blocking_region.set('name', region_name)
            blocking_region.set('type', 'default')

            # 1. regionNode elements - nodes in this region
            region_nodes = region.nodes if hasattr(region, 'nodes') else []
            for node in region_nodes:
                node_name = node.get_name() if hasattr(node, 'get_name') else str(node)
                region_node = ET.SubElement(blocking_region, 'regionNode')
                region_node.set('nodeName', node_name)

            # 2. globalConstraint
            global_constraint = ET.SubElement(blocking_region, 'globalConstraint')
            global_max = region.global_max_jobs if hasattr(region, 'global_max_jobs') else -1
            global_constraint.set('maxJobs', str(global_max))

            # 3. globalMemoryConstraint
            global_mem_constraint = ET.SubElement(blocking_region, 'globalMemoryConstraint')
            global_max_mem = region.global_max_memory if hasattr(region, 'global_max_memory') else -1
            global_mem_constraint.set('maxMemory', str(global_max_mem))

            # Get classes from region or sn
            region_classes = region.classes if hasattr(region, 'classes') else []

            # 4. classConstraint elements
            for job_class in region_classes:
                class_name = job_class.get_name() if hasattr(job_class, 'get_name') else str(job_class)
                class_max_jobs = region.get_class_max_jobs(job_class) if hasattr(region, 'get_class_max_jobs') else -1

                # Only write if not unbounded (-1)
                if class_max_jobs != -1:
                    class_constraint = ET.SubElement(blocking_region, 'classConstraint')
                    class_constraint.set('jobClass', class_name)
                    class_constraint.set('maxJobsPerClass', str(class_max_jobs))

            # 5. classMemoryConstraint elements
            for job_class in region_classes:
                class_name = job_class.get_name() if hasattr(job_class, 'get_name') else str(job_class)
                class_max_mem = region.get_class_max_memory(job_class) if hasattr(region, 'get_class_max_memory') else -1

                # Only write if not unbounded (-1)
                if class_max_mem != -1:
                    class_mem_constraint = ET.SubElement(blocking_region, 'classMemoryConstraint')
                    class_mem_constraint.set('jobClass', class_name)
                    class_mem_constraint.set('maxMemoryPerClass', str(class_max_mem))

            # 6. dropRules elements - always write for each class
            for job_class in region_classes:
                class_name = job_class.get_name() if hasattr(job_class, 'get_name') else str(job_class)
                drop_rule = region.get_drop_rule(job_class) if hasattr(region, 'get_drop_rule') else None

                drop_rules = ET.SubElement(blocking_region, 'dropRules')
                drop_rules.set('jobClass', class_name)

                # Determine if DROP or WAITQ
                if drop_rule is not None:
                    # Check if it's DROP strategy
                    is_drop = False
                    if hasattr(drop_rule, 'name'):
                        is_drop = drop_rule.name == 'DROP'
                    elif hasattr(drop_rule, 'value'):
                        is_drop = drop_rule.value == 1  # DROP = 1
                    elif drop_rule is True:
                        is_drop = True
                    drop_rules.set('dropThisClass', 'true' if is_drop else 'false')
                else:
                    drop_rules.set('dropThisClass', 'false')

            # 7. classSize elements (only if not default value of 1)
            for job_class in region_classes:
                class_name = job_class.get_name() if hasattr(job_class, 'get_name') else str(job_class)
                class_size = region.get_class_size(job_class) if hasattr(region, 'get_class_size') else 1

                if class_size != 1:
                    class_size_elem = ET.SubElement(blocking_region, 'classSize')
                    class_size_elem.set('jobClass', class_name)
                    class_size_elem.set('size', str(class_size))

    # Create preload section (MATLAB writeJSIM.m lines 145-185)
    # This is essential for:
    # - Closed networks: jobs must start at their reference stations
    # - SPNs with initial state: Places need initial token populations
    njobs = sn.njobs.flatten() if sn.njobs is not None else np.zeros(K)

    # Get initial state if available (for SPNs with Places)
    s0 = sn.state if hasattr(sn, 'state') and sn.state is not None else None
    stationToStateful = sn.stationToStateful if hasattr(sn, 'stationToStateful') else None

    # Check if we need preload section
    has_reference_nodes = False
    preload = ET.SubElement(sim, 'preload')

    # For each station (excluding Source and Join nodes)
    for ist in range(M):
        node_idx = int(sn.stationToNode[ist]) if sn.stationToNode is not None else ist
        node_type = int(sn.nodetype[node_idx]) if sn.nodetype is not None else -1

        # Skip Source (0) and Join (5) nodes
        if node_type == 0 or node_type == 5:
            continue

        node_name = nodenames[node_idx] if node_idx < len(nodenames) else f'Node{node_idx}'

        # Get initial population from state (like MATLAB's State.toMarginal)
        # For Places in SPNs, this gives the initial token counts
        nir = np.zeros(K)
        if s0 is not None and stationToStateful is not None:
            stateful_idx = int(stationToStateful[ist]) if ist < len(stationToStateful) else -1
            if stateful_idx >= 0 and stateful_idx < len(s0):
                state_i = np.asarray(s0[stateful_idx]).flatten()
                for r in range(min(K, len(state_i))):
                    nir[r] = state_i[r]

        # For closed classes, use reference station logic if state doesn't have jobs
        for r in range(K):
            if np.isfinite(njobs[r]) and njobs[r] > 0 and nir[r] == 0:
                # Check if this station is the reference station for class r
                ref_idx = int(refstat[r]) if r < len(refstat) else 0
                if ist == ref_idx:
                    # All jobs of this class start at reference station
                    nir[r] = njobs[r]

        # Build class populations for this station
        class_populations = []
        for r in range(K):
            # Skip closed classes with 0 jobs and no state population
            if np.isfinite(njobs[r]) and njobs[r] == 0 and nir[r] == 0:
                continue

            if nir[r] > 0:
                class_populations.append((classnames[r], int(round(nir[r]))))

        if class_populations:
            has_reference_nodes = True
            station_pop = ET.SubElement(preload, 'stationPopulations')
            station_pop.set('stationName', node_name)

            for class_name, pop in class_populations:
                class_pop = ET.SubElement(station_pop, 'classPopulation')
                class_pop.set('population', str(pop))
                class_pop.set('refClass', class_name)

    # Only keep preload section if we have reference nodes
    if not has_reference_nodes:
        sim.remove(preload)

    # Write to file
    xml_str = ET.tostring(archive, encoding='unicode')
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent='  ')

    with open(model_path, 'w') as f:
        f.write(pretty_xml)


def _write_source_node(node_elem: ET.Element, node_idx: int, sn: NetworkStruct, classnames: List[str],
                       cs_node_names: Optional[Dict[Tuple[int, int], str]] = None):
    """Write source node section."""
    doc = node_elem

    section = ET.SubElement(node_elem, 'section')
    section.set('className', 'RandomSource')

    param = ET.SubElement(section, 'parameter')
    param.set('array', 'true')
    param.set('classPath', 'jmt.engine.NetStrategies.ServiceStrategy')
    param.set('name', 'ServiceStrategy')

    ist = int(sn.nodeToStation[node_idx]) if hasattr(sn, 'nodeToStation') and sn.nodeToStation is not None and node_idx < len(sn.nodeToStation) else 0
    K = sn.nclasses

    for r in range(K):
        ref_class = ET.SubElement(param, 'refClass')
        ref_class.text = classnames[r]

        sub_param = ET.SubElement(param, 'subParameter')
        sub_param.set('classPath', 'jmt.engine.NetStrategies.ServiceStrategies.ServiceTimeStrategy')
        sub_param.set('name', 'ServiceTimeStrategy')

        njobs = sn.njobs.flatten() if sn.njobs is not None else np.zeros(K)
        if not np.isinf(njobs[r]):
            # Closed class - no arrivals at source
            value = ET.SubElement(sub_param, 'value')
            value.text = 'null'
        else:
            # Open class - check arrival distribution type
            rate = sn.rates[ist, r] if sn.rates is not None and ist < sn.rates.shape[0] and r < sn.rates.shape[1] else 1.0
            if np.isnan(rate) or rate <= 0:
                value = ET.SubElement(sub_param, 'value')
                value.text = 'null'
            else:
                # Get the process type for arrivals
                procid = None
                if hasattr(sn, 'procid') and sn.procid is not None:
                    try:
                        procid = sn.procid[ist][r]
                    except (IndexError, TypeError, KeyError):
                        pass

                # Handle Phase-Type distributions (PH, APH, Coxian)
                if procid in (ProcessType.PH, ProcessType.APH, ProcessType.COXIAN):
                    _write_phase_type_service_distribution(sub_param, sn, ist, r)
                elif procid == ProcessType.ERLANG:
                    # Erlang distribution
                    proc = None
                    if hasattr(sn, 'proc') and sn.proc is not None:
                        try:
                            proc = sn.proc[ist][r]
                        except (IndexError, TypeError, KeyError):
                            pass
                    phases = 2
                    if proc is not None and isinstance(proc, (list, tuple)) and len(proc) > 0:
                        T = np.asarray(proc[0], dtype=np.float64)
                        phases = T.shape[0] if T.ndim >= 1 else 2

                    distr = ET.SubElement(sub_param, 'subParameter')
                    distr.set('classPath', 'jmt.engine.random.Erlang')
                    distr.set('name', 'Erlang')

                    distr_par = ET.SubElement(sub_param, 'subParameter')
                    distr_par.set('classPath', 'jmt.engine.random.ErlangPar')
                    distr_par.set('name', 'distrPar')

                    alpha_param = ET.SubElement(distr_par, 'subParameter')
                    alpha_param.set('classPath', 'java.lang.Double')
                    alpha_param.set('name', 'alpha')
                    value = ET.SubElement(alpha_param, 'value')
                    value.text = str(rate * phases)

                    r_param = ET.SubElement(distr_par, 'subParameter')
                    r_param.set('classPath', 'java.lang.Long')
                    r_param.set('name', 'r')
                    value = ET.SubElement(r_param, 'value')
                    value.text = str(phases)
                elif procid == ProcessType.HYPEREXP:
                    # HyperExponential distribution
                    proc = None
                    if hasattr(sn, 'proc') and sn.proc is not None:
                        try:
                            proc = sn.proc[ist][r]
                        except (IndexError, TypeError, KeyError):
                            pass
                    pie = None
                    if hasattr(sn, 'pie') and sn.pie is not None:
                        try:
                            pie = sn.pie[ist][r]
                        except (IndexError, TypeError, KeyError):
                            pass

                    # Extract HyperExp parameters
                    p = 0.5
                    lambda1 = rate
                    lambda2 = rate
                    if proc is not None and isinstance(proc, (list, tuple)) and len(proc) >= 1:
                        T = np.asarray(proc[0], dtype=np.float64)
                        if T.shape[0] >= 2:
                            lambda1 = -T[0, 0] if T[0, 0] < 0 else rate
                            lambda2 = -T[1, 1] if T[1, 1] < 0 else rate
                    if pie is not None:
                        alpha = np.asarray(pie, dtype=np.float64).flatten()
                        if len(alpha) > 0:
                            p = alpha[0]

                    distr = ET.SubElement(sub_param, 'subParameter')
                    distr.set('classPath', 'jmt.engine.random.HyperExp')
                    distr.set('name', 'Hyperexponential')

                    distr_par = ET.SubElement(sub_param, 'subParameter')
                    distr_par.set('classPath', 'jmt.engine.random.HyperExpPar')
                    distr_par.set('name', 'distrPar')

                    p_param = ET.SubElement(distr_par, 'subParameter')
                    p_param.set('classPath', 'java.lang.Double')
                    p_param.set('name', 'p')
                    value = ET.SubElement(p_param, 'value')
                    value.text = str(p)

                    l1_param = ET.SubElement(distr_par, 'subParameter')
                    l1_param.set('classPath', 'java.lang.Double')
                    l1_param.set('name', 'lambda1')
                    value = ET.SubElement(l1_param, 'value')
                    value.text = str(lambda1)

                    l2_param = ET.SubElement(distr_par, 'subParameter')
                    l2_param.set('classPath', 'java.lang.Double')
                    l2_param.set('name', 'lambda2')
                    value = ET.SubElement(l2_param, 'value')
                    value.text = str(lambda2)
                elif procid == ProcessType.DET:
                    # Deterministic distribution
                    distr = ET.SubElement(sub_param, 'subParameter')
                    distr.set('classPath', 'jmt.engine.random.DeterministicDistr')
                    distr.set('name', 'Deterministic')

                    distr_par = ET.SubElement(sub_param, 'subParameter')
                    distr_par.set('classPath', 'jmt.engine.random.DeterministicDistrPar')
                    distr_par.set('name', 'distrPar')

                    t_param = ET.SubElement(distr_par, 'subParameter')
                    t_param.set('classPath', 'java.lang.Double')
                    t_param.set('name', 't')
                    value = ET.SubElement(t_param, 'value')
                    value.text = str(1.0 / rate) if rate > 0 else '0.0'
                else:
                    # Default: Exponential distribution
                    distr = ET.SubElement(sub_param, 'subParameter')
                    distr.set('classPath', 'jmt.engine.random.Exponential')
                    distr.set('name', 'Exponential')

                    distr_par = ET.SubElement(sub_param, 'subParameter')
                    distr_par.set('classPath', 'jmt.engine.random.ExponentialPar')
                    distr_par.set('name', 'distrPar')

                    lambda_param = ET.SubElement(distr_par, 'subParameter')
                    lambda_param.set('classPath', 'java.lang.Double')
                    lambda_param.set('name', 'lambda')
                    value = ET.SubElement(lambda_param, 'value')
                    value.text = str(rate)

    # ServiceTunnel and Router sections
    tunnel = ET.SubElement(node_elem, 'section')
    tunnel.set('className', 'ServiceTunnel')

    router = ET.SubElement(node_elem, 'section')
    router.set('className', 'Router')
    _write_routing_strategy(router, node_idx, sn, classnames, cs_node_names)


def _write_sink_node(node_elem: ET.Element, sn: NetworkStruct, classnames: List[str]):
    """Write sink node section."""
    section = ET.SubElement(node_elem, 'section')
    section.set('className', 'JobSink')


def _write_delay_node(node_elem: ET.Element, node_idx: int, sn: NetworkStruct, classnames: List[str],
                      cs_node_names: Optional[Dict[Tuple[int, int], str]] = None):
    """Write delay station node.

    Delay nodes (infinite servers) in JMT need:
    1. Queue section (input buffer)
    2. Delay section (service strategy)
    3. Router section (routing)
    """
    K = sn.nclasses
    ist = int(sn.nodeToStation[node_idx]) if hasattr(sn, 'nodeToStation') and sn.nodeToStation is not None and node_idx < len(sn.nodeToStation) else 0

    # Queue section (input buffer)
    queue = ET.SubElement(node_elem, 'section')
    queue.set('className', 'Queue')

    size_param = ET.SubElement(queue, 'parameter')
    size_param.set('classPath', 'java.lang.Integer')
    size_param.set('name', 'size')
    value = ET.SubElement(size_param, 'value')
    value.text = '-1'

    # Drop strategies
    drop_strategy = ET.SubElement(queue, 'parameter')
    drop_strategy.set('array', 'true')
    drop_strategy.set('classPath', 'java.lang.String')
    drop_strategy.set('name', 'dropStrategies')

    for r in range(K):
        ref_class = ET.SubElement(drop_strategy, 'refClass')
        ref_class.text = classnames[r]

        sub_param = ET.SubElement(drop_strategy, 'subParameter')
        sub_param.set('classPath', 'java.lang.String')
        sub_param.set('name', 'dropStrategy')
        value = ET.SubElement(sub_param, 'value')
        value.text = 'waiting queue'  # Match Java format

    # Queue get strategy (FCFS)
    strategy_param = ET.SubElement(queue, 'parameter')
    strategy_param.set('classPath', 'jmt.engine.NetStrategies.QueueGetStrategies.FCFSstrategy')
    strategy_param.set('name', 'FCFSstrategy')

    # Queue put strategy
    put_strategy = ET.SubElement(queue, 'parameter')
    put_strategy.set('array', 'true')
    put_strategy.set('classPath', 'jmt.engine.NetStrategies.QueuePutStrategy')
    put_strategy.set('name', 'QueuePutStrategy')

    for r in range(K):
        ref_class = ET.SubElement(put_strategy, 'refClass')
        ref_class.text = classnames[r]

        sub_param = ET.SubElement(put_strategy, 'subParameter')
        sub_param.set('classPath', 'jmt.engine.NetStrategies.QueuePutStrategies.TailStrategy')
        sub_param.set('name', 'TailStrategy')

    # Delay section (service)
    server = ET.SubElement(node_elem, 'section')
    server.set('className', 'Delay')

    service_param = ET.SubElement(server, 'parameter')
    service_param.set('array', 'true')
    service_param.set('classPath', 'jmt.engine.NetStrategies.ServiceStrategy')
    service_param.set('name', 'ServiceStrategy')

    for r in range(K):
        ref_class = ET.SubElement(service_param, 'refClass')
        ref_class.text = classnames[r]

        sub_param = ET.SubElement(service_param, 'subParameter')
        sub_param.set('classPath', 'jmt.engine.NetStrategies.ServiceStrategies.ServiceTimeStrategy')
        sub_param.set('name', 'ServiceTimeStrategy')

        rate = sn.rates[ist, r] if sn.rates is not None and ist < sn.rates.shape[0] and r < sn.rates.shape[1] else 1.0
        if np.isnan(rate) or rate < 0:
            # Disabled service - null
            value = ET.SubElement(sub_param, 'value')
            value.text = 'null'
        elif rate == 0:
            # Immediate service (zero service time)
            sub_param.set('classPath', 'jmt.engine.NetStrategies.ServiceStrategies.ZeroServiceTimeStrategy')
            sub_param.set('name', 'ZeroServiceTimeStrategy')
        else:
            distr = ET.SubElement(sub_param, 'subParameter')
            distr.set('classPath', 'jmt.engine.random.Exponential')
            distr.set('name', 'Exponential')

            distr_par = ET.SubElement(sub_param, 'subParameter')
            distr_par.set('classPath', 'jmt.engine.random.ExponentialPar')
            distr_par.set('name', 'distrPar')

            lambda_param = ET.SubElement(distr_par, 'subParameter')
            lambda_param.set('classPath', 'java.lang.Double')
            lambda_param.set('name', 'lambda')
            value = ET.SubElement(lambda_param, 'value')
            value.text = str(rate)

    # Router section
    router = ET.SubElement(node_elem, 'section')
    router.set('className', 'Router')
    _write_routing_strategy(router, node_idx, sn, classnames, cs_node_names)


def _write_queue_node(node_elem: ET.Element, node_idx: int, sn: NetworkStruct, classnames: List[str],
                      options: SolverJMTOptions, cs_node_names: Optional[Dict[Tuple[int, int], str]] = None):
    """Write queue station node."""
    K = sn.nclasses
    ist = int(sn.nodeToStation[node_idx]) if hasattr(sn, 'nodeToStation') and sn.nodeToStation is not None and node_idx < len(sn.nodeToStation) else 0

    # Get scheduling strategy
    sched = SchedStrategy.FCFS
    if sn.sched and ist in sn.sched:
        sched = sn.sched[ist]

    # Queue section
    queue = ET.SubElement(node_elem, 'section')
    queue.set('className', 'Queue')

    # 1. Size parameter (queue capacity)
    # LINE uses Kendall notation where cap = K = total system capacity
    # JMT's "size" parameter represents total capacity K (-1 means infinite)
    size_param = ET.SubElement(queue, 'parameter')
    size_param.set('classPath', 'java.lang.Integer')
    size_param.set('name', 'size')
    value = ET.SubElement(size_param, 'value')
    capacity = -1  # Default: infinite capacity
    if hasattr(sn, 'cap') and sn.cap is not None and ist < len(sn.cap):
        cap_val = sn.cap[ist]
        if not np.isinf(cap_val):
            capacity = int(cap_val)
    value.text = str(capacity)

    # 2. Drop strategies (required)
    drop_strategy = ET.SubElement(queue, 'parameter')
    drop_strategy.set('array', 'true')
    drop_strategy.set('classPath', 'java.lang.String')
    drop_strategy.set('name', 'dropStrategies')

    for r in range(K):
        ref_class = ET.SubElement(drop_strategy, 'refClass')
        ref_class.text = classnames[r]

        sub_param = ET.SubElement(drop_strategy, 'subParameter')
        sub_param.set('classPath', 'java.lang.String')
        sub_param.set('name', 'dropStrategy')
        value = ET.SubElement(sub_param, 'value')
        # Check if there's a drop rule defined in sn.droprule
        drop_text = 'drop'  # Default to drop for finite capacity
        if hasattr(sn, 'droprule') and sn.droprule is not None:
            if ist < sn.droprule.shape[0] and r < sn.droprule.shape[1]:
                drop_val = sn.droprule[ist, r]
                if drop_val == 0 or np.isnan(drop_val):
                    drop_text = 'drop'
                elif drop_val == 1:  # WAITQ
                    drop_text = 'waiting queue'
                else:
                    drop_text = 'drop'
        value.text = drop_text

    # 3. Queue get strategy
    # Check if this is a polling queue
    is_polling_queue = False
    polling_type = None
    polling_k = 1

    if sched == SchedStrategy.POLLING and sn.nodeparam and node_idx in sn.nodeparam:
        nodeparam = sn.nodeparam[node_idx]
        if isinstance(nodeparam, dict):
            # Get polling type from first class that has it
            for r in range(K):
                if r in nodeparam and isinstance(nodeparam[r], dict):
                    if 'pollingType' in nodeparam[r]:
                        is_polling_queue = True
                        polling_type = nodeparam[r]['pollingType']
                        polling_par = nodeparam[r].get('pollingPar', [1])
                        polling_k = polling_par[0] if polling_par else 1
                        break

    if is_polling_queue and polling_type is not None:
        _write_polling_get_strategy(queue, polling_type, polling_k)
    else:
        strategy_param = ET.SubElement(queue, 'parameter')
        strategy_param.set('classPath', _get_sched_strategy_class(sched))
        strategy_param.set('name', 'FCFSstrategy')

    # 4. Queue put strategy
    put_strategy = ET.SubElement(queue, 'parameter')
    put_strategy.set('array', 'true')
    put_strategy.set('classPath', 'jmt.engine.NetStrategies.QueuePutStrategy')
    put_strategy.set('name', 'QueuePutStrategy')

    for r in range(K):
        ref_class = ET.SubElement(put_strategy, 'refClass')
        ref_class.text = classnames[r]

        # TailStrategy for FCFS (default)
        sub_param = ET.SubElement(put_strategy, 'subParameter')
        sub_param.set('classPath', 'jmt.engine.NetStrategies.QueuePutStrategies.TailStrategy')
        sub_param.set('name', 'TailStrategy')

    # Server section
    server = ET.SubElement(node_elem, 'section')
    # Use PSServer for processor sharing variants (PS, DPS, GPS)
    # Use PollingServer variants for POLLING scheduling
    if sched in (SchedStrategy.PS, SchedStrategy.DPS, SchedStrategy.GPS):
        server.set('className', 'PSServer')
    elif sched == SchedStrategy.POLLING and is_polling_queue and polling_type is not None:
        # Use appropriate polling server class based on polling type
        if polling_type == PollingType.GATED:
            server.set('className', 'GatedPollingServer')
        elif polling_type == PollingType.EXHAUSTIVE:
            server.set('className', 'ExhaustivePollingServer')
        elif polling_type == PollingType.KLIMITED:
            server.set('className', 'LimitedPollingServer')
        else:
            server.set('className', 'ExhaustivePollingServer')  # Default
    else:
        server.set('className', 'Server')

    # Number of servers
    nservers = 1
    if sn.nservers is not None:
        nservers_val = sn.nservers[ist] if len(sn.nservers.shape) == 1 else sn.nservers[ist, 0]
        if np.isinf(nservers_val):
            nservers = 1000000  # Very large number for infinite servers
        else:
            nservers = int(nservers_val)

    servers_param = ET.SubElement(server, 'parameter')
    servers_param.set('classPath', 'java.lang.Integer')
    servers_param.set('name', 'maxJobs')
    value = ET.SubElement(servers_param, 'value')
    value.text = str(nservers)

    # Number of visits
    visits_param = ET.SubElement(server, 'parameter')
    visits_param.set('array', 'true')
    visits_param.set('classPath', 'java.lang.Integer')
    visits_param.set('name', 'numberOfVisits')

    for r in range(K):
        ref_class = ET.SubElement(visits_param, 'refClass')
        ref_class.text = classnames[r]

        sub_param = ET.SubElement(visits_param, 'subParameter')
        sub_param.set('classPath', 'java.lang.Integer')
        sub_param.set('name', 'numberOfVisits')
        value = ET.SubElement(sub_param, 'value')
        value.text = '1'

    # Service strategy
    service_param = ET.SubElement(server, 'parameter')
    service_param.set('array', 'true')
    service_param.set('classPath', 'jmt.engine.NetStrategies.ServiceStrategy')
    service_param.set('name', 'ServiceStrategy')

    for r in range(K):
        ref_class = ET.SubElement(service_param, 'refClass')
        ref_class.text = classnames[r]

        sub_param = ET.SubElement(service_param, 'subParameter')
        sub_param.set('classPath', 'jmt.engine.NetStrategies.ServiceStrategies.ServiceTimeStrategy')
        sub_param.set('name', 'ServiceTimeStrategy')

        rate = sn.rates[ist, r] if sn.rates is not None and ist < sn.rates.shape[0] and r < sn.rates.shape[1] else 1.0

        # Get process type
        procid = None
        if hasattr(sn, 'procid') and sn.procid is not None:
            if ist < sn.procid.shape[0] and r < sn.procid.shape[1]:
                procid = sn.procid[ist, r]

        if np.isnan(rate) or rate < 0:
            # Disabled service - null
            value = ET.SubElement(sub_param, 'value')
            value.text = 'null'
        elif rate == 0:
            # Immediate service (zero service time)
            sub_param.set('classPath', 'jmt.engine.NetStrategies.ServiceStrategies.ZeroServiceTimeStrategy')
            sub_param.set('name', 'ZeroServiceTimeStrategy')
        elif procid in (ProcessType.MAP, ProcessType.MMPP2):
            # MAP/MMPP2 distribution
            _write_map_service_distribution(sub_param, sn, ist, r)
        elif procid == ProcessType.ERLANG:
            # Erlang distribution
            distr = ET.SubElement(sub_param, 'subParameter')
            distr.set('classPath', 'jmt.engine.random.Erlang')
            distr.set('name', 'Erlang')

            distr_par = ET.SubElement(sub_param, 'subParameter')
            distr_par.set('classPath', 'jmt.engine.random.ErlangPar')
            distr_par.set('name', 'distrPar')

            # Get number of phases from sn.proc or sn.phases
            phases = 1
            # First try sn.proc[ist][r]['k'] (Python stores Erlang info there)
            if hasattr(sn, 'proc') and sn.proc is not None:
                try:
                    proc_entry = sn.proc[ist][r]
                    if isinstance(proc_entry, dict) and 'k' in proc_entry:
                        phases = int(proc_entry['k'])
                except (IndexError, TypeError, KeyError):
                    pass
            # Fallback to sn.phases if available
            if phases == 1 and hasattr(sn, 'phases') and sn.phases is not None:
                if ist < sn.phases.shape[0] and r < sn.phases.shape[1]:
                    phases = int(sn.phases[ist, r])

            # Alpha = rate * phases (MATLAB: sn.rates(i,r)*sn.phases(i,r))
            alpha_param = ET.SubElement(distr_par, 'subParameter')
            alpha_param.set('classPath', 'java.lang.Double')
            alpha_param.set('name', 'alpha')
            value = ET.SubElement(alpha_param, 'value')
            value.text = str(rate * phases)

            # r = number of phases
            r_param = ET.SubElement(distr_par, 'subParameter')
            r_param.set('classPath', 'java.lang.Long')
            r_param.set('name', 'r')
            value = ET.SubElement(r_param, 'value')
            value.text = str(phases)
        elif procid == ProcessType.HYPEREXP:
            # HyperExponential distribution - check if 2-phase or use phase-type
            phases = 1
            if hasattr(sn, 'phases') and sn.phases is not None:
                if ist < sn.phases.shape[0] and r < sn.phases.shape[1]:
                    phases = int(sn.phases[ist, r])

            if phases <= 2:
                # 2-phase HyperExp
                distr = ET.SubElement(sub_param, 'subParameter')
                distr.set('classPath', 'jmt.engine.random.HyperExp')
                distr.set('name', 'Hyperexponential')

                distr_par = ET.SubElement(sub_param, 'subParameter')
                distr_par.set('classPath', 'jmt.engine.random.HyperExpPar')
                distr_par.set('name', 'distrPar')

                # Get pie (phase probabilities) and proc (phase rates)
                p = 0.5  # Default
                lambda1 = rate
                lambda2 = rate
                if hasattr(sn, 'pie') and sn.pie is not None and ist in sn.pie and r in sn.pie[ist]:
                    pie = sn.pie[ist][r]
                    if len(pie) >= 1:
                        p = pie[0]
                if hasattr(sn, 'proc') and sn.proc is not None and ist in sn.proc and r in sn.proc[ist]:
                    proc = sn.proc[ist][r]
                    if proc is not None and len(proc) >= 1:
                        T = proc[0]
                        if hasattr(T, 'shape') and T.shape[0] >= 2:
                            lambda1 = -T[0, 0]
                            lambda2 = -T[1, 1]

                p_param = ET.SubElement(distr_par, 'subParameter')
                p_param.set('classPath', 'java.lang.Double')
                p_param.set('name', 'p')
                value = ET.SubElement(p_param, 'value')
                value.text = str(p)

                lambda1_param = ET.SubElement(distr_par, 'subParameter')
                lambda1_param.set('classPath', 'java.lang.Double')
                lambda1_param.set('name', 'lambda1')
                value = ET.SubElement(lambda1_param, 'value')
                value.text = str(lambda1)

                lambda2_param = ET.SubElement(distr_par, 'subParameter')
                lambda2_param.set('classPath', 'java.lang.Double')
                lambda2_param.set('name', 'lambda2')
                value = ET.SubElement(lambda2_param, 'value')
                value.text = str(lambda2)
            else:
                # More than 2 phases - use phase-type representation
                _write_phase_type_service_distribution(sub_param, sn, ist, r)
        elif procid in (ProcessType.PH, ProcessType.APH, ProcessType.COXIAN):
            # Phase-type distributions
            _write_phase_type_service_distribution(sub_param, sn, ist, r)
        else:
            # Default: Exponential distribution
            distr = ET.SubElement(sub_param, 'subParameter')
            distr.set('classPath', 'jmt.engine.random.Exponential')
            distr.set('name', 'Exponential')

            distr_par = ET.SubElement(sub_param, 'subParameter')
            distr_par.set('classPath', 'jmt.engine.random.ExponentialPar')
            distr_par.set('name', 'distrPar')

            lambda_param = ET.SubElement(distr_par, 'subParameter')
            lambda_param.set('classPath', 'java.lang.Double')
            lambda_param.set('name', 'lambda')
            value = ET.SubElement(lambda_param, 'value')
            value.text = str(rate)

    # PSStrategy (for PS/DPS/GPS scheduling)
    if sched in (SchedStrategy.PS, SchedStrategy.DPS, SchedStrategy.GPS):
        ps_strategy_param = ET.SubElement(server, 'parameter')
        ps_strategy_param.set('array', 'true')
        ps_strategy_param.set('classPath', 'jmt.engine.NetStrategies.PSStrategy')
        ps_strategy_param.set('name', 'PSStrategy')

        for r in range(K):
            ref_class = ET.SubElement(ps_strategy_param, 'refClass')
            ref_class.text = classnames[r]

            sub_param = ET.SubElement(ps_strategy_param, 'subParameter')
            if sched == SchedStrategy.PS:
                sub_param.set('classPath', 'jmt.engine.NetStrategies.PSStrategies.EPSStrategy')
                sub_param.set('name', 'EPSStrategy')
            elif sched == SchedStrategy.DPS:
                sub_param.set('classPath', 'jmt.engine.NetStrategies.PSStrategies.DPSStrategy')
                sub_param.set('name', 'DPSStrategy')
            elif sched == SchedStrategy.GPS:
                sub_param.set('classPath', 'jmt.engine.NetStrategies.PSStrategies.GPSStrategy')
                sub_param.set('name', 'GPSStrategy')

    # Service weights (required for PSServer - PS/DPS/GPS scheduling)
    if sched in (SchedStrategy.PS, SchedStrategy.DPS, SchedStrategy.GPS):
        weights_param = ET.SubElement(server, 'parameter')
        weights_param.set('array', 'true')
        weights_param.set('classPath', 'java.lang.Double')
        weights_param.set('name', 'serviceWeights')

        for r in range(K):
            ref_class = ET.SubElement(weights_param, 'refClass')
            ref_class.text = classnames[r]

            sub_param = ET.SubElement(weights_param, 'subParameter')
            sub_param.set('classPath', 'java.lang.Double')
            sub_param.set('name', 'serviceWeight')
            value = ET.SubElement(sub_param, 'value')
            # Get weight from schedparam (for DPS/GPS), default to 1 for PS
            weight = 1.0
            if sched in (SchedStrategy.DPS, SchedStrategy.GPS):
                if hasattr(sn, 'schedparam') and sn.schedparam is not None:
                    if ist < sn.schedparam.shape[0] and r < sn.schedparam.shape[1]:
                        w = sn.schedparam[ist, r]
                        if not np.isnan(w) and w > 0:
                            weight = w
            value.text = str(weight)

    # Switchover strategy for polling queues
    if sched == SchedStrategy.POLLING:
        _write_switchover_strategy(server, node_idx, sn, classnames)
    else:
        # Check if switchover times are defined for non-polling queues and warn
        has_switchover = False
        if sn.nodeparam and node_idx in sn.nodeparam:
            nodeparam = sn.nodeparam[node_idx]
            if isinstance(nodeparam, dict):
                for r in range(K):
                    if r in nodeparam and isinstance(nodeparam[r], dict):
                        if 'switchoverTime' in nodeparam[r] and nodeparam[r]['switchoverTime']:
                            has_switchover = True
                            break
        if has_switchover:
            import warnings
            node_name = sn.nodenames[node_idx] if hasattr(sn, 'nodenames') and node_idx < len(sn.nodenames) else f"node {node_idx}"
            warnings.warn(f"JMT does not support switchover times for non-polling queues. "
                         f"Switchover times will be ignored for {node_name}.")

    # Router section
    router = ET.SubElement(node_elem, 'section')
    router.set('className', 'Router')
    _write_routing_strategy(router, node_idx, sn, classnames, cs_node_names)


def _write_router_node(node_elem: ET.Element, node_idx: int, sn: NetworkStruct, classnames: List[str],
                       cs_node_names: Optional[Dict[Tuple[int, int], str]] = None):
    """Write router node section.

    Router nodes in JMT need:
    1. Queue (input section - buffer)
    2. ServiceTunnel (middle section - pass-through)
    3. Router (output section with routing strategy)
    """
    K = sn.nclasses

    # 1. Queue section (input buffer)
    queue = ET.SubElement(node_elem, 'section')
    queue.set('className', 'Queue')

    size_param = ET.SubElement(queue, 'parameter')
    size_param.set('classPath', 'java.lang.Integer')
    size_param.set('name', 'size')
    value = ET.SubElement(size_param, 'value')
    value.text = '-1'  # Infinite capacity

    # Drop strategies
    drop_strategy = ET.SubElement(queue, 'parameter')
    drop_strategy.set('array', 'true')
    drop_strategy.set('classPath', 'java.lang.String')
    drop_strategy.set('name', 'dropStrategies')

    for r in range(K):
        ref_class = ET.SubElement(drop_strategy, 'refClass')
        ref_class.text = classnames[r]

        sub_param = ET.SubElement(drop_strategy, 'subParameter')
        sub_param.set('classPath', 'java.lang.String')
        sub_param.set('name', 'dropStrategy')
        value = ET.SubElement(sub_param, 'value')
        value.text = 'drop'

    # Queue get strategy (FCFS)
    strategy_param = ET.SubElement(queue, 'parameter')
    strategy_param.set('classPath', 'jmt.engine.NetStrategies.QueueGetStrategies.FCFSstrategy')
    strategy_param.set('name', 'FCFSstrategy')

    # Queue put strategy
    put_strategy = ET.SubElement(queue, 'parameter')
    put_strategy.set('array', 'true')
    put_strategy.set('classPath', 'jmt.engine.NetStrategies.QueuePutStrategy')
    put_strategy.set('name', 'QueuePutStrategy')

    for r in range(K):
        ref_class = ET.SubElement(put_strategy, 'refClass')
        ref_class.text = classnames[r]

        sub_param = ET.SubElement(put_strategy, 'subParameter')
        sub_param.set('classPath', 'jmt.engine.NetStrategies.QueuePutStrategies.TailStrategy')
        sub_param.set('name', 'TailStrategy')

    # 2. ServiceTunnel section (pass-through)
    tunnel = ET.SubElement(node_elem, 'section')
    tunnel.set('className', 'ServiceTunnel')

    # 3. Router section
    router = ET.SubElement(node_elem, 'section')
    router.set('className', 'Router')
    _write_routing_strategy(router, node_idx, sn, classnames, cs_node_names)


def _write_classswitch_node(node_elem: ET.Element, node_idx: int, sn: NetworkStruct, classnames: List[str]):
    """Write ClassSwitch node section.

    ClassSwitch nodes in JMT need:
    1. Queue (input section - buffer)
    2. ClassSwitch (middle section - class switching matrix)
    3. Router (output section with routing strategy)
    """
    K = sn.nclasses

    # 1. Queue section (input buffer)
    queue = ET.SubElement(node_elem, 'section')
    queue.set('className', 'Queue')

    size_param = ET.SubElement(queue, 'parameter')
    size_param.set('classPath', 'java.lang.Integer')
    size_param.set('name', 'size')
    value = ET.SubElement(size_param, 'value')
    value.text = '-1'  # Infinite capacity

    # Drop strategies
    drop_strategy = ET.SubElement(queue, 'parameter')
    drop_strategy.set('array', 'true')
    drop_strategy.set('classPath', 'java.lang.String')
    drop_strategy.set('name', 'dropStrategies')

    for r in range(K):
        ref_class = ET.SubElement(drop_strategy, 'refClass')
        ref_class.text = classnames[r]

        sub_param = ET.SubElement(drop_strategy, 'subParameter')
        sub_param.set('classPath', 'java.lang.String')
        sub_param.set('name', 'dropStrategy')
        value = ET.SubElement(sub_param, 'value')
        value.text = 'drop'

    # Queue get strategy (FCFS)
    strategy_param = ET.SubElement(queue, 'parameter')
    strategy_param.set('classPath', 'jmt.engine.NetStrategies.QueueGetStrategies.FCFSstrategy')
    strategy_param.set('name', 'FCFSstrategy')

    # Queue put strategy
    put_strategy = ET.SubElement(queue, 'parameter')
    put_strategy.set('array', 'true')
    put_strategy.set('classPath', 'jmt.engine.NetStrategies.QueuePutStrategy')
    put_strategy.set('name', 'QueuePutStrategy')

    for r in range(K):
        ref_class = ET.SubElement(put_strategy, 'refClass')
        ref_class.text = classnames[r]

        sub_param = ET.SubElement(put_strategy, 'subParameter')
        sub_param.set('classPath', 'jmt.engine.NetStrategies.QueuePutStrategies.TailStrategy')
        sub_param.set('name', 'TailStrategy')

    # 2. ClassSwitch section (class switching matrix)
    cs_section = ET.SubElement(node_elem, 'section')
    cs_section.set('className', 'ClassSwitch')

    # Build the class switching matrix
    matrix_param = ET.SubElement(cs_section, 'parameter')
    matrix_param.set('array', 'true')
    matrix_param.set('classPath', 'java.lang.Object')
    matrix_param.set('name', 'matrix')

    # Get connections from this node to determine destination nodes
    if sn.connmatrix is not None:
        conn_i = sn.connmatrix[node_idx, :]
        jset = np.where(conn_i > 0)[0]
    else:
        jset = np.array([])

    for r in range(K):
        ref_class = ET.SubElement(matrix_param, 'refClass')
        ref_class.text = classnames[r]

        row_param = ET.SubElement(matrix_param, 'subParameter')
        row_param.set('array', 'true')
        row_param.set('classPath', 'java.lang.Float')
        row_param.set('name', 'row')

        for s in range(K):
            ref_class_col = ET.SubElement(row_param, 'refClass')
            ref_class_col.text = classnames[s]

            cell_param = ET.SubElement(row_param, 'subParameter')
            cell_param.set('classPath', 'java.lang.Float')
            cell_param.set('name', 'cell')
            cell_value = ET.SubElement(cell_param, 'value')

            # Calculate class switching probability from rtnodes
            val = 0.0
            if sn.rtnodes is not None and len(jset) > 0:
                for j in jset:
                    src_idx = node_idx * K + r
                    dst_idx = int(j) * K + s
                    if src_idx < sn.rtnodes.shape[0] and dst_idx < sn.rtnodes.shape[1]:
                        val += sn.rtnodes[src_idx, dst_idx]
            elif r == s:
                # Default: keep same class
                val = 1.0
            cell_value.text = f'{val:.12f}'

    # 3. Router section
    router = ET.SubElement(node_elem, 'section')
    router.set('className', 'Router')
    _write_routing_strategy(router, node_idx, sn, classnames)


def _write_place_node(node_elem: ET.Element, node_idx: int, sn: NetworkStruct, classnames: List[str]):
    """Write Place node section for Petri nets.

    Place nodes in JMT use a Storage section.
    """
    K = sn.nclasses

    # Storage section
    storage = ET.SubElement(node_elem, 'section')
    storage.set('className', 'Storage')

    # Total capacity
    capacity_param = ET.SubElement(storage, 'parameter')
    capacity_param.set('classPath', 'java.lang.Integer')
    capacity_param.set('name', 'totalCapacity')
    value = ET.SubElement(capacity_param, 'value')
    value.text = '-1'  # Infinite capacity

    # Place capacities (per-class)
    place_cap = ET.SubElement(storage, 'parameter')
    place_cap.set('array', 'true')
    place_cap.set('classPath', 'java.lang.Integer')
    place_cap.set('name', 'capacities')

    for r in range(K):
        ref_class = ET.SubElement(place_cap, 'refClass')
        ref_class.text = classnames[r]

        sub_param = ET.SubElement(place_cap, 'subParameter')
        sub_param.set('classPath', 'java.lang.Integer')
        sub_param.set('name', 'capacity')
        value = ET.SubElement(sub_param, 'value')
        value.text = '-1'  # Infinite capacity

    # Drop rules - use 'waiting queue' for SPNs (matches MATLAB DropStrategy.WAITQ)
    drop_rules = ET.SubElement(storage, 'parameter')
    drop_rules.set('array', 'true')
    drop_rules.set('classPath', 'java.lang.String')
    drop_rules.set('name', 'dropRules')

    for r in range(K):
        ref_class = ET.SubElement(drop_rules, 'refClass')
        ref_class.text = classnames[r]

        sub_param = ET.SubElement(drop_rules, 'subParameter')
        sub_param.set('classPath', 'java.lang.String')
        sub_param.set('name', 'dropRule')
        value = ET.SubElement(sub_param, 'value')
        value.text = 'waiting queue'

    # Get strategy (FCFS)
    get_strategy = ET.SubElement(storage, 'parameter')
    get_strategy.set('classPath', 'jmt.engine.NetStrategies.QueueGetStrategies.FCFSstrategy')
    get_strategy.set('name', 'FCFSstrategy')

    # Put strategies - use QueuePutStrategy name to match MATLAB
    put_strategy = ET.SubElement(storage, 'parameter')
    put_strategy.set('array', 'true')
    put_strategy.set('classPath', 'jmt.engine.NetStrategies.QueuePutStrategy')
    put_strategy.set('name', 'QueuePutStrategy')

    for r in range(K):
        ref_class = ET.SubElement(put_strategy, 'refClass')
        ref_class.text = classnames[r]

        sub_param = ET.SubElement(put_strategy, 'subParameter')
        sub_param.set('classPath', 'jmt.engine.NetStrategies.QueuePutStrategies.TailStrategy')
        sub_param.set('name', 'TailStrategy')

    # 2. ServiceTunnel section (pass-through - tokens don't need service)
    tunnel = ET.SubElement(node_elem, 'section')
    tunnel.set('className', 'ServiceTunnel')

    # 3. Linkage section (for Places, not Router - JMT handles routing via connections)
    linkage = ET.SubElement(node_elem, 'section')
    linkage.set('className', 'Linkage')


def _write_transition_node(node_elem: ET.Element, node_idx: int, sn: NetworkStruct, classnames: List[str]):
    """Write Transition node section for Petri nets.

    Transition nodes in JMT have three sections:
    1. Enabling (enabling and inhibiting conditions)
    2. Timing (mode names, servers, timing strategies)
    3. Firing (firing outcomes)
    """
    K = sn.nclasses
    nodenames = sn.nodenames if sn.nodenames else [f'Node{i+1}' for i in range(sn.nnodes)]

    # Get transition parameters from nodeparam
    trans_param = None
    if hasattr(sn, 'nodeparam') and sn.nodeparam is not None:
        trans_param = sn.nodeparam.get(node_idx)

    # Defaults if no nodeparam
    nmodes = 1
    modenames = ['Mode1']
    firing_prio = [1]
    fire_weight = [1.0]
    nmodeservers = [1]
    enabling = [np.zeros((sn.nnodes, K))]
    inhibiting = [np.full((sn.nnodes, K), np.inf)]
    firing = [np.zeros((sn.nnodes, K))]

    if trans_param is not None:
        nmodes = getattr(trans_param, 'nmodes', 1)
        modenames = getattr(trans_param, 'modenames', ['Mode1'])
        firing_prio = getattr(trans_param, 'firingprio', [1])
        fire_weight = getattr(trans_param, 'fireweight', [1.0])
        nmodeservers = getattr(trans_param, 'nmodeservers', np.array([1]))
        enabling = getattr(trans_param, 'enabling', enabling)
        inhibiting = getattr(trans_param, 'inhibiting', inhibiting)
        firing = getattr(trans_param, 'firing', firing)

    # 1. Enabling section
    enabling_section = ET.SubElement(node_elem, 'section')
    enabling_section.set('className', 'Enabling')

    # Enabling conditions - uses TransitionMatrix structure
    enabling_param = ET.SubElement(enabling_section, 'parameter')
    enabling_param.set('array', 'true')
    enabling_param.set('classPath', 'jmt.engine.NetStrategies.TransitionUtilities.TransitionMatrix')
    enabling_param.set('name', 'enablingConditions')

    for m in range(nmodes):
        # Each mode has a TransitionMatrix
        mode_matrix = ET.SubElement(enabling_param, 'subParameter')
        mode_matrix.set('classPath', 'jmt.engine.NetStrategies.TransitionUtilities.TransitionMatrix')
        mode_matrix.set('name', 'enablingCondition')

        # enablingVectors array
        vectors = ET.SubElement(mode_matrix, 'subParameter')
        vectors.set('array', 'true')
        vectors.set('classPath', 'jmt.engine.NetStrategies.TransitionUtilities.TransitionVector')
        vectors.set('name', 'enablingVectors')

        for k in range(sn.nnodes):
            if sn.nodetype[k] != NodeType.PLACE:
                continue

            # Check if this place has relevant entries
            has_relevant = False
            for r in range(K):
                en_val = enabling[m][k, r] if m < len(enabling) else 0
                in_val = inhibiting[m][k, r] if m < len(inhibiting) else np.inf
                if (not np.isinf(en_val) and en_val > 0) or (not np.isinf(in_val) and in_val > 0):
                    has_relevant = True
                    break

            if not has_relevant:
                continue

            # Create vector for this place
            vector = ET.SubElement(vectors, 'subParameter')
            vector.set('classPath', 'jmt.engine.NetStrategies.TransitionUtilities.TransitionVector')
            vector.set('name', 'enablingVector')

            # Station name
            station_name = ET.SubElement(vector, 'subParameter')
            station_name.set('classPath', 'java.lang.String')
            station_name.set('name', 'stationName')
            value = ET.SubElement(station_name, 'value')
            value.text = nodenames[k]

            # Enabling entries array
            entries = ET.SubElement(vector, 'subParameter')
            entries.set('array', 'true')
            entries.set('classPath', 'java.lang.Integer')
            entries.set('name', 'enablingEntries')

            for r in range(K):
                ref_class = ET.SubElement(entries, 'refClass')
                ref_class.text = classnames[r]

                entry = ET.SubElement(entries, 'subParameter')
                entry.set('classPath', 'java.lang.Integer')
                entry.set('name', 'enablingEntry')
                val = ET.SubElement(entry, 'value')
                en_val = enabling[m][k, r] if m < len(enabling) else 0
                val.text = '-1' if np.isinf(en_val) else str(int(en_val))

    # Inhibiting conditions - MATLAB writes vectors for ALL input places (never skips)
    # and uses '0' for infinite inhibiting values (not '-1' like enabling)
    inhibiting_param = ET.SubElement(enabling_section, 'parameter')
    inhibiting_param.set('array', 'true')
    inhibiting_param.set('classPath', 'jmt.engine.NetStrategies.TransitionUtilities.TransitionMatrix')
    inhibiting_param.set('name', 'inhibitingConditions')

    # Get input places (nodes connected TO this transition)
    input_places = []
    if sn.connmatrix is not None:
        for k in range(sn.nnodes):
            if sn.connmatrix[k, node_idx] > 0 and sn.nodetype[k] == NodeType.PLACE:
                input_places.append(k)

    for m in range(nmodes):
        mode_matrix = ET.SubElement(inhibiting_param, 'subParameter')
        mode_matrix.set('classPath', 'jmt.engine.NetStrategies.TransitionUtilities.TransitionMatrix')
        mode_matrix.set('name', 'inhibitingCondition')

        vectors = ET.SubElement(mode_matrix, 'subParameter')
        vectors.set('array', 'true')
        vectors.set('classPath', 'jmt.engine.NetStrategies.TransitionUtilities.TransitionVector')
        vectors.set('name', 'inhibitingVectors')

        # Write vectors for ALL input places (no skipping)
        for k in input_places:
            vector = ET.SubElement(vectors, 'subParameter')
            vector.set('classPath', 'jmt.engine.NetStrategies.TransitionUtilities.TransitionVector')
            vector.set('name', 'inhibitingVector')

            station_name = ET.SubElement(vector, 'subParameter')
            station_name.set('classPath', 'java.lang.String')
            station_name.set('name', 'stationName')
            value = ET.SubElement(station_name, 'value')
            value.text = nodenames[k]

            entries = ET.SubElement(vector, 'subParameter')
            entries.set('array', 'true')
            entries.set('classPath', 'java.lang.Integer')
            entries.set('name', 'inhibitingEntries')

            for r in range(K):
                ref_class = ET.SubElement(entries, 'refClass')
                ref_class.text = classnames[r]

                entry = ET.SubElement(entries, 'subParameter')
                entry.set('classPath', 'java.lang.Integer')
                entry.set('name', 'inhibitingEntry')
                val = ET.SubElement(entry, 'value')
                in_val = inhibiting[m][k, r] if m < len(inhibiting) else np.inf
                # Use '0' for infinite inhibiting (matches MATLAB), unlike enabling which uses '-1'
                val.text = '0' if np.isinf(in_val) else str(int(in_val))

    # 2. Timing section
    timing_section = ET.SubElement(node_elem, 'section')
    timing_section.set('className', 'Timing')

    # Mode names
    modenames_param = ET.SubElement(timing_section, 'parameter')
    modenames_param.set('array', 'true')
    modenames_param.set('classPath', 'java.lang.String')
    modenames_param.set('name', 'modeNames')

    for m in range(nmodes):
        sub_param = ET.SubElement(modenames_param, 'subParameter')
        sub_param.set('classPath', 'java.lang.String')
        sub_param.set('name', 'modeName')
        value = ET.SubElement(sub_param, 'value')
        value.text = modenames[m]

    # Number of servers
    servers_param = ET.SubElement(timing_section, 'parameter')
    servers_param.set('array', 'true')
    servers_param.set('classPath', 'java.lang.Integer')
    servers_param.set('name', 'numbersOfServers')

    for m in range(nmodes):
        sub_param = ET.SubElement(servers_param, 'subParameter')
        sub_param.set('classPath', 'java.lang.Integer')
        sub_param.set('name', 'numberOfServers')
        value = ET.SubElement(sub_param, 'value')
        nservers_raw = nmodeservers[m] if m < len(nmodeservers) else 1
        if np.isinf(nservers_raw) or nservers_raw >= 1000000:
            value.text = '-1'  # JMT uses -1 for infinite servers
        else:
            value.text = str(int(nservers_raw))

    # Timing strategies
    timing_strat_param = ET.SubElement(timing_section, 'parameter')
    timing_strat_param.set('array', 'true')
    timing_strat_param.set('classPath', 'jmt.engine.NetStrategies.ServiceStrategy')
    timing_strat_param.set('name', 'timingStrategies')

    for m in range(nmodes):
        dist = None
        if trans_param is not None and hasattr(trans_param, 'distributions'):
            dists = trans_param.distributions
            if m < len(dists) and dists[m] is not None:
                dist = dists[m]

        if dist is not None:
            sub_param = ET.SubElement(timing_strat_param, 'subParameter')
            sub_param.set('classPath', 'jmt.engine.NetStrategies.ServiceStrategies.ServiceTimeStrategy')
            sub_param.set('name', 'timingStrategy')
            _write_distribution_param(sub_param, dist)
        else:
            sub_param = ET.SubElement(timing_strat_param, 'subParameter')
            sub_param.set('classPath', 'jmt.engine.NetStrategies.ServiceStrategies.ZeroServiceTimeStrategy')
            sub_param.set('name', 'ZeroServiceTimeStrategy')

    # Firing priorities
    prio_param = ET.SubElement(timing_section, 'parameter')
    prio_param.set('array', 'true')
    prio_param.set('classPath', 'java.lang.Integer')
    prio_param.set('name', 'firingPriorities')

    for m in range(nmodes):
        sub_param = ET.SubElement(prio_param, 'subParameter')
        sub_param.set('classPath', 'java.lang.Integer')
        sub_param.set('name', 'firingPriority')
        value = ET.SubElement(sub_param, 'value')
        value.text = str(int(firing_prio[m]) if m < len(firing_prio) else 1)

    # Firing weights
    weight_param = ET.SubElement(timing_section, 'parameter')
    weight_param.set('array', 'true')
    weight_param.set('classPath', 'java.lang.Double')
    weight_param.set('name', 'firingWeights')

    for m in range(nmodes):
        sub_param = ET.SubElement(weight_param, 'subParameter')
        sub_param.set('classPath', 'java.lang.Double')
        sub_param.set('name', 'firingWeight')
        value = ET.SubElement(sub_param, 'value')
        value.text = str(float(fire_weight[m]) if m < len(fire_weight) else 1.0)

    # 3. Firing section
    firing_section = ET.SubElement(node_elem, 'section')
    firing_section.set('className', 'Firing')

    # Firing outcomes - must include ALL output PLACES connected to this transition
    # (even with 0 values for multi-mode transitions), but only include SINK if it has
    # a non-zero firing value (to avoid breaking models that use routing-only to Sink)
    firing_param = ET.SubElement(firing_section, 'parameter')
    firing_param.set('array', 'true')
    firing_param.set('classPath', 'jmt.engine.NetStrategies.TransitionUtilities.TransitionMatrix')
    firing_param.set('name', 'firingOutcomes')

    # Get all output places connected FROM this transition (MATLAB: outputs = find(connmatrix(ind,:)))
    # For Places: include all connected (needed for multi-mode transitions)
    # For Sinks: only include if there's a non-zero firing value in any mode
    output_nodes = []
    if sn.connmatrix is not None:
        for k in range(sn.nnodes):
            if sn.connmatrix[node_idx, k] > 0:
                if sn.nodetype[k] == NodeType.PLACE:
                    # Always include Places
                    output_nodes.append(k)
                elif sn.nodetype[k] == NodeType.SINK:
                    # Only include Sink if there's a non-zero firing value
                    has_nonzero_firing = False
                    for m in range(nmodes):
                        for r in range(K):
                            fire_val = firing[m][k, r] if m < len(firing) else 0
                            if fire_val != 0:
                                has_nonzero_firing = True
                                break
                        if has_nonzero_firing:
                            break
                    if has_nonzero_firing:
                        output_nodes.append(k)

    for m in range(nmodes):
        mode_matrix = ET.SubElement(firing_param, 'subParameter')
        mode_matrix.set('classPath', 'jmt.engine.NetStrategies.TransitionUtilities.TransitionMatrix')
        mode_matrix.set('name', 'firingOutcome')

        vectors = ET.SubElement(mode_matrix, 'subParameter')
        vectors.set('array', 'true')
        vectors.set('classPath', 'jmt.engine.NetStrategies.TransitionUtilities.TransitionVector')
        vectors.set('name', 'firingVectors')

        # Write vectors for all output nodes
        for k in output_nodes:
            vector = ET.SubElement(vectors, 'subParameter')
            vector.set('classPath', 'jmt.engine.NetStrategies.TransitionUtilities.TransitionVector')
            vector.set('name', 'firingVector')

            station_name = ET.SubElement(vector, 'subParameter')
            station_name.set('classPath', 'java.lang.String')
            station_name.set('name', 'stationName')
            value = ET.SubElement(station_name, 'value')
            value.text = nodenames[k]

            entries = ET.SubElement(vector, 'subParameter')
            entries.set('array', 'true')
            entries.set('classPath', 'java.lang.Integer')
            entries.set('name', 'firingEntries')

            for r in range(K):
                ref_class = ET.SubElement(entries, 'refClass')
                ref_class.text = classnames[r]

                entry = ET.SubElement(entries, 'subParameter')
                entry.set('classPath', 'java.lang.Integer')
                entry.set('name', 'firingEntry')
                val = ET.SubElement(entry, 'value')
                fire_val = firing[m][k, r] if m < len(firing) else 0
                val.text = str(int(fire_val))


def _write_distribution_param(parent: ET.Element, dist) -> None:
    """Write distribution parameters for timing strategy."""
    dist_name = dist._name if hasattr(dist, '_name') else type(dist).__name__

    if dist_name == 'Exp':
        distr = ET.SubElement(parent, 'subParameter')
        distr.set('classPath', 'jmt.engine.random.Exponential')
        distr.set('name', 'Exponential')

        distr_par = ET.SubElement(parent, 'subParameter')
        distr_par.set('classPath', 'jmt.engine.random.ExponentialPar')
        distr_par.set('name', 'distrPar')

        lambda_param = ET.SubElement(distr_par, 'subParameter')
        lambda_param.set('classPath', 'java.lang.Double')
        lambda_param.set('name', 'lambda')
        value = ET.SubElement(lambda_param, 'value')
        rate = dist.get_rate() if hasattr(dist, 'get_rate') else 1.0
        value.text = str(rate)
    elif dist_name == 'Erlang':
        distr = ET.SubElement(parent, 'subParameter')
        distr.set('classPath', 'jmt.engine.random.Erlang')
        distr.set('name', 'Erlang')

        distr_par = ET.SubElement(parent, 'subParameter')
        distr_par.set('classPath', 'jmt.engine.random.ErlangPar')
        distr_par.set('name', 'distrPar')

        alpha_param = ET.SubElement(distr_par, 'subParameter')
        alpha_param.set('classPath', 'java.lang.Double')
        alpha_param.set('name', 'alpha')
        value = ET.SubElement(alpha_param, 'value')
        rate = dist.get_rate() if hasattr(dist, 'get_rate') else 1.0
        value.text = str(rate)

        r_param = ET.SubElement(distr_par, 'subParameter')
        r_param.set('classPath', 'java.lang.Long')
        r_param.set('name', 'r')
        value = ET.SubElement(r_param, 'value')
        try:
            order = dist.get_number_of_phases() if hasattr(dist, 'get_number_of_phases') else 1
        except NotImplementedError:
            order = 1
        value.text = str(order)
    elif dist_name == 'HyperExp':
        distr = ET.SubElement(parent, 'subParameter')
        distr.set('classPath', 'jmt.engine.random.HyperExp')
        distr.set('name', 'Hyperexponential')

        distr_par = ET.SubElement(parent, 'subParameter')
        distr_par.set('classPath', 'jmt.engine.random.HyperExpPar')
        distr_par.set('name', 'distrPar')

        # Get parameters
        p = 0.5
        lambda1 = 1.0
        lambda2 = 1.0
        if hasattr(dist, '_p') and hasattr(dist, '_lambda1') and hasattr(dist, '_lambda2'):
            p = dist._p
            lambda1 = dist._lambda1
            lambda2 = dist._lambda2

        p_param = ET.SubElement(distr_par, 'subParameter')
        p_param.set('classPath', 'java.lang.Double')
        p_param.set('name', 'p')
        value = ET.SubElement(p_param, 'value')
        value.text = str(p)

        l1_param = ET.SubElement(distr_par, 'subParameter')
        l1_param.set('classPath', 'java.lang.Double')
        l1_param.set('name', 'lambda1')
        value = ET.SubElement(l1_param, 'value')
        value.text = str(lambda1)

        l2_param = ET.SubElement(distr_par, 'subParameter')
        l2_param.set('classPath', 'java.lang.Double')
        l2_param.set('name', 'lambda2')
        value = ET.SubElement(l2_param, 'value')
        value.text = str(lambda2)
    elif dist_name == 'Pareto':
        distr = ET.SubElement(parent, 'subParameter')
        distr.set('classPath', 'jmt.engine.random.Pareto')
        distr.set('name', 'Pareto')

        distr_par = ET.SubElement(parent, 'subParameter')
        distr_par.set('classPath', 'jmt.engine.random.ParetoPar')
        distr_par.set('name', 'distrPar')

        # Get alpha (shape) and k (scale) parameters
        alpha = 3.0  # default shape
        k = 1.0  # default scale
        if hasattr(dist, 'alpha'):
            alpha = dist.alpha
        elif hasattr(dist, '_alpha'):
            alpha = dist._alpha
        if hasattr(dist, 'scale'):
            k = dist.scale
        elif hasattr(dist, '_scale'):
            k = dist._scale

        alpha_param = ET.SubElement(distr_par, 'subParameter')
        alpha_param.set('classPath', 'java.lang.Double')
        alpha_param.set('name', 'alpha')
        value = ET.SubElement(alpha_param, 'value')
        value.text = str(alpha)

        k_param = ET.SubElement(distr_par, 'subParameter')
        k_param.set('classPath', 'java.lang.Double')
        k_param.set('name', 'k')
        value = ET.SubElement(k_param, 'value')
        value.text = str(k)
    else:
        # Default to exponential with rate 1
        distr = ET.SubElement(parent, 'subParameter')
        distr.set('classPath', 'jmt.engine.random.Exponential')
        distr.set('name', 'Exponential')

        distr_par = ET.SubElement(parent, 'subParameter')
        distr_par.set('classPath', 'jmt.engine.random.ExponentialPar')
        distr_par.set('name', 'distrPar')

        lambda_param = ET.SubElement(distr_par, 'subParameter')
        lambda_param.set('classPath', 'java.lang.Double')
        lambda_param.set('name', 'lambda')
        value = ET.SubElement(lambda_param, 'value')
        value.text = '1.0'


def _write_phase_type_service_distribution(parent: ET.Element, sn: NetworkStruct, ist: int, r: int) -> None:
    """
    Write Phase-Type service distribution to JMT XML.

    This writes the PhaseTypeDistr format used by JMT for general phase-type
    distributions (PH, APH, Coxian, etc.).

    Args:
        parent: Parent XML element (serviceTimeStrategyNode)
        sn: NetworkStruct containing proc and pie fields
        ist: Station index
        r: Class index
    """
    # Get phase-type representation from proc and pie
    # proc stores [alpha, T] for PH distributions
    T = None
    alpha = None

    if hasattr(sn, 'proc') and sn.proc is not None:
        try:
            proc = sn.proc[ist][r]
            if proc is not None and isinstance(proc, (list, tuple)) and len(proc) >= 2:
                # proc = [alpha, T] - alpha is initial probability vector, T is sub-generator matrix
                alpha_candidate = np.asarray(proc[0], dtype=np.float64)
                T_candidate = np.asarray(proc[1], dtype=np.float64)
                # T should be 2D (n x n matrix), alpha should be 1D (n vector)
                if T_candidate.ndim == 2:
                    T = T_candidate
                    alpha = alpha_candidate
                elif alpha_candidate.ndim == 2:
                    # Reversed order: proc = [T, alpha]
                    T = alpha_candidate
                    alpha = T_candidate
            elif proc is not None and isinstance(proc, (list, tuple)) and len(proc) == 1:
                # Single element - assume it's T
                T = np.asarray(proc[0], dtype=np.float64)
        except (IndexError, TypeError, KeyError):
            pass

    # If alpha not found in proc, try pie field
    if alpha is None and hasattr(sn, 'pie') and sn.pie is not None:
        try:
            pie = sn.pie[ist][r]
            if pie is not None:
                alpha = np.asarray(pie, dtype=np.float64)
        except (IndexError, TypeError, KeyError):
            pass

    if T is None:
        # Fallback to exponential if phase-type not available
        distr = ET.SubElement(parent, 'subParameter')
        distr.set('classPath', 'jmt.engine.random.Exponential')
        distr.set('name', 'Exponential')

        distr_par = ET.SubElement(parent, 'subParameter')
        distr_par.set('classPath', 'jmt.engine.random.ExponentialPar')
        distr_par.set('name', 'distrPar')

        lambda_param = ET.SubElement(distr_par, 'subParameter')
        lambda_param.set('classPath', 'java.lang.Double')
        lambda_param.set('name', 'lambda')
        value = ET.SubElement(lambda_param, 'value')
        rate = sn.rates[ist, r] if sn.rates is not None and ist < sn.rates.shape[0] and r < sn.rates.shape[1] else 1.0
        value.text = str(rate)
        return

    # Ensure T is 2D matrix
    if T.ndim == 1:
        # Convert 1D array to 2D (single phase)
        T = T.reshape(1, -1) if len(T) > 1 else np.array([[T[0]]])
    elif T.ndim == 0:
        # Scalar - convert to 1x1 matrix
        T = np.array([[float(T)]])

    n_phases = T.shape[0]

    if alpha is None:
        alpha = np.zeros(n_phases)
        alpha[0] = 1.0
    else:
        # Ensure alpha is 1D
        alpha = np.asarray(alpha).flatten()
        # Ensure correct size
        if len(alpha) < n_phases:
            alpha_new = np.zeros(n_phases)
            alpha_new[:len(alpha)] = alpha
            alpha = alpha_new
        elif len(alpha) > n_phases:
            alpha = alpha[:n_phases]

    # Ensure alpha is positive
    alpha = np.abs(alpha)

    # Write distribution element
    distr = ET.SubElement(parent, 'subParameter')
    distr.set('classPath', 'jmt.engine.random.PhaseTypeDistr')
    distr.set('name', 'Phase-Type')

    # Write parameter element
    distr_par = ET.SubElement(parent, 'subParameter')
    distr_par.set('classPath', 'jmt.engine.random.PhaseTypePar')
    distr_par.set('name', 'distrPar')

    # Write alpha (initial probability vector)
    alpha_param = ET.SubElement(distr_par, 'subParameter')
    alpha_param.set('array', 'true')
    alpha_param.set('classPath', 'java.lang.Object')
    alpha_param.set('name', 'alpha')

    alpha_vec = ET.SubElement(alpha_param, 'subParameter')
    alpha_vec.set('array', 'true')
    alpha_vec.set('classPath', 'java.lang.Object')
    alpha_vec.set('name', 'vector')

    for k in range(n_phases):
        entry = ET.SubElement(alpha_vec, 'subParameter')
        entry.set('classPath', 'java.lang.Double')
        entry.set('name', 'entry')
        value = ET.SubElement(entry, 'value')
        value.text = f'{alpha[k]:.12f}'

    # Write T matrix (sub-generator)
    t_param = ET.SubElement(distr_par, 'subParameter')
    t_param.set('array', 'true')
    t_param.set('classPath', 'java.lang.Object')
    t_param.set('name', 'T')

    for k in range(n_phases):
        row_vec = ET.SubElement(t_param, 'subParameter')
        row_vec.set('array', 'true')
        row_vec.set('classPath', 'java.lang.Object')
        row_vec.set('name', 'vector')

        for j in range(n_phases):
            entry = ET.SubElement(row_vec, 'subParameter')
            entry.set('classPath', 'java.lang.Double')
            entry.set('name', 'entry')
            value = ET.SubElement(entry, 'value')
            # MATLAB: if k==j, use -abs(T(k,j)), else use abs(T(k,j))
            if k == j:
                value.text = f'{-abs(T[k, j]):.12f}'
            else:
                value.text = f'{abs(T[k, j]):.12f}'


def _write_map_service_distribution(parent: ET.Element, sn: NetworkStruct, ist: int, r: int) -> None:
    """
    Write MAP/MMPP2 service distribution to JMT XML.

    This writes the MAPDistr format used by JMT for Markov Arrival Processes
    and Markov Modulated Poisson Processes.

    Args:
        parent: Parent XML element (serviceTimeStrategyNode)
        sn: NetworkStruct containing proc field with D0, D1 matrices
        ist: Station index
        r: Class index
    """
    # Get D0 and D1 matrices from proc
    D0 = None
    D1 = None

    if hasattr(sn, 'proc') and sn.proc is not None:
        try:
            proc = sn.proc[ist][r]
            if proc is not None and isinstance(proc, (list, tuple)) and len(proc) >= 2:
                D0 = np.asarray(proc[0], dtype=np.float64)
                D1 = np.asarray(proc[1], dtype=np.float64)
        except (IndexError, TypeError):
            pass

    if D0 is None or D1 is None:
        # Fallback to exponential if matrices not available
        distr = ET.SubElement(parent, 'subParameter')
        distr.set('classPath', 'jmt.engine.random.Exponential')
        distr.set('name', 'Exponential')

        distr_par = ET.SubElement(parent, 'subParameter')
        distr_par.set('classPath', 'jmt.engine.random.ExponentialPar')
        distr_par.set('name', 'distrPar')

        lambda_param = ET.SubElement(distr_par, 'subParameter')
        lambda_param.set('classPath', 'java.lang.Double')
        lambda_param.set('name', 'lambda')
        value = ET.SubElement(lambda_param, 'value')
        rate = sn.rates[ist, r] if sn.rates is not None and ist < sn.rates.shape[0] and r < sn.rates.shape[1] else 1.0
        value.text = str(rate)
        return

    # Get number of phases
    n_phases = D0.shape[0]

    # Write distribution element
    distr = ET.SubElement(parent, 'subParameter')
    distr.set('classPath', 'jmt.engine.random.MAPDistr')
    distr.set('name', 'Burst (MAP)')

    # Write parameter element
    distr_par = ET.SubElement(parent, 'subParameter')
    distr_par.set('classPath', 'jmt.engine.random.MAPPar')
    distr_par.set('name', 'distrPar')

    # Write D0 matrix
    d0_param = ET.SubElement(distr_par, 'subParameter')
    d0_param.set('array', 'true')
    d0_param.set('classPath', 'java.lang.Object')
    d0_param.set('name', 'D0')

    for k in range(n_phases):
        row_param = ET.SubElement(d0_param, 'subParameter')
        row_param.set('array', 'true')
        row_param.set('classPath', 'java.lang.Object')
        row_param.set('name', 'vector')

        for j in range(n_phases):
            entry_param = ET.SubElement(row_param, 'subParameter')
            entry_param.set('classPath', 'java.lang.Double')
            entry_param.set('name', 'entry')
            value = ET.SubElement(entry_param, 'value')
            value.text = f'{D0[k, j]:.12f}'

    # Write D1 matrix
    d1_param = ET.SubElement(distr_par, 'subParameter')
    d1_param.set('array', 'true')
    d1_param.set('classPath', 'java.lang.Object')
    d1_param.set('name', 'D1')

    for k in range(n_phases):
        row_param = ET.SubElement(d1_param, 'subParameter')
        row_param.set('array', 'true')
        row_param.set('classPath', 'java.lang.Object')
        row_param.set('name', 'vector')

        for j in range(n_phases):
            entry_param = ET.SubElement(row_param, 'subParameter')
            entry_param.set('classPath', 'java.lang.Double')
            entry_param.set('name', 'entry')
            value = ET.SubElement(entry_param, 'value')
            value.text = f'{D1[k, j]:.12f}'


def _write_fork_node(node_elem: ET.Element, node_idx: int, sn: NetworkStruct, classnames: List[str],
                     cs_node_names: Optional[Dict[Tuple[int, int], str]] = None):
    """Write Fork node section.

    Fork nodes in JMT have three sections:
    1. Queue (buffer)
    2. ServiceTunnel
    3. Fork (with ForkStrategy)
    """
    K = sn.nclasses

    # Get fanOut (tasks per link), default to 1
    fan_out = 1
    if hasattr(sn, 'nodeparam') and sn.nodeparam is not None:
        if node_idx in sn.nodeparam and sn.nodeparam[node_idx] is not None:
            if isinstance(sn.nodeparam[node_idx], dict):
                fan_out = sn.nodeparam[node_idx].get('fanOut', 1)

    # 1. Queue section (buffer)
    queue = ET.SubElement(node_elem, 'section')
    queue.set('className', 'Queue')

    size_param = ET.SubElement(queue, 'parameter')
    size_param.set('classPath', 'java.lang.Integer')
    size_param.set('name', 'size')
    value = ET.SubElement(size_param, 'value')
    value.text = '-1'  # Infinite capacity

    # Drop strategies
    drop_strategy = ET.SubElement(queue, 'parameter')
    drop_strategy.set('array', 'true')
    drop_strategy.set('classPath', 'java.lang.String')
    drop_strategy.set('name', 'dropStrategies')

    for r in range(K):
        ref_class = ET.SubElement(drop_strategy, 'refClass')
        ref_class.text = classnames[r]

        sub_param = ET.SubElement(drop_strategy, 'subParameter')
        sub_param.set('classPath', 'java.lang.String')
        sub_param.set('name', 'dropStrategy')
        value = ET.SubElement(sub_param, 'value')
        value.text = 'drop'

    # Queue get strategy (FCFS)
    strategy_param = ET.SubElement(queue, 'parameter')
    strategy_param.set('classPath', 'jmt.engine.NetStrategies.QueueGetStrategies.FCFSstrategy')
    strategy_param.set('name', 'FCFSstrategy')

    # Queue put strategy
    put_strategy = ET.SubElement(queue, 'parameter')
    put_strategy.set('array', 'true')
    put_strategy.set('classPath', 'jmt.engine.NetStrategies.QueuePutStrategy')
    put_strategy.set('name', 'QueuePutStrategy')

    for r in range(K):
        ref_class = ET.SubElement(put_strategy, 'refClass')
        ref_class.text = classnames[r]

        sub_param = ET.SubElement(put_strategy, 'subParameter')
        sub_param.set('classPath', 'jmt.engine.NetStrategies.QueuePutStrategies.TailStrategy')
        sub_param.set('name', 'TailStrategy')

    # 2. ServiceTunnel section
    tunnel = ET.SubElement(node_elem, 'section')
    tunnel.set('className', 'ServiceTunnel')

    # 3. Fork section
    fork = ET.SubElement(node_elem, 'section')
    fork.set('className', 'Fork')

    # jobsPerLink parameter
    jpl_param = ET.SubElement(fork, 'parameter')
    jpl_param.set('classPath', 'java.lang.Integer')
    jpl_param.set('name', 'jobsPerLink')
    value = ET.SubElement(jpl_param, 'value')
    value.text = str(fan_out)

    # block parameter
    block_param = ET.SubElement(fork, 'parameter')
    block_param.set('classPath', 'java.lang.Integer')
    block_param.set('name', 'block')
    value = ET.SubElement(block_param, 'value')
    value.text = '-1'

    # isSimplifiedFork parameter
    simpl_param = ET.SubElement(fork, 'parameter')
    simpl_param.set('classPath', 'java.lang.Boolean')
    simpl_param.set('name', 'isSimplifiedFork')
    value = ET.SubElement(simpl_param, 'value')
    value.text = 'true'

    # ForkStrategy parameter
    strategy_param = ET.SubElement(fork, 'parameter')
    strategy_param.set('array', 'true')
    strategy_param.set('classPath', 'jmt.engine.NetStrategies.ForkStrategy')
    strategy_param.set('name', 'ForkStrategy')

    # Find outgoing connections for this fork
    outgoing_nodes = []
    if sn.connmatrix is not None:
        for j in range(sn.nnodes):
            if sn.connmatrix[node_idx, j] > 0:
                outgoing_nodes.append(j)

    nodenames = sn.nodenames if sn.nodenames else [f'Node{i+1}' for i in range(sn.nnodes)]

    for r in range(K):
        ref_class = ET.SubElement(strategy_param, 'refClass')
        ref_class.text = classnames[r]

        class_strat = ET.SubElement(strategy_param, 'subParameter')
        class_strat.set('classPath', 'jmt.engine.NetStrategies.ForkStrategies.ProbabilitiesFork')
        class_strat.set('name', 'Branch Probabilities')

        emp_array = ET.SubElement(class_strat, 'subParameter')
        emp_array.set('array', 'true')
        emp_array.set('classPath', 'jmt.engine.NetStrategies.ForkStrategies.OutPath')
        emp_array.set('name', 'EmpiricalEntryArray')

        # For each outgoing link, create an OutPath entry
        for out_node in outgoing_nodes:
            out_path = ET.SubElement(emp_array, 'subParameter')
            out_path.set('classPath', 'jmt.engine.NetStrategies.ForkStrategies.OutPath')
            out_path.set('name', 'OutPathEntry')

            # outUnitProbability
            emp_entry = ET.SubElement(out_path, 'subParameter')
            emp_entry.set('classPath', 'jmt.engine.random.EmpiricalEntry')
            emp_entry.set('name', 'outUnitProbability')

            # stationName
            station_name = ET.SubElement(emp_entry, 'subParameter')
            station_name.set('classPath', 'java.lang.String')
            station_name.set('name', 'stationName')
            value = ET.SubElement(station_name, 'value')
            value.text = nodenames[out_node]

            # probability
            prob_param = ET.SubElement(emp_entry, 'subParameter')
            prob_param.set('classPath', 'java.lang.Double')
            prob_param.set('name', 'probability')
            value = ET.SubElement(prob_param, 'value')
            value.text = '1.0'

            # JobsPerLinkDis
            jpl_dis = ET.SubElement(out_path, 'subParameter')
            jpl_dis.set('classPath', 'jmt.engine.random.EmpiricalEntry')
            jpl_dis.set('array', 'true')
            jpl_dis.set('name', 'JobsPerLinkDis')

            jpl_entry = ET.SubElement(jpl_dis, 'subParameter')
            jpl_entry.set('classPath', 'jmt.engine.random.EmpiricalEntry')
            jpl_entry.set('name', 'EmpiricalEntry')

            # numbers (jobs per link)
            numbers_param = ET.SubElement(jpl_entry, 'subParameter')
            numbers_param.set('classPath', 'java.lang.String')
            numbers_param.set('name', 'numbers')
            value = ET.SubElement(numbers_param, 'value')
            value.text = str(fan_out)

            # probability for this distribution
            prob_param2 = ET.SubElement(jpl_entry, 'subParameter')
            prob_param2.set('classPath', 'java.lang.Double')
            prob_param2.set('name', 'probability')
            value = ET.SubElement(prob_param2, 'value')
            value.text = '1.0'


def _write_join_node(node_elem: ET.Element, node_idx: int, sn: NetworkStruct, classnames: List[str],
                     cs_node_names: Optional[Dict[Tuple[int, int], str]] = None):
    """Write Join node section.

    Join nodes in JMT have three sections:
    1. Join (with JoinStrategy)
    2. ServiceTunnel
    3. Router (dispatcher)
    """
    K = sn.nclasses

    # Get the number of incoming links (fanIn) - this is the number of tasks to wait for
    fan_in = 0
    if sn.connmatrix is not None:
        for i in range(sn.nnodes):
            if sn.connmatrix[i, node_idx] > 0:
                fan_in += 1

    # 1. Join section
    join = ET.SubElement(node_elem, 'section')
    join.set('className', 'Join')

    strategy_param = ET.SubElement(join, 'parameter')
    strategy_param.set('array', 'true')
    strategy_param.set('classPath', 'jmt.engine.NetStrategies.JoinStrategy')
    strategy_param.set('name', 'JoinStrategy')

    for r in range(K):
        ref_class = ET.SubElement(strategy_param, 'refClass')
        ref_class.text = classnames[r]

        # Default: Standard Join (wait for all tasks)
        join_strat = ET.SubElement(strategy_param, 'subParameter')
        join_strat.set('classPath', 'jmt.engine.NetStrategies.JoinStrategies.NormalJoin')
        join_strat.set('name', 'Standard Join')

        req_param = ET.SubElement(join_strat, 'subParameter')
        req_param.set('classPath', 'java.lang.Integer')
        req_param.set('name', 'numRequired')
        value = ET.SubElement(req_param, 'value')
        value.text = str(max(1, fan_in))  # Number of tasks to wait for

    # 2. ServiceTunnel section
    tunnel = ET.SubElement(node_elem, 'section')
    tunnel.set('className', 'ServiceTunnel')

    # 3. Router section
    router = ET.SubElement(node_elem, 'section')
    router.set('className', 'Router')
    _write_routing_strategy(router, node_idx, sn, classnames, cs_node_names)


def _write_routing_strategy(router: ET.Element, node_idx: int, sn: NetworkStruct, classnames: List[str],
                            cs_node_names: Optional[Dict[Tuple[int, int], str]] = None):
    """Write routing strategy for a node.

    Handles different routing strategies (RAND, RROBIN, JSQ, PROB, etc.) by using
    the appropriate JMT strategy class.

    When class switching exists between this node and a destination, routes to
    the ClassSwitch node instead of the direct destination.

    Args:
        router: XML element for the Router section
        node_idx: Index of the current node
        sn: NetworkStruct object
        classnames: List of class names
        cs_node_names: Optional dict mapping (src_idx, dst_idx) to ClassSwitch node names
    """
    from ...sn.network_struct import RoutingStrategy

    if cs_node_names is None:
        cs_node_names = {}

    K = sn.nclasses
    M = sn.nnodes
    nodenames = sn.nodenames if sn.nodenames else [f'Node{i+1}' for i in range(M)]

    # Check if we have routing probability data
    has_rtnodes = hasattr(sn, 'rtnodes') and sn.rtnodes is not None and sn.rtnodes.size > 0
    has_connmatrix = hasattr(sn, 'connmatrix') and sn.connmatrix is not None
    has_routing = hasattr(sn, 'routing') and sn.routing is not None

    param = ET.SubElement(router, 'parameter')
    param.set('array', 'true')
    param.set('classPath', 'jmt.engine.NetStrategies.RoutingStrategy')
    param.set('name', 'RoutingStrategy')

    for r in range(K):
        ref_class = ET.SubElement(param, 'refClass')
        ref_class.text = classnames[r]

        # Get routing strategy for this node/class
        strategy = RoutingStrategy.RAND  # Default
        if has_routing and node_idx < sn.routing.shape[0] and r < sn.routing.shape[1]:
            strategy = RoutingStrategy(int(sn.routing[node_idx, r]))

        # Handle different routing strategies
        if strategy == RoutingStrategy.RROBIN:
            # Round Robin strategy
            sub_param = ET.SubElement(param, 'subParameter')
            sub_param.set('classPath', 'jmt.engine.NetStrategies.RoutingStrategies.RoundRobinStrategy')
            sub_param.set('name', 'Round Robin')

        elif strategy == RoutingStrategy.WRROBIN:
            # Weighted Round Robin strategy
            sub_param = ET.SubElement(param, 'subParameter')
            sub_param.set('classPath', 'jmt.engine.NetStrategies.RoutingStrategies.WeightedRoundRobinStrategy')
            sub_param.set('name', 'Weighted Round Robin')

            weight_array = ET.SubElement(sub_param, 'subParameter')
            weight_array.set('array', 'true')
            weight_array.set('classPath', 'jmt.engine.NetStrategies.RoutingStrategies.WeightEntry')
            weight_array.set('name', 'WeightEntryArray')

            # Add weight entries for connected nodes
            if has_connmatrix:
                for j in range(M):
                    if sn.connmatrix[node_idx, j] > 0:
                        weight_entry = ET.SubElement(weight_array, 'subParameter')
                        weight_entry.set('classPath', 'jmt.engine.NetStrategies.RoutingStrategies.WeightEntry')
                        weight_entry.set('name', 'WeightEntry')

                        station_param = ET.SubElement(weight_entry, 'subParameter')
                        station_param.set('classPath', 'java.lang.String')
                        station_param.set('name', 'stationName')
                        station_value = ET.SubElement(station_param, 'value')
                        station_value.text = nodenames[j]

                        weight_param = ET.SubElement(weight_entry, 'subParameter')
                        weight_param.set('classPath', 'java.lang.Integer')
                        weight_param.set('name', 'weight')
                        weight_value = ET.SubElement(weight_param, 'value')
                        # Default weight of 1 for each destination
                        weight_value.text = '1'

        elif strategy == RoutingStrategy.JSQ:
            # Join Shortest Queue strategy
            sub_param = ET.SubElement(param, 'subParameter')
            sub_param.set('classPath', 'jmt.engine.NetStrategies.RoutingStrategies.ShortestQueueLengthRoutingStrategy')
            sub_param.set('name', 'Join the Shortest Queue (JSQ)')

        elif strategy == RoutingStrategy.KCHOICES:
            # Power of K choices strategy
            sub_param = ET.SubElement(param, 'subParameter')
            sub_param.set('classPath', 'jmt.engine.NetStrategies.RoutingStrategies.PowerOfKRoutingStrategy')
            sub_param.set('name', 'Power of k')

            k_param = ET.SubElement(sub_param, 'subParameter')
            k_param.set('classPath', 'java.lang.Integer')
            k_param.set('name', 'k')
            k_value = ET.SubElement(k_param, 'value')
            k_value.text = '2'  # Default k=2

            mem_param = ET.SubElement(sub_param, 'subParameter')
            mem_param.set('classPath', 'java.lang.Boolean')
            mem_param.set('name', 'withMemory')
            mem_value = ET.SubElement(mem_param, 'value')
            mem_value.text = 'false'

        elif strategy == RoutingStrategy.PROB:
            # Probabilistic routing using EmpiricalStrategy
            # When class switching exists, sum probabilities across all destination classes
            # and route to ClassSwitch node instead of direct destination
            routing_probs = []
            if has_rtnodes and has_connmatrix:
                row_idx = node_idx * K + r
                if row_idx < sn.rtnodes.shape[0]:
                    for j in range(M):
                        if sn.connmatrix[node_idx, j] > 0:
                            # Check if there's a ClassSwitch node for this edge
                            if (node_idx, j) in cs_node_names:
                                # Sum probabilities across ALL destination classes
                                total_prob = 0.0
                                for s in range(K):
                                    col_idx = j * K + s
                                    if col_idx < sn.rtnodes.shape[1]:
                                        total_prob += sn.rtnodes[row_idx, col_idx]
                                if total_prob > 0:
                                    routing_probs.append((cs_node_names[(node_idx, j)], total_prob))
                            else:
                                # No class switching - use same-class probability
                                col_idx = j * K + r
                                if col_idx < sn.rtnodes.shape[1]:
                                    prob = sn.rtnodes[row_idx, col_idx]
                                    if prob > 0:
                                        routing_probs.append((nodenames[j], prob))

            if routing_probs:
                # Normalize probabilities to sum to 1.0 if needed
                total = sum(p for _, p in routing_probs)
                if total > 0 and abs(total - 1.0) > 1e-10:
                    routing_probs = [(name, prob / total) for name, prob in routing_probs]

                sub_param = ET.SubElement(param, 'subParameter')
                sub_param.set('classPath', 'jmt.engine.NetStrategies.RoutingStrategies.EmpiricalStrategy')
                sub_param.set('name', 'Probabilities')

                emp_array = ET.SubElement(sub_param, 'subParameter')
                emp_array.set('array', 'true')
                emp_array.set('classPath', 'jmt.engine.random.EmpiricalEntry')
                emp_array.set('name', 'EmpiricalEntryArray')

                for dest_name, prob in routing_probs:
                    emp_entry = ET.SubElement(emp_array, 'subParameter')
                    emp_entry.set('classPath', 'jmt.engine.random.EmpiricalEntry')
                    emp_entry.set('name', 'EmpiricalEntry')

                    station_param = ET.SubElement(emp_entry, 'subParameter')
                    station_param.set('classPath', 'java.lang.String')
                    station_param.set('name', 'stationName')
                    station_value = ET.SubElement(station_param, 'value')
                    station_value.text = dest_name

                    prob_param = ET.SubElement(emp_entry, 'subParameter')
                    prob_param.set('classPath', 'java.lang.Double')
                    prob_param.set('name', 'probability')
                    prob_value = ET.SubElement(prob_param, 'value')
                    prob_value.text = f'{prob:.12f}'
            else:
                # Fallback to Random if no probabilities defined
                sub_param = ET.SubElement(param, 'subParameter')
                sub_param.set('classPath', 'jmt.engine.NetStrategies.RoutingStrategies.RandomStrategy')
                sub_param.set('name', 'Random')

        elif strategy == RoutingStrategy.DISABLED:
            # Disabled routing
            sub_param = ET.SubElement(param, 'subParameter')
            sub_param.set('classPath', 'jmt.engine.NetStrategies.RoutingStrategies.DisabledRoutingStrategy')
            sub_param.set('name', 'Disabled')

        else:
            # Default: Try to use EmpiricalStrategy with explicit probabilities if available
            # This handles RAND strategy when routing probabilities are defined
            # When class switching exists, sum probabilities and route to ClassSwitch node
            routing_probs = []
            if has_rtnodes and has_connmatrix:
                row_idx = node_idx * K + r
                if row_idx < sn.rtnodes.shape[0]:
                    # Iterate over all nodes (not just stations) to include Sink
                    n_nodes = sn.nnodes if hasattr(sn, 'nnodes') else sn.connmatrix.shape[1]
                    for j in range(n_nodes):
                        if j < sn.connmatrix.shape[1] and sn.connmatrix[node_idx, j] > 0:
                            # Check if there's a ClassSwitch node for this edge
                            if (node_idx, j) in cs_node_names:
                                # Sum probabilities across ALL destination classes
                                total_prob = 0.0
                                for s in range(K):
                                    col_idx = j * K + s
                                    if col_idx < sn.rtnodes.shape[1]:
                                        total_prob += sn.rtnodes[row_idx, col_idx]
                                if total_prob > 0:
                                    routing_probs.append((cs_node_names[(node_idx, j)], total_prob))
                            else:
                                # No class switching - use same-class probability
                                col_idx = j * K + r
                                if col_idx < sn.rtnodes.shape[1]:
                                    prob = sn.rtnodes[row_idx, col_idx]
                                    if prob > 0:
                                        routing_probs.append((nodenames[j], prob))

            if routing_probs:
                # Normalize probabilities to sum to 1.0
                # This is necessary for RAND strategy where rtnodes contains connection weights (1.0)
                # rather than actual routing probabilities
                total = sum(p for _, p in routing_probs)
                if total > 0 and abs(total - 1.0) > 1e-10:
                    routing_probs = [(name, prob / total) for name, prob in routing_probs]

                # Use EmpiricalStrategy with explicit probabilities
                sub_param = ET.SubElement(param, 'subParameter')
                sub_param.set('classPath', 'jmt.engine.NetStrategies.RoutingStrategies.EmpiricalStrategy')
                sub_param.set('name', 'Probabilities')

                emp_array = ET.SubElement(sub_param, 'subParameter')
                emp_array.set('array', 'true')
                emp_array.set('classPath', 'jmt.engine.random.EmpiricalEntry')
                emp_array.set('name', 'EmpiricalEntryArray')

                for dest_name, prob in routing_probs:
                    emp_entry = ET.SubElement(emp_array, 'subParameter')
                    emp_entry.set('classPath', 'jmt.engine.random.EmpiricalEntry')
                    emp_entry.set('name', 'EmpiricalEntry')

                    station_param = ET.SubElement(emp_entry, 'subParameter')
                    station_param.set('classPath', 'java.lang.String')
                    station_param.set('name', 'stationName')
                    station_value = ET.SubElement(station_param, 'value')
                    station_value.text = dest_name

                    prob_param = ET.SubElement(emp_entry, 'subParameter')
                    prob_param.set('classPath', 'java.lang.Double')
                    prob_param.set('name', 'probability')
                    prob_value = ET.SubElement(prob_param, 'value')
                    prob_value.text = f'{prob:.12f}'
            else:
                # Fallback to Random strategy
                sub_param = ET.SubElement(param, 'subParameter')
                sub_param.set('classPath', 'jmt.engine.NetStrategies.RoutingStrategies.RandomStrategy')
                sub_param.set('name', 'Random')


def _parse_jsim_results(result_path: str, sn: NetworkStruct) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Parse JMT simulation results from XML output.

    Returns:
        Tuple of (Q, U, R, T) matrices
    """
    M = sn.nstations
    K = sn.nclasses

    Q = np.full((M, K), np.nan)
    U = np.full((M, K), np.nan)
    R = np.full((M, K), np.nan)
    T = np.full((M, K), np.nan)

    if not os.path.exists(result_path):
        return Q, U, R, T

    try:
        tree = ET.parse(result_path)
        root = tree.getroot()

        classnames = sn.classnames if sn.classnames else [f'Class{i+1}' for i in range(K)]
        nodenames = sn.nodenames if sn.nodenames else [f'Node{i+1}' for i in range(sn.nnodes)]

        for measure in root.iter('measure'):
            measure_type = measure.get('measureType', measure.get('type', ''))
            node_name = measure.get('station', measure.get('referenceNode', ''))
            class_name = measure.get('class', measure.get('referenceUserClass', ''))
            mean_value = measure.get('meanValue', '0')
            # Note: We accept results even when successful="false" as JMT still provides
            # valid mean values - it just means the precision target wasn't met

            # Find station index
            station_idx = -1
            for i in range(M):
                node_idx = int(sn.stationToNode[i]) if sn.stationToNode is not None else i
                if node_idx < len(nodenames) and nodenames[node_idx] == node_name:
                    station_idx = i
                    break

            if station_idx < 0:
                continue

            # Find class index
            class_idx = -1
            for r in range(K):
                if r < len(classnames) and classnames[r] == class_name:
                    class_idx = r
                    break

            if class_idx < 0:
                continue

            try:
                value = float(mean_value)
            except ValueError:
                continue

            if 'Number of Customers' in measure_type or 'QLen' in measure_type:
                Q[station_idx, class_idx] = value
            elif 'Utilization' in measure_type or 'Util' in measure_type:
                U[station_idx, class_idx] = value
            elif 'Response Time' in measure_type or 'RespT' in measure_type:
                R[station_idx, class_idx] = value
            elif 'Throughput' in measure_type or 'Tput' in measure_type:
                T[station_idx, class_idx] = value

    except Exception as e:
        pass  # Return NaN-filled matrices on parse error

    return Q, U, R, T


def solver_jmt(
    sn: NetworkStruct,
    options: Optional[SolverJMTOptions] = None,
    model: Any = None
) -> SolverJMTReturn:
    """
    JMT solver handler - calls JMT via subprocess.

    Performs discrete-event simulation using JMT by:
    1. Writing the model to JSIM XML format
    2. Calling JMT via subprocess
    3. Parsing the results

    Args:
        sn: Network structure
        options: Solver options
        model: Optional Network model (for FCR regions)

    Returns:
        SolverJMTReturn with all performance metrics

    Raises:
        RuntimeError: If JMT is not available or fails
    """
    start_time = time.time()

    if options is None:
        options = SolverJMTOptions()

    if not is_jmt_available():
        raise RuntimeError(
            "SolverJMT requires Java and JMT.jar.\n"
            "Ensure Java is installed and JMT.jar is in the common/ directory."
        )

    jmt_path = _get_jmt_jar_path()

    M = sn.nstations
    K = sn.nclasses

    # Create temporary directory
    temp_dir = tempfile.mkdtemp(prefix='jmt_')

    try:
        model_path = os.path.join(temp_dir, 'model.jsimg')
        result_path = model_path + '-result.jsim'  # JMT creates .jsimg-result.jsim

        # Write model to JSIM format
        _write_jsim_file(sn, model_path, options, model)

        # Build command
        cmd = [
            'java',
            '-cp', jmt_path,
            'jmt.commandline.Jmt',
            'sim',
            model_path,
            '-seed', str(options.seed),
        ]

        if options.verbose:
            print(f"SolverJMT command: {' '.join(cmd)}")

        # Execute command
        result = subprocess.run(
            cmd,
            capture_output=True,
            cwd=temp_dir,
            timeout=600  # 10 minute timeout
        )

        if result.returncode != 0:
            stderr = result.stderr.decode('utf-8', errors='ignore')
            raise RuntimeError(f"JMT simulation failed: {stderr}")

        # Parse results
        Q, U, R, T = _parse_jsim_results(result_path, sn)

        # Calculate arrival rates and other metrics
        A = np.zeros((M, K))
        W = R.copy()

        # System throughput (sum at reference stations)
        X = np.zeros((1, K))
        refstat = sn.refstat.flatten() if sn.refstat is not None else np.zeros(K, dtype=int)
        for r in range(K):
            if int(refstat[r]) < M:
                X[0, r] = T[int(refstat[r]), r]

        # Cycle times
        C = np.zeros((1, K))
        njobs = sn.njobs.flatten() if sn.njobs is not None else np.zeros(K)
        for r in range(K):
            if not np.isinf(njobs[r]) and X[0, r] > 0:
                C[0, r] = njobs[r] / X[0, r]

        runtime = time.time() - start_time

        return SolverJMTReturn(
            Q=Q,
            U=U,
            R=R,
            T=T,
            A=A,
            W=W,
            C=C,
            X=X,
            runtime=runtime,
            method='jsim'
        )

    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)
