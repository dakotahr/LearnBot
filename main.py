# =========================================================================
# SECTOR 1: IMPORTACIONES (Las herramientas que usará el script)
# =========================================================================
import threading  # Permite ejecutar Flask en paralelo sin detener el bot
from flask import Flask  # Crea la web falsa para Render

from highrise import BaseBot
from highrise import __main__
from highrise.models import AnchorPosition, CurrencyItem, Item, Position, Reaction, SessionMetadata, User

# ¡AQUÍ ESTÁ EL SECRETO REUTILIZABLE! 
# Haseinha no escribe los comandos acá. Los importa desde otros archivos de la carpeta "src"
from src.handlers.handleEvents import handle_chat, handle_join, handle_leave, handle_start, handle_whisper, handle_emote, handle_tips, handle_reactions, handle_movements
from src.handlers.handleCommands import CommandHandler

from asyncio import run as arun
from config.config import authorization


# =========================================================================
# SECTOR 2: SERVIDOR FLASK (Parche obligatorio para Render Gratis)
# =========================================================================
app = Flask(__name__)

@app.route('/')
def home():
    # Esta página responderá con un texto simple cuando UptimeRobot la visite
    return "¡Servidor Modular de Haseinha Activo 24/7!", 200

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# Iniciamos la web en un hilo secundario (background) para que no interfiera con el bot
threading.Thread(target=run_flask, daemon=True).start()


# =========================================================================
# SECTOR 3: LA CLASE BOT Y ENRUTAMIENTO DE EVENTOS
# =========================================================================
class Bot(BaseBot):
    def __init__(self):
        # Inicializa el manejador de comandos que procesará las órdenes del chat
        self.command_handler = CommandHandler(self)
        super().__init__()

    # Cuando el bot se conecta con éxito...
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        # En vez de escribir código acá, se lo manda a la función "handle_start" en handleEvents.py
        await handle_start(self, session_metadata)

    # Cuando alguien habla por el chat público...
    async def on_chat(self, user: User, message: str) -> None:
        # Envía el mensaje directo a "handle_chat" para ver si es un comando o un texto normal
        await handle_chat(self, user, message)

    # Cuando alguien le habla por privado (susurro) al bot...
    async def on_whisper(self, user: User, message: str) -> None:
        await handle_whisper(self, user, message)

    # Cuando un jugador entra a la sala...
    async def on_user_join(self, user: User) -> None:
        # Va al archivo handleEvents.py, donde seguro está el mensaje de bienvenida o el contador
        await handle_join(self, user)

    # Cuando un jugador se va de la sala...
    async def on_user_leave(self, user: User) -> None:
        await handle_leave(self, user)

    # Cuando alguien tira un emote/baile en la sala...
    async def on_emote(self, user: User, emote_id: str, receiver: User | None) -> None:
        # Envía los datos aquí. Ideal si querés que el bot reaccione o imite el baile
        await handle_emote(self, user, emote_id, receiver)

    # Cuando un usuario le da propina (Gold/Tip) al bot o a otro jugador...
    async def on_tip(self, sender: User, receiver: User, tip: CurrencyItem | Item) -> None:
        # Útil para bots de economía, juegos de azar o agradecer donaciones automáticamente
        await handle_tips(self, sender, receiver, tip)

    # Cuando alguien usa una reacción (como un corazón o un aplauso flotante)...
    async def on_reaction(self, user: User, reaction: Reaction, receiver: User) -> None:
        await handle_reactions(self, user, reaction, receiver)

    # Cuando cualquier usuario camina o se teletransporta en el mapa...
    async def on_user_move(self, user: User, destination: Position | AnchorPosition) -> None:
        # Envía las coordenadas actuales del usuario a "handle_movements". 
        # (¡Acá es donde se procesa la lógica de seguimiento inteligente!)
        await handle_movements(self, user, destination)

    # Método interno para arrancar el bucle principal de Highrise
    async def run(self, room_id, token):
        await __main__.main(self, room_id, token)


# =========================================================================
# SECTOR 4: ARRANQUE AUTOMÁTICO (Punto de Entrada)
# =========================================================================
if __name__ == "__main__":
    # Lee de forma automática las variables guardadas dentro de tu config/config.py
    room_id = authorization.room
    token = authorization.token
    
    # Enciende el bot pasándole las credenciales obtenidas
    arun(Bot().run(room_id, token))
