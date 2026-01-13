
class types:
    PlayerJoin = "minecraft:notification/players/joined"              # name, uuid
    PlayerLeft = "minecraft:notification/players/left"                # name, uuid

    PlayerIPBanned = "minecraft:notification/ip_bans/added"           # ip reason expires source
    PlayerIPUnBanned = "minecraft:notification/ip_bans/removed"       #
    PlayerBanned = "minecraft:notification/bans/added"                # player reason expires source
    PlayerUnBanned = "minecraft:notification/bans/removed"            #

    OperatorAdded = "minecraft:notification/operators/added"          # player permissionLevel bypassesPlayerLimit
    OperatorRemoved = "minecraft:notification/operators/removed"      #

    WhitelistAdded = "minecraft:notification/allowlist/added"         #
    WhitelistRemoved = "minecraft:notification/allowlist/removed"     #

    GameruleUpdated = "minecraft:notification/gamerules/updated"      #
    ServerStarted = "minecraft:notification/server/started"           #
    ServerStopping = "minecraft:notification/server/stopping"         #
    ServerSaving = "minecraft:notification/server/saving"             #
    ServerSaved = "minecraft:notification/server/saved"               #
    ServerActivity = "minecraft:notification/server/activity"         #
    ServerStatus = "minecraft:notification/server/status"             # started, players[], version


