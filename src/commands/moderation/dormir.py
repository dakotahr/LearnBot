from highrise import User
from highrise.models import Position

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "dormir"
        self.description = "Manda a un usuario a dormir directo al suelo de la sala. Uso: /dormir @usuario"
        self.permissions = ["moderation"] # Solo dueños o moderadores autorizados
        self.cooldown = 2

    async def execute(self, user: User, args: list, message: str):
        # 1. Validación de argumentos (Necesitamos saber a quién tirar al suelo)
        if len(args) == 0:
            await self.bot.highrise.send_whisper(user.id, "⚠️ Uso correcto: /dormir @usuario\nEjemplo: /dormir @Pepe")
            return

        # Limpiamos el arroba si lo pusieron en el chat
        target_username = args.replace("@", "").strip().lower()

        try:
            # 2. El bot escanea la sala buscando al usuario objetivo
            response = await self.bot.highrise.get_room_users()
            users_in_room = [content for content in response.content]
            
            target_user = None
            target_position = None
            
            for u, pos in users_in_room:
                if u.username.lower() == target_username:
                    target_user = u
                    target_position = pos
                    break

            if not target_user:
                await self.bot.highrise.send_whisper(user.id, f"❌ El usuario '@{target_username}' no está en la sala.")
                return

            # 3. EL TRUCO MAGICO: Forzamos la teletransportación al ras del suelo (Y = 0.0)
            await self.bot.highrise.chat(f"💤 ¡Zzz! @{user.username} mandó a dormir a @{target_user.username} al suelo. 🛏️")
            
            # Teletransportamos al usuario manteniendo su X y su Z, pero bajando su Y a 0.0
            await self.bot.highrise.teleport(
                target_user.id,
                Position(
                    x=target_position.x,
                    y=0.0,  # El nivel del suelo absoluto de la sala
                    z=target_position.z,
                    facing=target_position.facing
                )
            )

            # 4. Le inyectamos el emote en bucle para que se quede sentado o acostado en el piso
            await self.bot.highrise.send_emote("idle-loop-sitfloor", target_user.id)

        except Exception as e:
            print(f"Error en comando dormir: {e}")
            await self.bot.highrise.send_whisper(user.id, "❌ Hubo un error técnico al intentar mandar a dormir al usuario.")
