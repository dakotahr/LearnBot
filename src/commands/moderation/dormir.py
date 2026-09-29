from highrise import User

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "dormir"
        self.description = "Sanciona a un usuario mandándolo a dormir afuera (Expulsión/Kick). Uso: /dormir @usuario"
        self.permissions = ["moderation"] # Exclusivo para vos y tus moderadores
        self.cooldown = 3

    async def execute(self, user: User, args: list, message: str):
        # 1. Validación de argumentos
        if len(args) == 0:
            await self.bot.highrise.send_whisper(user.id, "⚠️ Uso correcto: /dormir @usuario\nEjemplo: /dormir @Pepe")
            return

        target_username = args.replace("@", "").strip().lower()

        # Evitamos que te expulses a vos mismo por error
        if target_username == "iamdakota":
            await self.bot.highrise.send_whisper(user.id, "❌ No podés mandarte a dormir afuera a vos mismo, crack.")
            return

        try:
            # 2. El bot busca al usuario en la sala para extraer su ID único
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

            # 3. Anuncio público en el chat de la sala
            await self.bot.highrise.chat(f"🚪 💤 ¡A dormir afuera! @{user.username} mandó a dormir a @{target_user.username} fuera de la sala.")

            # 4. 🔥 EL PODER DE MODERACIÓN REAL: Expulsamos al usuario de la sala
            # Usamos la función nativa oficial para dar Kick instantáneo
            await self.bot.highrise.moderate_room(
                user_id=target_user.id,
                action="kick"
            )

        except Exception as e:
            print(f"Error en comando dormir estilo kick: {e}")
            await self.bot.highrise.send_whisper(user.id, "❌ No pude expulsar al usuario. Verifica si el bot tiene rango de Moderador de la sala.")
