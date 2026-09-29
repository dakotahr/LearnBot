from highrise import User
from highrise.models import Position

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "dormir"
        self.description = "El bot se teletransporta y se acuesta a dormir al lado de un usuario. Uso: /dormir @usuario"
        self.permissions = ["moderation"] # Exclusivo para vos y tus moderadores
        self.cooldown = 3

    async def execute(self, user: User, args: list, message: str):
        # 1. Validación de argumentos
        if len(args) == 0:
            await self.bot.highrise.send_whisper(user.id, "⚠️ Uso correcto: /dormir @usuario\nEjemplo: /dormir @Pepe")
            return

        target_username = args.replace("@", "").strip().lower()

        try:
            # 2. El bot busca al usuario objetivo en la sala para copiar sus coordenadas
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

            # 3. ¡TELETRANSPORTACIÓN!: El bot se clava al lado del usuario usando su misma X y Z
            # Le sumamos un mini ajuste de 0.5 a la X para que quede paradito justo al lado y no encima
            await self.bot.highrise.teleport(
                self.bot.id,
                Position(
                    x=target_position.x + 0.5,
                    y=target_position.y,
                    z=target_position.z,
                    facing=target_position.facing
                )
            )

            # Anuncio divertido en el chat público
            await self.bot.highrise.chat(f"💤 Shhh... 🤫 @{user.username} mandó a beBot33 a dormir al lado de @{target_user.username}. ¡No hagan ruido! 🛏️")

            # 4. El bot se acuesta en el suelo usando su propia animación en loop
            await self.bot.highrise.send_emote("idle-loop-sitfloor")

        except Exception as e:
            print(f"Error en comando dormir interactivo: {e}")
            await self.bot.highrise.send_whisper(user.id, "❌ No pude mover al bot al lado del usuario.")
