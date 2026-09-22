# =========================================================================
# ⚙️ ARCHIVO DE CONFIGURACIÓN ORIGINAL DE HSEINHA (config/config.py)
# =========================================================================

class config:
    # CONFIGURACIÓN BÁSICA: Símbolo de comando, IDs, nombres y coordenadas iniciales.
    prefix = '/'
    botID = '6ab1d5b3be121e4c4a3fe7d0'    # ID de tu nuevo bot beBot33
    botName = 'beBot33'                  # Nombre oficial del nuevo bot
    ownerName = 'IamDakota'              # Tu nombre de usuario
    roomName = 'Sala de IamDakota'       # Nombre descriptivo para tu sala
    room = '69a113aed41925285a28e3cd'
    # Coordenadas exactas donde aparecerá el bot al entrar a la sala
    coordinates = {
        'x': 8.5,
        'y': 0.6000,
        'z': 20.5,
        'facing': 'FrontRight'
    }


class loggers:
    # REGISTROS DE CONSOLA: Controla qué eventos verás impresos en la consola de Render.
    SessionMetadata = True  # Muestra datos técnicos al conectar
    messages = True         # Imprime lo que la gente habla en el chat público
    whispers = True         # Imprime los susurros privados que recibe el bot
    joins = True            # Avisa cuando alguien entra a la sala
    leave = True            # Avisa cuando alguien se va de la sala
    tips = True             # Avisa si alguien da propinas de Gold
    emotes = False          # Desactivado: No satura la consola si la gente baila mucho
    reactions = False       # Desactivado: No avisa por cada corazón flotante
    userMovement = False    # Desactivado: No satura la consola cuando la gente camina


class messages:
    # MENSAJES PERSONALIZADOS: Respuestas automáticas que usarán los comandos modulares.
    invalidPosition = "Your position could not be determined."
    invalidPlayer = "{user} is not in the room."
    invalidUser = "User {user} is not found."
    invalidUsage = "Usage: {prefix}{commandName}{args}"
    invalidUserFormat = "Invalid user format. Please use '@username'."


class permissions:
    # RANGOS POR ID: Sistema interno de Haseinha para dar permisos absolutos.
    # Colocamos el ID de tu bot y podés sumar tu propio ID de usuario cuando lo consigas.
    owners = ['69a113aed41925285a28e3cd']       # IDs de los dueños con control total
    moderators = ['6ab1d5b3be121e4c4a3fe7d0']   # IDs de los moderadores de la sala


class authorization:
    # CREDENCIALES DE CONEXIÓN: Los datos críticos que lee main.py para encender el bot.
    room = '6894bd39e3e4a405517cb530'  # ID real de tu sala nueva para beBot33
    token = 'a3effb3099a112365e8d89aff24388b1a1e131d9473d8e97f351dfa86a2bac37'  # API Key de conexión
