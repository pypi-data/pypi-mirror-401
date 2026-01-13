from dataclasses import dataclass

from typing import Union


@dataclass
class PlayerData:
    id: str
    name: str

    @classmethod
    def from_minecraft_data(cls, data: dict[str, any]) -> 'PlayerData':
        return cls(
            name=data.get('name', ''),
            id=data.get('id', '')
        )

    @property
    def uuid(self) -> str:
        return self.id

    @property
    def dict(self) -> dict:
        return {"id": self.id, "name": self.name, "uuid": self.uuid}

@dataclass
class GameRule:
    key: str
    value: Union[int, bool, str]
    type: str
    @classmethod
    def from_minecraft_data(cls, data: dict[str, any]) -> 'GameRule':
        value = data.get("value")
        if data.get("type") == "boolean":
            value = bool(data.get("value"))
        if data.get("type") == "integer":
            value = int(data.get("value"))
        return cls(
            data.get("key"),
            value,
            data.get("type")
        )
    @property
    def dict(self) -> dict:
        return {"key": self.key, "value": self.value, "type": self.type}