import networkx as nx


# Partitions the reachability graph into balanced agent groups.
def partition_reachability_graph(reachability_graph: nx.DiGraph, agent_count: int) -> list[list[str]]:

    host_ids = list(reachability_graph.nodes())  # Get all hosts from reachability graph

    partitions = [[] for _ in range(agent_count)]  # Create empty partitions

    sorted_hosts = sorted(
        host_ids,
        key=lambda host: reachability_graph.out_degree(host),
        reverse=True
    )  # Sort hosts by reachability workload

    for index, host_id in enumerate(sorted_hosts):
        agent_id = index % agent_count  # Assign host to agent in round-robin order
        partitions[agent_id].append(host_id)

    return partitions