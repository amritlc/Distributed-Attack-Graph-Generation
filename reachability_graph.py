import networkx as nx


# Builds a reachability graph from the synthetic network.
def build_reachability_graph(network: dict) -> nx.DiGraph:

    reachability_graph = nx.DiGraph()  # Stores host reachability relationships

    for host_id, host in network.items():

        reachability_graph.add_node(host_id, zone=host.zone)  # Add host as graph node

        for target_host_id in host.reachable_hosts:

            if target_host_id in network:
                reachability_graph.add_edge(host_id, target_host_id)  # Add reachability edge

    return reachability_graph