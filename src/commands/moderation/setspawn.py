from highrise import User
from highrise.models import Position

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "setspawn"
        self.description = "Guarda tu posición actual en la memoria del bot como su nuevo punto de aparición."
        self.permissions = ["moderation"]
        self.cooldown = 3

    async def execute(self, user: User, args: list, message: str):
        await self.bot.highrise.chat("⚙️ Escaneando coordenadas en tiempo real...")
        
        try:
            # 1. Buscamos tu posición actual en la sala
            response = await self.bot.highrise.get_room_users()
            tu_posicion = None
            
            for user_in_room, position in response.content:
                if user_in_room.id == user.id:
                    tu_posicion = position
                    break

            if not tu_posicion or not isinstance(tu_posicion, Position):
                await self.bot.highrise.send_whisper(user.id, "❌ No pude detectar tus coordenadas. Muévete un paso e intenta de nuevo.")
                return

            # 2. ¡LA MAGIA DE MEMORIA!: Guardamos la posición directo en las variables del bot
            self.bot.coordenadas_fijas = {
                "x": tu_posicion.x,
                "y": tu_posicion.y,
                "z": tu_posicion.z,
                "facing": tu_posicion.facing
            }

            await self.bot.highrise.chat(f"📍 ¡Punto de aparición memorizado con éxito! El bot vendrá aquí cada vez que entre a la sala. ✨")

        except Exception as e:
            print(f"Error en comando setspawn por memoria: {e}")
            await self.bot.highrise.send_whisper(user.id, "❌ Ocurrió un error al intentar memorizar la posición.")
