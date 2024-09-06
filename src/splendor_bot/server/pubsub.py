from dataclasses import dataclass, field
from typing import Callable
from uuid import UUID


@dataclass
class PubSub:
    events: dict[str, dict[UUID, Callable]] = field(default_factory=dict)
    
    def subscribe(
        self,
        event: str,
        callback: Callable,
        connection_uuid: UUID,
    ) -> UUID:
        if event not in self.events:
            self.events[event] = {}
        self.events[event][connection_uuid] = callback
        return connection_uuid

    def unsubscribe(self, event: str, connection_uuid: UUID) -> None:
        if event in self.events:
            if connection_uuid in self.events[event]:
                self.events[event].pop(connection_uuid)

    async def publish(self, event: str, *args, **kwargs) -> None:
        if event in self.events:
            for callback in self.events[event].values():
                await callback(*args, **kwargs)
