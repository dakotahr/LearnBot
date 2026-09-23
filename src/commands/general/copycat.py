from highrise import User

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "copycat"
        self.description = "Hace que el bot imite los bailes de un usuario específico. Uso: /copycat @usuario o /copycat stop"
        self.permissions = []  # Libre para que lo usen tus visitantes si querés
        self.cooldown = 2

        # Inicializamos la variable interna en el bot si no existe
        if not hasattr(bot, 'usuario_a_imitar'):
            bot.usuario_a_imitar = None

    async def execute(self, user: User, args: list, message: str):
        # 1. Modo para DETENER la imitación
        if len(args) > 0 and args[0].lower() == 'stop':
            self.bot.usuario_a_imitar = None
            await self.bot.highrise.send_whisper(user.id, "🛑 Sistema de imitación desactivado.")
            return

        # 2. Validación de argumentos
        if len(args) == 0:
            await self.bot.highrise.send_whisper(user.id, "Uso correcto: /copycat @usuario o /copycat stop")
            return

        # Limpiamos el arroba si lo pusieron
        objetivo = args[0].replace("@", "").strip().lower()

        # 3. Buscamos si el usuario objetivo está realmente en la sala
        try:
            response = await self.bot.highrise.get_room_users()
            users_in_room = [content[0] for content in response.content]
            
            target_user = next((u for u in users_in_room if u.username.lower() == objetivo), None)
            
            if target_user:
                # Guardamos el ID del usuario en la memoria del bot
                self.bot.usuario_a_imitar = target_user.id
                await self.bot.highrise.chat(f"🤖 Modo espejo activado. Ahora imitando a @{target_user.username} ✨")
            else:
                await self.bot.highrise.send_whisper(user.id, f"El usuario '@{objetivo}' no se encuentra en esta sala.")
        except Exception as e:
            print(f"Error en comando copycat: {e}")
