from highrise import User


class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "veroutfit"
        self.description = "Muestra el outfit actual del bot"
        self.permissions = []
        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):

        try:

            respuesta = await self.bot.highrise.get_my_outfit()

            await self.bot.highrise.send_whisper(
                user.id,
                str(respuesta)
            )

        except Exception as e:

            print(f"[VEROUTFIT] Error: {e}")

            await self.bot.highrise.send_whisper(
                user.id,
                f"❌ Error al consultar outfit: {e}"
            )
