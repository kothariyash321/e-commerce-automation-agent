class AgentMemory:
    """Stores short-lived context between tool steps."""

    def __init__(self):
        self.buffer = []

    def add(self, event: dict) -> None:
        self.buffer.append(event)

    def read(self) -> list[dict]:
        return self.buffer[-50:]
