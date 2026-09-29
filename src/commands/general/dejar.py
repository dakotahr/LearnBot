from highrise import User

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "dejar"
        self.description = "Deja un mensaje secreto estilo MSN para otro usuario de la sala. Uso: /dejar @usuario mensaje"
        self.permissions = [] # Libre para todos tus visitantes
        self.cooldown = 3

        # Inicializamos la base de datos de mensajes en la RAM si no existe
        if not hasattr(bot, 'mensajes_msn'):
            bot.mensajes_msn = {}

    async def execute(self, user: User, args: list, message: str):
        # 1. Validación de argumentos (Necesitamos al menos el @usuario y una palabra)
        if len(args) < 2:
            await self.bot.highrise.send_whisper(user.id, "⚠️ Uso correcto: /dejar @usuario [tu mensaje]\nEjemplo: /dejar @Pepe ya vuelvo, fui a tomar agua")
            return

        target_username = args[0].replace("@", "").strip().lower()
        texto_mensaje = " ".join(args[1:]).strip()

        # 2. El bot verifica si el destinatario está actualmente en la sala
        try:
            response = await self.bot.highrise.get_room_users()
            users_in_room = [content for content in response.content]
            
            target_user = next((u for u, pos in users_in_room if u.username.lower() == target_username), None)
            
            if not target_user:
                await self.bot.highrise.send_whisper(user.id, f"❌ El usuario '@{target_username}' no está en la sala actual para recibir el mensaje.")
                return

            if target_user.id == user.id:
                await self.bot.highrise.send_whisper(user.id, "😂 No tiene sentido dejarte un mensaje secreto a vos mismo.")
                return

            # 3. ¡GUARDAMOS EL RECADO!: Estructuramos el mensaje en la memoria viva
            # Si el usuario ya tenía mensajes pendientes, se los sumamos como una lista
            if target_user.id not in self.bot.mensajes_msn:
                self.bot.mensajes_msn[target_user.id] = []
                
            self.bot.mensajes_msn[target_user.id].append({
                "remitente": user.username,
                "texto": texto_mensaje
            })

            # Confirmación privada al remitente
            await self.bot.highrise.send_whisper(user.id, f"✅ ¡Mensaje guardado! Se lo entregaré en privado a @{target_user.username} apenas hable en el chat. ✉️")

        except Exception as e:
            print(f"Error en comando dejar: {e}")
            await self.bot.highrise.send_whisper(user.id, "❌ Ocurrió un error técnico al intentar procesar el recado.")
