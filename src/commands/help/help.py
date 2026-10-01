from highrise import User


class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = 'help'
        self.description = "Muestra los comandos disponibles"
        self.aliases = ['info', 'hmm']

        # Help es público para todos los usuarios.
        self.permissions = []

        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):
        comandos = self.bot.command_handler.commands

        await self.bot.highrise.send_whisper(
            user.id,
            "📚 Comandos disponibles:"
        )

        for nombre, comando in sorted(comandos.items()):
            descripcion = getattr(
                comando,
                "description",
                "Sin descripción"
            )

            await self.bot.highrise.send_whisper(
                user.id,
                f"/{nombre} - {descripcion}"
            )
