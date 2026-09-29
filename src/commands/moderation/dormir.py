from highrise import User

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "dormir"
        self.description = "Interrumpe la acción de un usuario obligándolo a sentarse. Uso: /dormir @usuario"
        self.permissions = ["moderation"]  # Exclusivo para vos y tus moderadores
        self.cooldown = 2

    async def execute(self, user: User, args: list, message: str):
        # 1. Validación de argumentos
        if len(args) == 0:
            await self.bot.highrise.send_whisper(user.id, "⚠️ Uso correcto: /dormir @usuario\nEjemplo: /dormir @Pepe")
            return

        target_username = args.replace("@", "").strip().lower()

        try:
            # 2. El bot busca al usuario en la sala para extraer su ID
            response = await self.bot.highrise.get_room_users()
            users_in_room = [content for content in response.content]
            
            target_user = None
            for u, pos in users_in_room:
                if u.username.lower() == target_username:
                    target_user = u
                    break

            if not target_user:
                await self.bot.highrise.send_whisper(user.id, f"❌ El usuario '@{target_username}' no está en la sala.")
                return

            # 3. Anuncio público divertido en el chat
            await self.bot.highrise.chat(f"💤 ¡Zzz! @{user.username} mandó a dormir a @{target_user.username}. 🛏️")
            
            # 4. PASO TÉCNICO DE PRUEBA: Enviamos el emote directo usando el ID del jugador
            await self.bot.highrise.send_emote("idle-loop-sitfloor", target_user.id)

        except Exception as e:
            print(f"Error en comando dormir Prueba 1: {e}")
            await self.bot.highrise.send_whisper(user.id, "❌ No pude forzar la animación en el usuario.")
