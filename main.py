# =========================================================================
# SECTOR 1: IMPORTACIONES (Las herramientas que usará el script)
# =========================================================================
import threading  # Permite ejecutar Flask en paralelo sin detener el bot
import os         # ¡AÑADIDO!: Permite revisar si existen archivos en Render
import json       # ¡AÑADIDO!: Permite leer y descifrar el mapa del spawn
from flask import Flask  # Crea la web falsa para Render

from highrise import BaseBot
from highrise import __main__
from highrise.models import AnchorPosition, CurrencyItem, Item, Position, Reaction, SessionMetadata, User

# ¡AQUÍ ESTÁ EL SECRETO REUTILIZABLE! 
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
    return "¡Servidor Modular de Haseinha Activo 24/7!", 200

def run_flask():
    app.run(host='0.0.0.0', port=10000)

threading.Thread(target=run_flask, daemon=True).start()


# =========================================================================
# SECTOR 3: LA CLASE BOT Y ENRUTAMIENTO DE EVENTOS
# =========================================================================
class Bot(BaseBot):
    def __init__(self):
        self.command_handler = CommandHandler(self)
        super().__init__()

    # Cuando el bot se conecta con éxito...
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        # En rutan los procesos base de Haseinha
        await handle_start(self, session_metadata)
        
        # 🔮 CIRCUITO DE APARICIÓN INTELIGENTE (/setspawn):
        # Ni bien enciende, el bot revisa si guardaste un punto de nacimiento dinámico
        ruta_spawn = 'config/json/spawn.json'
        if os.path.exists(ruta_spawn):
            try:
                with open(ruta_spawn, 'r') as f:
                    datos = json.load(f)
                    
                print("📌 Ajustando coordenadas: Moviendo bot al punto personalizado de spawn.json")
                # El bot se teletransporta automáticamente al lugar exacto que elegiste
                await self.highrise.walk_to(
                    Position(
                        x=datos["x"],
                        y=datos["y"],
                        z=datos["z"],
                        facing=datos["facing"]
                    )
                )
            except Exception as e:
                print(f"Error al mover el bot al spawn personalizado: {e}")

    # Cuando alguien habla por el chat público...
    async def on_chat(self, user: User, message: str) -> None:
        await handle_chat(self, user, message)

    # Cuando alguien le habla por privado (susurro) al bot...
    async def on_whisper(self, user: User, message: str) -> None:
        await handle_whisper(self, user, message)

    # Cuando un jugador entra a la sala...
    async def on_user_join(self, user: User) -> None:
        await handle_join(self, user)

    # Cuando un jugador se va de la sala...
    async def on_user_leave(self, user: User) -> None:
        await handle_leave(self, user)

    # Cuando alguien tira un emote/baile en la sala...
    async def on_emote(self, user: User, emote_id: str, receiver: User | None) -> None:
        await handle_emote(self, user, emote_id, receiver)

    # Cuando un usuario le da propina (Gold/Tip) al bot o a otro jugador...
    async def on_tip(self, sender: User, receiver: User, tip: CurrencyItem | Item) -> None:
        await handle_tips(self, sender, receiver, tip)

    # Cuando alguien usa una reacción (como un corazón o un aplauso flotante)...
    async def on_reaction(self, user: User, reaction: Reaction, receiver: User) -> None:
        await handle_reactions(self, user, reaction, receiver)

    # Cuando cualquier usuario camina o se teletransporta en el mapa...
    async def on_user_move(self, user: User, destination: Position | AnchorPosition) -> None:
        await handle_movements(self, user, destination)

    # Método interno para arrancar el bucle principal de Highrise
    async def run(self, room_id, token):
        await __main__.main(self, room_id, token)


# =========================================================================
# SECTOR 4: ARRANQUE AUTOMÁTICO (Solución Definitiva Asíncrona)
# =========================================================================
if __name__ == "__main__":
    import asyncio  
    from highrise.__main__ import main, BotDefinition
    
    room_id = authorization.room
    token = authorization.token
    
    definitions = [BotDefinition(Bot(), room_id, token)]
    
    asyncio.run(main(definitions))
