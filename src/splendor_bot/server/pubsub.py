from dataclasses import dataclass, field
from typing import Callable
from uuid import UUID, uuid4


@dataclass
class PubSub:
    events: dict[str, dict[UUID, Callable]] = field(default_factory=dict)
    
    def subscribe(self, event: str, callback: Callable) -> UUID:
        if event not in self.events:
            self.events[event] = {}
        callback_uuid = uuid4()
        self.events[event][callback_uuid] = callback
        return callback_uuid

    def unsubscribe(self, event: str, callback_uuid: UUID) -> None:
        if event in self.events:
            if callback_uuid in self.events[event]:
                self.events[event].pop(callback_uuid)

    async def publish(self, event: str, *args, **kwargs) -> None:
        if event in self.events:
            for callback in self.events[event].values():
                await callback(*args, **kwargs)
