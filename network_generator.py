from dataclasses import dataclass
from typing import List, Dict


# shows a vulnerability on a host.
@dataclass
class Vulnerability:
    cve_id: str                  # CVE identifier
    service: str                 # Vulnerable service
    precondition: str            # Required privilege before exploitation
    postcondition: str           # Privilege gained after exploitation


# shows a host in the enterprise network.
@dataclass
class Host:
    host_id: str                         # Unique host identifier
    ip: str                              # IP address
    zone: str                            # Network zone
    services: List[str]                  # Running services
    vulnerabilities: List[Vulnerability] # Host vulnerabilities
    reachable_hosts: List[str]           # Hosts reachable from this host


# generates a synthetic enterprise network.
def generate_network(host_count: int) -> Dict[str, Host]:

    hosts = {}  # stores all generated hosts

    # available network zones.
    zones = [
        "External",
        "DMZ",
        "AdminLAN",
        "InternalLAN1",
        "InternalLAN2"
    ]

    # available enterprise services.
    services_pool = [
        "Apache",
        "IIS",
        "MySQL",
        "Exchange",
        "SMB",
        "RDP",
        "SSH",
        "Browser"
    ]

    # create the required number of hosts.
    for i in range(1, host_count + 1):

        host_id = f"H{i}"                              # Generate host ID
        zone = zones[i % len(zones)]                  # Assign network zone
        ip = f"192.168.{i // 255}.{i % 255}"          # Generate IP address

        # assign two services to each host.
        services = [
            services_pool[i % len(services_pool)],
            services_pool[(i + 2) % len(services_pool)]
        ]

        vulnerabilities = []  # stores host vulnerabilities

        # generate approximately 10 vulnerabilities per host.
        for v in range(10):

            service = services[v % len(services)]

            # Define privilege transition for each vulnerability.
            if v % 4 == 0:
                pre = "network_access"
                post = "user_access"

            elif v % 4 == 1:
                pre = "user_access"
                post = "network_access"

            elif v % 4 == 2:
                pre = "admin_access"
                post = "database_access"

            else:
                pre = "user_access"
                post = "admin_access"

            # create vulnerability object.
            vulnerabilities.append(
                Vulnerability(
                    cve_id=f"CVE_SYN_{i}_{v}",
                    service=service,
                    precondition=pre,
                    postcondition=post
                )
            )

        reachable_hosts = []  # Stores reachable neighbouring hosts

        # Connect each host to the next three hosts.
        for j in range(i + 1, min(i + 4, host_count + 1)):
            reachable_hosts.append(f"H{j}")

        # create host object.
        hosts[host_id] = Host(
            host_id=host_id,
            ip=ip,
            zone=zone,
            services=services,
            vulnerabilities=vulnerabilities,
            reachable_hosts=reachable_hosts
        )

    return hosts


# runs a simple test when executed directly.
if __name__ == "__main__":

    network = generate_network(18)

    print("=" * 60)
    print("Synthetic Enterprise Network Generated")
    print("=" * 60)

    print(f"\nTotal Hosts: {len(network)}\n")

    print(network["H1"])