import json
from highrise import User
from highrise.models import Position

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "setspawn"
        self.description = "Guarda tu posición actual como el nuevo punto de aparición del bot."
        self.permissions = ["moderation"] # Solo vos podés usarlo
        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):
        await self.bot.highrise.chat("⚙️ Escaneando coordenadas actuales...")
        
        try:
            # 1. Buscamos tu posición exacta en la sala
            response = await self.bot.highrise.get_room_users()
            tu_posicion = None
            
            for user_in_room, position in response.content:
                if user_in_room.id == user.id:
                    tu_posicion = position
                    break

            if not tu_posicion or not isinstance(tu_posicion, Position):
                await self.bot.highrise.send_whisper(user.id, "❌ No pude detectar tus coordenadas. Muévete un paso e intenta de nuevo.")
                return

            # 2. Armamos la estructura de datos igualita al config.py
            datos_spawn = {
                "x": tu_posicion.x,
                "y": tu_posicion.y,
                "z": tu_posicion.z,
                "facing": str(tu_posicion.facing)
            }

            # 3. ¡LA MAGIA!: Escribimos el archivo en el disco de Render para que no se borre
            ruta_archivo = 'config/json/spawn.json'
            with open(ruta_archivo, 'w') as f:
                json.dump(datos_spawn, f, indent=4)

            await self.bot.highrise.chat(f"📍 ¡Nuevo punto de aparición fijado con éxito! X:{tu_posicion.x:.2f} Y:{tu_posicion.y:.2f} Z:{tu_posicion.z:.2f} ✨")

        except Exception as e:
            print(f"Error en comando setspawn: {e}")
            await self.bot.highrise.send_whisper(user.id, "❌ Ocurrió un error al intentar guardar las coordenadas.")
