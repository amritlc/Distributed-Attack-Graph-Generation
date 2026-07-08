# Simulates virtual shared memory for distributed agents.
class SharedMemory:

    # Creates shared memory storage.
    def __init__(self):
        self.expanded_privileges = set()

    # Checks whether a privilege has already been expanded.
    def is_expanded(self, privilege: str) -> bool:
        return privilege in self.expanded_privileges

    # Marks a privilege as expanded.
    def mark_expanded(self, privilege: str):
        self.expanded_privileges.add(privilege)

    # Returns total expanded privileges.
    def count_expanded(self) -> int:
        return len(self.expanded_privileges)