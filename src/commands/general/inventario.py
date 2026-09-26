from highrise import User

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "inventario"
        self.description = "Muestra un resumen de la ropa que tiene el bot"
        self.permissions = []
        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):
        try:
            # 1. Obtener inventario
            inventario_data = await self.bot.highrise.get_inventory()
            
            # Si el SDK devuelve tupla o lista, extraemos los items
            items = inventario_data.items if hasattr(inventario_data, 'items') else inventario_data

            total_items = len(items)
            
            # Tomamos solo los IDs de los primeros 5 ítems para no pasar el límite de texto
            ejemplos_items = [item.id for item in items[:5]]
            texto_items = "\n• ".join(ejemplos_items) if ejemplos_items else "Sin ítems"

            await self.bot.highrise.send_whisper(
                user.id,
                f"📦 Total en inventario: {total_items} prendas.\nPrimeras prendas:\n• {texto_items}"
            )

            # 2. Obtener outfit actual
            outfit_data = await self.bot.highrise.get_my_outfit()
            
            outfit_items = outfit_data.outfit if hasattr(outfit_data, 'outfit') else outfit_data
            ejemplos_outfit = [item.id for item in outfit_items[:5]]
            texto_outfit = "\n• ".join(ejemplos_outfit) if ejemplos_outfit else "Sin outfit"

            await self.bot.highrise.send_whisper(
                user.id,
                f"👕 Prendas equipadas actualmente ({len(outfit_items)}):\n• {texto_outfit}"
            )

        except Exception as e:
            print(f"Error en inventario: {e}")
            await self.bot.highrise.send_whisper(
                user.id,
                f"❌ Error al consultar inventario:\n{type(e).__name__}: {e}"
            )
