import pandas as pd
from network_generator import generate_network
from reachability_graph import build_reachability_graph
from network_partitioner import partition_reachability_graph
from serial_dfs import run_serial_dfs
from distributed_runner import run_distributed_generation


def run_experiments():

    host_sizes = [18, 27, 36, 54, 90, 126]
    agent_counts = [2, 3, 4]
    results = []

    for host_count in host_sizes:

        print(f"Running experiment for {host_count} hosts...")

        network = generate_network(host_count)
        reachability_graph = build_reachability_graph(network)

        serial_graph, serial_time, serial_privileges = run_serial_dfs(network)

        row = {
            "Host Count": host_count,
            "Serial DFS Time": serial_time,
            "Privilege Count": serial_privileges,
            "Graph Nodes": serial_graph.number_of_nodes(),
            "Graph Edges": serial_graph.number_of_edges()
        }

        for agent_count in agent_counts:

            partitions = partition_reachability_graph(
                reachability_graph,
                agent_count
            )

            distributed_graph, distributed_time, distributed_privileges, expanded = run_distributed_generation(
                network,
                reachability_graph,
                partitions
            )

            row[f"Distributed {agent_count} Agents Time"] = distributed_time
            row[f"Distributed {agent_count} Agents Privileges"] = distributed_privileges
            row[f"Distributed {agent_count} Agents Expanded"] = expanded

        results.append(row)

    df = pd.DataFrame(results)
    df.to_csv("results/experiment_results.csv", index=False)

    print("\nExperiment completed.")
    print("Results saved to results/experiment_results.csv")


if __name__ == "__main__":
    run_experiments()