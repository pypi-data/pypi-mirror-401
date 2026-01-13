from abc import abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Union

from . import objects


@dataclass
class NotificationBase:
    identifier: ClassVar[str]
    @classmethod
    @abstractmethod
    def create_from_params(cls, params: list[any]) -> 'NotificationBase':
        pass



class types:
    @dataclass
    class PlayerJoin(NotificationBase):
        player: objects.PlayerData
        identifier: ClassVar[str] = "minecraft:notification/players/joined"
        @classmethod
        def create_from_params(cls, params: list[any]) -> 'types.PlayerJoin':
            return cls(objects.PlayerData.from_minecraft_data(params[0]))

    @dataclass
    class PlayerLeft(NotificationBase):
        player: objects.PlayerData
        identifier: ClassVar[str] = "minecraft:notification/players/left"
        @classmethod
        def create_from_params(cls, params: list[any]) -> 'types.PlayerLeft':
            return cls(objects.PlayerData.from_minecraft_data(params[0]))

    @dataclass
    class OperatorAdded(NotificationBase):
        player: objects.PlayerData
        permissionLevel: int
        bypassesPlayerLimit: bool
        identifier: ClassVar[str] = "minecraft:notification/operators/added"
        @classmethod
        def create_from_params(cls, params: list[any]) -> 'types.OperatorAdded':
            data = params[0]
            return cls(
                player=objects.PlayerData.from_minecraft_data(data['player']),
                permissionLevel=int(data['permissionLevel']),
                bypassesPlayerLimit=bool(data['bypassesPlayerLimit'])
            )

    @dataclass
    class OperatorRemoved(NotificationBase):
        player: objects.PlayerData
        permissionLevel: int
        bypassesPlayerLimit: bool
        identifier: ClassVar[str] = "minecraft:notification/operators/removed"
        @classmethod
        def create_from_params(cls, params: list[any]) -> 'types.OperatorRemoved':
            data = params[0]
            return cls(
                player=objects.PlayerData.from_minecraft_data(data['player']),
                permissionLevel=int(data['permissionLevel']),
                bypassesPlayerLimit=bool(data['bypassesPlayerLimit'])
            )

    @dataclass
    class PlayerIPBanned(NotificationBase):
        ip: str
        reason: str
        source: str
        identifier: ClassVar[str] = "minecraft:notification/ip_bans/added"
        @classmethod
        def create_from_params(cls, params: list[any]) -> 'types.PlayerIPBanned':
            data = params[0]
            return cls(
                data['ip'],
                data.get("reason", None),
                data['source']
            )

    @dataclass
    class PlayerIPUnBanned(NotificationBase):
        ip: str
        identifier: ClassVar[str] = "minecraft:notification/ip_bans/removed"
        @classmethod
        def create_from_params(cls, params: list[any]) -> 'types.PlayerIPUnBanned':
            return cls(
                params[0]
            )

    @dataclass
    class PlayerBanned(NotificationBase):
        player: objects.PlayerData
        reason:str
        source: str
        identifier: ClassVar[str] = "minecraft:notification/bans/added"
        @classmethod
        def create_from_params(cls, params: list[any]) -> 'types.PlayerBanned':
            return cls(
                objects.PlayerData.from_minecraft_data(params[0].get("player")),
                params[0].get("reason", None),
                params[0].get("source")
            )

    @dataclass
    class PlayerUnBanned(NotificationBase):
        player: objects.PlayerData
        identifier: ClassVar[str] = "minecraft:notification/bans/removed"
        @classmethod
        def create_from_params(cls, params: list[any]) -> 'types.PlayerUnBanned':
            return cls(
                objects.PlayerData.from_minecraft_data(params[0])
            )

    @dataclass
    class WhiteListAdded(NotificationBase):
        player: objects.PlayerData
        identifier: ClassVar[str] = "minecraft:notification/allowlist/added"
        @classmethod
        def create_from_params(cls, params: list[any]) -> 'types.WhiteListAdded':
            return cls(
                objects.PlayerData.from_minecraft_data(params[0])
            )

    @dataclass
    class WhiteListRemoved(NotificationBase):
        player: objects.PlayerData
        identifier: ClassVar[str] = "minecraft:notification/allowlist/removed"

        @classmethod
        def create_from_params(cls, params: list[any]) -> 'types.WhiteListRemoved':
            return cls(
                objects.PlayerData.from_minecraft_data(params[0])
            )

    @dataclass
    class GameruleUpdated(NotificationBase):
        game_rule: objects.GameRule
        identifier: ClassVar[str] = "minecraft:notification/gamerules/updated"
        @classmethod
        def create_from_params(cls, params: list[any]) -> 'types.GameruleUpdated':
            return cls(
                objects.GameRule.from_minecraft_data(params[0])
            )

    @dataclass
    class ServerStarted(NotificationBase):
        params: any
        identifier: ClassVar[str] = "minecraft:notification/server/started"

        @classmethod
        def create_from_params(cls, params: list[any]) -> 'types.ServerStarted':
            return cls(
                params
            )

    @dataclass
    class ServerStopping(NotificationBase):
        params: any
        identifier: ClassVar[str] = "minecraft:notification/server/stopping"
        @classmethod
        def create_from_params(cls, params: list[any]) -> 'types.ServerStopping':
            return cls(
                params
            )

    @dataclass
    class ServerSaving(NotificationBase):
        params: any
        identifier: ClassVar[str] = "minecraft:notification/server/saving"

        @classmethod
        def create_from_params(cls, params: list[any]) -> 'types.ServerSaving':
            return cls(
                params
            )

    @dataclass
    class ServerSaved(NotificationBase):
        params: any
        identifier: ClassVar[str] = "minecraft:notification/server/saved"

        @classmethod
        def create_from_params(cls, params: list[any]) -> 'types.ServerSaved':
            return cls(
                params
            )

    @dataclass
    class ServerActivity(NotificationBase):
        params: any
        identifier: ClassVar[str] = "minecraft:notification/server/activity"

        @classmethod
        def create_from_params(cls, params: list[any]) -> 'types.ServerActivity':
            return cls(
                params
            )

    @dataclass
    class ServerStatus(NotificationBase):
        params: any
        identifier: ClassVar[str] = "minecraft:notification/server/status"

        @classmethod
        def create_from_params(cls, params: list[any]) -> 'types.ServerStatus':
            return cls(
                params
            )


