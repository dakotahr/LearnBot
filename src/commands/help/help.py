from highrise import User


class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = 'help'
        self.description = "Muestra la lista de comandos disponibles"
        self.aliases = ['info', 'hmm']
        self.permissions = []
        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):
        await self.bot.highrise.send_whisper(
            user.id,
            "📚 COMANDOS DISPONIBLES:\n"
            "/help - Muestra esta ayuda\n"
            "/info - Alias de help\n"
            "/hmm - Alias de help\n"
            "/outfit - Cambia el look del bot\n"
            "/inventario - Muestra el inventario\n"
            "/cloname - Clona el look de un usuario"
        )
