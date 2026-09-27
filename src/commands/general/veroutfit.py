from highrise import User


class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "veroutfit"
        self.description = "Muestra las paletas activas del pelo, piel, ojos y rostro"
        self.permissions = []
        self.cooldown = 5

    async def execute(self, user: User, args: list):
        try:
            outfit = await self.bot.highrise.get_my_outfit()

            mensaje = "🎨 Paletas activas:\n\n"

            for item in outfit.outfit:
                item_id = item.id

                if (
                    item_id.startswith("hair_")
                    or item_id == "body-flesh"
                    or item_id.startswith("eye-")
                    or item_id.startswith("eyebrow-")
                    or item_id.startswith("nose-")
                    or item_id.startswith("mouth-")
                    or item_id.startswith("freckle-")
                    or "facial" in item_id
                    or "beard" in item_id
                    or "mustache" in item_id
                ):
                    mensaje += (
                        f"{item_id}\n"
                        f"Paleta: {item.active_palette}\n\n"
                    )

            await self.bot.highrise.send_whisper(user.id, mensaje)

        except Exception as e:
            await self.bot.highrise.send_whisper(
                user.id,
                f"❌ Error:\n{type(e).__name__}: {e}"
            )
