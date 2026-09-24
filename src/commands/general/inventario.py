from highrise import User

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "inventario"
        self.description = "Muestra la ropa que tiene el bot"
        self.permissions = []
        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):
        try:
            inventario = await self.bot.highrise.get_inventory()

            if not inventario:
                await self.bot.highrise.send_whisper(
                    user.id,
                    "El bot no tiene prendas en su inventario."
                )
                return

            mensaje = "👕 Ropa que tiene el bot:\n"

            for item in inventario:
                mensaje += f"\nID: {item.id}"

            await self.bot.highrise.send_whisper(user.id, mensaje)

        except Exception as e:
            print(f"Error al obtener el inventario: {e}")
            await self.bot.highrise.send_whisper(
                user.id,
                "No pude consultar el inventario del bot."
            )
