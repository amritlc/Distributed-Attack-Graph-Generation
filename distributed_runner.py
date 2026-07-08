import time
import networkx as nx
from shared_memory import SharedMemory
from distributed_agent import run_agent_dfs


# Runs all distributed agents and merges their partial attack graphs.
def run_distributed_generation(network, reachability_graph, partitions):

    start_time = time.time()  # Start timer

    shared_memory = SharedMemory()  # Shared privilege expansion tracker
    final_graph = nx.DiGraph()  # Stores merged final attack graph

    for agent_id, assigned_hosts in enumerate(partitions):

        partial_graph = run_agent_dfs(
            agent_id=agent_id,
            assigned_hosts=assigned_hosts,
            network=network,
            reachability_graph=reachability_graph,
            shared_memory=shared_memory
        )

        final_graph = nx.compose(final_graph, partial_graph)  # Merge partial graph

    runtime = time.time() - start_time  # Calculate runtime

    privilege_count = sum(
        1 for _, data in final_graph.nodes(data=True)
        if data.get("node_type") == "privilege"
    )

    return final_graph, runtime, privilege_count, shared_memory.count_expanded()