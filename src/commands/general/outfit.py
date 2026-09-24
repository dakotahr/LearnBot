import asyncio
from highrise import User
from highrise.models import Item

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "outfit"
        self.description = "Cambia el conjunto de ropa del bot. Uso: /outfit 1 o /outfit 2"
        self.permissions = []  # Libre por si querés que la gente lo cambie, o poné tu restricción
        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):
        if len(args) == 0:
            await self.bot.highrise.send_whisper(user.id, "Uso correcto: /outfit 1 o /outfit 2")
            return

        opcion = args[0].strip()

        # =========================================================================
        # 👗 CONFIGURACIÓN DE TUS CONJUNTOS (IDs Técnicos de Ropa)
        # =========================================================================
        # Nota para Dakota: Mañana buscaremos los IDs reales de la ropa que le regalaste
        # y los reemplazaremos acá adentro de las comillas simples.
        
        if opcion == "1":
            await self.bot.highrise.chat("👕 Cambiando al conjunto informal...")
            nuevo_look = [
                Item(type='clothing', amount=1, id='body-flesh', account_bound=False), # Base del cuerpo
                Item(type='clothing', amount=1, id='shirt-n_basicshirt', account_bound=False), # Reemplazar ID de remera
                Item(type='clothing', amount=1, id='pants-n_basicpants', account_bound=False), # Reemplazar ID de pantalón
            ]
            
        elif opcion == "2":
            await self.bot.highrise.chat("👔 Cambiando al conjunto elegante...")
            nuevo_look = [
                Item(type='clothing', amount=1, id='body-flesh', account_bound=False),
                Item(type='clothing', amount=1, id='shirt-n_suitshirt', account_bound=False), # Reemplazar ID de remera 2
                Item(type='clothing', amount=1, id='pants-n_suitpants', account_bound=False), # Reemplazar ID de pantalón 2
            ]
        else:
            await self.bot.highrise.send_whisper(user.id, "Conjunto no encontrado. Elige 1 o 2.")
            return

        # Execución del cambio de ropa en el servidor de Highrise
        try:
            await self.bot.highrise.set_outfit(nuevo_look)
        except Exception as e:
            print(f"Error al cambiar outfit: {e}")
            await self.bot.highrise.send_whisper(user.id, "No se pudo cambiar la ropa. Verifica si el bot es dueño de esos ítems.")
