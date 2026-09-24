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
        # ============================================================
        # 📦 INVENTARIO
        # ============================================================
        inventario = await self.bot.highrise.get_inventory()

        # ============================================================
        # 👕 OUTFIT ACTUAL
        # ============================================================
        outfit = await self.bot.highrise.get_outfit()

        # ------------------------------------------------------------
        # Convertimos el inventario a una lista más fácil de leer
        # ------------------------------------------------------------
        inventario_ids = []

        for item in inventario.items:
            inventario_ids.append(item.id)

        # ------------------------------------------------------------
        # Convertimos el outfit actual a una lista más fácil de leer
        # ------------------------------------------------------------
        outfit_ids = []

        for item in outfit:
            outfit_ids.append(item.id)

        # ------------------------------------------------------------
        # Mensaje del inventario
        # ------------------------------------------------------------
        mensaje_inventario = (
            "📦 INVENTARIO DEL BOT\n\n"
            + "\n".join(f"- {item_id}" for item_id in inventario_ids)
        )

        # ------------------------------------------------------------
        # Mensaje del outfit actual
        # ------------------------------------------------------------
        mensaje_outfit = (
            "👕 OUTFIT ACTUAL DEL BOT\n\n"
            + "\n".join(f"- {item_id}" for item_id in outfit_ids)
        )

        # ------------------------------------------------------------
        # Enviamos ambos resultados por whisper
        # ------------------------------------------------------------
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
            f"❌ Error al consultar:\n"
            f"{type(e).__name__}: {e}"
        )
```
