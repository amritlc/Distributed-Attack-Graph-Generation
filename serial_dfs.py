import time
import networkx as nx
from network_generator import Host


# Runs serial DFS attack graph generation.
def run_serial_dfs(network: dict[str, Host]):

    start_time = time.time()  # Start runtime measurement

    graph = nx.DiGraph()  # Create directed attack graph

    expanded = set()  # Stores already expanded privileges

    stack = ["network_access_H1"]  # Initial attacker privilege

    graph.add_node("network_access_H1", node_type="privilege")  # Add initial privilege node

    while stack:

        current_privilege = stack.pop()  # Get latest privilege from stack

        if current_privilege in expanded:
            continue  # Skip already expanded privilege

        expanded.add(current_privilege)  # Mark privilege as expanded

        privilege_type, current_host = current_privilege.rsplit("_", 1)  # Split privilege and host

        if current_host not in network:
            continue  # Skip if host does not exist

        source_host = network[current_host]  # Get current host object

        for target_host_id in source_host.reachable_hosts:

            target_host = network[target_host_id]  # Get reachable host

            for vulnerability in target_host.vulnerabilities:

                if vulnerability.precondition == privilege_type:

                    exploit_node = f"{vulnerability.cve_id}_{target_host_id}"  # Create exploit node

                    new_privilege = f"{vulnerability.postcondition}_{target_host_id}"  # Create gained privilege

                    graph.add_node(exploit_node, node_type="vulnerability")  # Add vulnerability node

                    graph.add_node(new_privilege, node_type="privilege")  # Add new privilege node

                    graph.add_edge(current_privilege, exploit_node)  # Privilege enables exploit

                    graph.add_edge(exploit_node, new_privilege)  # Exploit gives new privilege

                    if new_privilege not in expanded:
                        stack.append(new_privilege)  # Add new privilege for further expansion

    end_time = time.time()  # End runtime measurement

    runtime = end_time - start_time  # Calculate total runtime

    privilege_count = sum(
        1 for _, data in graph.nodes(data=True)
        if data.get("node_type") == "privilege"
    )  # Count privilege nodes

    return graph, runtime, privilege_count