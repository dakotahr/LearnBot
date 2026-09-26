from highrise import User

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "dance"  # El comando será /dance [nombre-del-baile]
        self.description = "Ejecuta cualquier emote directamente por su ID técnico de Highrise."
        self.permissions = [] # Libre para todos los visitantes
        self.cooldown = 2

    async def execute(self, user: User, args: list, message: str):
        # 1. Si el usuario no escribió nada después de /dance, le avisamos
        if not args:
            await self.bot.highrise.send_whisper(user.id, "⚠️ Uso correcto: /dance [id-del-emote]\nEjemplo: /dance dance-macarena")
            return

        # 2. Convertimos la lista de argumentos en un solo texto y limpiamos espacios
        emote_id = " ".join(args).strip().lower()

        # 3. Ejecución del emote
        try:
            # Mandamos la orden directa al servidor de Highrise
            await self.bot.highrise.send_emote(emote_id, user.id)
            
        except Exception as e:
            # Si el ID no existe o falla el envío
            print(f"Error al ejecutar /dance directo: {e}")
            await self.bot.highrise.send_whisper(
                user.id, 
                f"❌ El nombre '{emote_id}' no parece ser un emote válido en Highrise. ¡Verifica cómo se escribe!"
            )
