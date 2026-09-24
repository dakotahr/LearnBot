from highrise import User

class Command:
def **init**(self, bot):
self.bot = bot
self.name = "inventario"
self.description = "Muestra el inventario y el outfit actual del bot"
self.permissions = []
self.cooldown = 5

```
async def execute(self, user: User, args: list, message: str):
    try:
        inventario = await self.bot.highrise.get_inventory()

        outfit = await self.bot.highrise.get_outfit()

        inventario_ids = []

        for item in inventario.items:
            inventario_ids.append(item.id)

        outfit_ids = []

        for item in outfit.items:
            outfit_ids.append(item.id)

        mensaje_inventario = "INVENTARIO DEL BOT\n\n"

        for item_id in inventario_ids:
            mensaje_inventario += f"- {item_id}\n"

        mensaje_outfit = "OUTFIT ACTUAL DEL BOT\n\n"

        for item_id in outfit_ids:
            mensaje_outfit += f"- {item_id}\n"

        await self.bot.highrise.send_whisper(
            user.id,
            mensaje_inventario
        )

        await self.bot.highrise.send_whisper(
            user.id,
            mensaje_outfit
        )

    except Exception as e:
        await self.bot.highrise.send_whisper(
            user.id,
            f"ERROR:\n{type(e).__name__}: {e}"
        )
```
