from highrise import User

class Command:
def **init**(self, bot):
self.bot = bot
self.name = "inventario"
self.description = "Muestra la ropa que tiene el bot"
self.permissions = []
self.cooldown = 5

```
async def execute(self, user: User, args: list, message: str):
    try:
        inventario = await self.bot.highrise.get_inventory()

        await self.bot.highrise.send_whisper(
            user.id,
            f"Respuesta de inventario: {inventario}"
        )

        outfit = await self.bot.highrise.get_outfit()

        await self.bot.highrise.send_whisper(
            user.id,
            f"Respuesta de outfit: {outfit}"
        )

    except Exception as e:
        await self.bot.highrise.send_whisper(
            user.id,
            f"❌ Error al consultar:\n{type(e).__name__}: {e}"
        )
```
