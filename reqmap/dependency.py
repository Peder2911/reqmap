
class Dependency():
    def __init__(self, name: str):
        self.name: str = name

    def __repr__(self) -> str:
        return f"Dependency(\"{self.name}\")"

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: "Dependency") -> bool:
        return hash(self) == hash(other)
