from highrise import User

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "inventario"
        self.description = "Muestra el código exacto de la ropa equipada"
        self.permissions = []
        self.cooldown = 2

    async def execute(self, user: User, args: list, message: str):
        try:
            # Obtenemos el outfit actual
            response = await self.bot.highrise.get_my_outfit()
            items = response.outfit if hasattr(response, 'outfit') else response

            if not items:
                await self.bot.highrise.send_whisper(user.id, "❌ El bot no tiene prendas equipadas.")
                return

            await self.bot.highrise.send_whisper(user.id, f"📋 Copia estas prendas ({len(items)} en total):")

            # Enviamos las prendas en bloques pequeños para que Highrise no las bloquee
            bloque = ""
            for i, item in enumerate(items, 1):
                linea = f"Item(type='clothing', amount=1, id='{item.id}', account_bound=False),\n"
                
                # Si sobrepasa los 200 caracteres, enviamos el mensaje y empezamos uno nuevo
                if len(bloque) + len(linea) > 200:
                    await self.bot.highrise.send_whisper(user.id, bloque)
                    bloque = linea
                else:
                    bloque += linea

            # Enviamos lo que quede pendiente
            if bloque:
                await self.bot.highrise.send_whisper(user.id, bloque)

        except Exception as e:
            await self.bot.highrise.send_whisper(user.id, f"❌ Error: {e}")
