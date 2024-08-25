from dataclasses import dataclass, field
from typing import Callable


@dataclass
class PubSub:
    connections: dict[str, list[Callable]] = field(default_factory=dict)
    
    def subscribe(self, event: str, callback: Callable) -> None:
        if event not in self.connections:
            self.connections[event] = []
        self.connections[event].append(callback)

    def publish(self, event: str, *args, **kwargs) -> None:
        if event in self.connections:
            for callback in self.connections[event]:
                callback(*args, **kwargs)
