from network_generator import generate_network
from reachability_graph import build_reachability_graph
from network_partitioner import partition_reachability_graph
from distributed_runner import run_distributed_generation
from serial_dfs import run_serial_dfs


if __name__ == "__main__":

    network = generate_network(18)
    reachability_graph = build_reachability_graph(network)
    partitions = partition_reachability_graph(reachability_graph, 3)

    serial_graph, serial_time, serial_privileges = run_serial_dfs(network)

    distributed_graph, distributed_time, distributed_privileges, expanded = run_distributed_generation(
        network,
        reachability_graph,
        partitions
    )

    print("=" * 60)
    print("Lightweight Distributed Attack Graph Simulation")
    print("=" * 60)
    print(f"Serial Runtime        : {serial_time:.6f}s")
    print(f"Serial Privileges     : {serial_privileges}")
    print(f"Distributed Runtime   : {distributed_time:.6f}s")
    print(f"Distributed Privileges: {distributed_privileges}")
    print(f"Expanded Privileges   : {expanded}")