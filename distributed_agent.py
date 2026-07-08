import networkx as nx
from shared_memory import SharedMemory


# Runs distributed DFS for one agent and builds a partial attack graph.
def run_agent_dfs(
    agent_id: int,
    assigned_hosts: list[str],
    network: dict,
    reachability_graph: nx.DiGraph,
    shared_memory: SharedMemory
) -> nx.DiGraph:

    partial_graph = nx.DiGraph()  # Stores this agent's partial attack graph
    stack = []  # Stores privileges waiting to be expanded

    # Add initial network access privileges for assigned hosts.
    for host_id in assigned_hosts:
        stack.append(f"network_access_{host_id}")

    while stack:

        current_privilege = stack.pop()  # Get next privilege

        if shared_memory.is_expanded(current_privilege):
            continue  # Skip if already expanded by any agent

        shared_memory.mark_expanded(current_privilege)  # Mark privilege as expanded

        privilege_type, current_host = current_privilege.rsplit("_", 1)

        if current_host not in network:
            continue  # Skip invalid host

        # Explore reachable hosts from the current host.
        for target_host_id in reachability_graph.successors(current_host):

            target_host = network[target_host_id]

            for vulnerability in target_host.vulnerabilities:

                if vulnerability.precondition == privilege_type:

                    exploit_node = f"{vulnerability.cve_id}_{target_host_id}"
                    new_privilege = f"{vulnerability.postcondition}_{target_host_id}"

                    partial_graph.add_node(current_privilege, node_type="privilege")
                    partial_graph.add_node(exploit_node, node_type="vulnerability")
                    partial_graph.add_node(new_privilege, node_type="privilege")

                    partial_graph.add_edge(current_privilege, exploit_node)
                    partial_graph.add_edge(exploit_node, new_privilege)

                    if not shared_memory.is_expanded(new_privilege):
                        stack.append(new_privilege)

    return partial_graph