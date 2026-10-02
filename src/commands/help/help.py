from highrise import User


class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = 'help'
        self.description = "Muestra los comandos disponibles"
        self.aliases = ['info', 'hmm']
        self.permissions = []
        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):
        # ============================================================
        # EDITA SOLAMENTE ESTA LISTA SI QUIERES CAMBIAR LOS COMANDOS
        # QUE APARECEN EN /help.
        #
        # Para agregar un comando: "nombre",
        # Para quitarlo: elimina su línea.
        # ============================================================
        comandos_ayuda = [
            "dance",
            "dejar",
            "loop",
            "me",
            "test",
            "help",
            "wallet",
        ]

        # ============================================================
        # NO NECESITAS EDITAR NADA DE ABAJO
        # ============================================================
        await self.bot.highrise.send_whisper(
            user.id,
            "📚 COMANDOS DISPONIBLES:"
        )

        for nombre in comandos_ayuda:
            comando = self.bot.command_handler.commands.get(nombre)

            if comando:
                descripcion = getattr(
                    comando,
                    "description",
                    "Sin descripción"
                )

                await self.bot.highrise.send_whisper(
                    user.id,
                    f"/{nombre} - {descripcion}"
                )
