
import os

# =========================================================================
# CONFIGURACIÓN ORIGINAL DE HSEINHA
# =========================================================================

class config:
    # Configuración básica
    prefix = '/'
    botID = '6ab1d5b3be121e4c4a3fe7d0'
    botName = 'beBot33'
    ownerName = 'IamDakota'
    roomName = 'Sala de IamDakota'

    # Coordenadas donde aparecerá el bot
    coordinates = {
        'x': 2.25,
        'y': 0.25,
        'z': 4.75,
        'facing': 'FrontLeft'
    }


# =========================================================================
# REGISTROS DE CONSOLA
# =========================================================================

class loggers:
    SessionMetadata = True
    messages = True
    whispers = True
    joins = True
    leave = True
    tips = True
    emotes = False
    reactions = False
    userMovement = False


# =========================================================================
# MENSAJES PERSONALIZADOS
# =========================================================================

class messages:
    invalidPosition = "Your position could not be determined."
    invalidPlayer = "{user} is not in the room."
    invalidUser = "User {user} is not found."
    invalidUsage = "Usage: {prefix}{commandName}{args}"
    invalidUserFormat = "Invalid user format. Please use '@username'."


# =========================================================================
# PERMISOS
# =========================================================================

class permissions:
    owners = [
        '6ab1d5b3be121e4c4a3fe7d0',
        '670ee03a3fb7c8c6e59bbd76'
    ]

    moderators = [
        '6ab1d5b3be121e4c4a3fe7d0',
        '670ee03a3fb7c8c6e59bbd76'
    ]


# =========================================================================
# CREDENCIALES PRIVADAS: VARIABLES DE ENTORNO
# =========================================================================

class authorization:
    room = os.getenv("HIGHRISE_ROOM_ID", "").strip()
    token = os.getenv("HIGHRISE_API_TOKEN", "").strip()

    if not room:
        raise RuntimeError(
            "Falta configurar la variable de entorno HIGHRISE_ROOM_ID."
        )

    if not token:
        raise RuntimeError(
            "Falta configurar la variable de entorno HIGHRISE_API_TOKEN."
        )
