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
    
    # Coordenadas exactas donde aparecerá el bot al entrar a la sala
    coordinates = {
        'x': 8.5,
        'y': 0.6000,
        'z': 20.5,
        'facing': 'FrontRight'
    }


class loggers:
    # REGISTROS DE CONSOLA: Controla qué eventos verás impresos en la consola de Render.
    SessionMetadata = True  
    messages = True         
    whispers = True         
    joins = True            
    leave = True            
    tips = True             
    emotes = False          
    reactions = False       
    userMovement = False    


class messages:
    # MENSAJES PERSONALIZADOS: Respuestas automáticas que usarán los comandos modulares.
    invalidPosition = "Your position could not be determined."
    invalidPlayer = "{user} is not in the room."
    invalidUser = "User {user} is not found."
    invalidUsage = "Usage: {prefix}{commandName}{args}"
    invalidUserFormat = "Invalid user format. Please use '@username'."


class permissions:
    # RANGOS POR ID: Sistema interno de Haseinha para dar permisos absolutos.
    # Colocamos el ID de tu bot en owners y en moderators para que tenga control total.
    owners = ['6ab1d5b3be121e4c4a3fe7d0' , '670ee03a3fb7c8c6e59bbd76]       
    moderators = ['6ab1d5b3be121e4c4a3fe7d0' , '670ee03a3fb7c8c6e59bbd76]   


class authorization:
    # CREDENCIALES DE CONEXIÓN: Los datos críticos que lee main.py para encender el bot.
    # ¡CORREGIDO! Ahora ambos usan el ID real de tu sala: 69a113aed41925285a28e3cd
    room = '69a113aed41925285a28e3cd'  
    token = 'a3effb3099a112365e8d89aff24388b1a1e131d9473d8e97f351dfa86a2bac37'  # API Key de conexión
