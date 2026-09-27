from highrise import User

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "veroutfit"
        self.description = "Prueba del comando veroutfit"
        self.permissions = []
        self.cooldown = 5

    async def execute(self, user: User, args: list):
        await self.bot.highrise.send_whisper(
            user.id,
            "OK - el comando veroutfit funciona."
        )
