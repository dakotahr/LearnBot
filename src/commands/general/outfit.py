import asyncio
from highrise import User
from highrise.models import Item

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "outfit"
        self.description = "Cambia el look del bot a sus conjuntos fijos. Uso: /outfit 1 o /outfit 2"
        self.permissions = [] # Libre para todos
        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):
        # 1. Validación de argumentos
        if not args:
            await self.bot.highrise.send_whisper(user.id, "⚠️ Uso correcto: /outfit 1 (Fábrica) o /outfit 2 (Elegante)")
            return

        # Arreglo clave: Obtenemos el texto del primer argumento de la lista
        opcion = args[0].strip()

        # =========================================================================
        # 👕 CONJUNTO 1: FACHA DE FÁBRICA TRADICIONAL
        # =========================================================================
        if opcion == "1":
            await self.bot.highrise.chat("👕 Cambiando al outfit 1 (Clásico de fábrica)... ✨")
            
            conjunto_1 = [
                Item(type='clothing', amount=1, id='hair_front-n_malenew05', account_bound=False),
                Item(type='clothing', amount=1, id='hair_back-n_malenew05', account_bound=False),
                Item(type='clothing', amount=1, id='eye-n_basic2018malesquaresleepy', account_bound=False),
                Item(type='clothing', amount=1, id='eyebrow-n_basic2018newbrows07', account_bound=False),
                Item(type='clothing', amount=1, id='nose-n_basic2018newnose05', account_bound=False),
                Item(type='clothing', amount=1, id='mouth-basic2018chippermouth', account_bound=False),
                Item(type='clothing', amount=1, id='freckle-n_basic2018freckle04', account_bound=False),
                Item(type='clothing', amount=1, id='shirt-n_room32019denimjackethoodie', account_bound=False),
                Item(type='clothing', amount=1, id='pants-n_starteritems2019cuffedjeanswhite', account_bound=False),
                Item(type='clothing', amount=1, id='shoes-n_room32019socksneakersgrey', account_bound=False)
            ]

            try:
                await self.bot.highrise.set_outfit(conjunto_1)
            except Exception as e:
                print(f"Error al cambiar al outfit 1: {e}")
                await self.bot.highrise.send_whisper(user.id, "❌ No se pudo aplicar el outfit 1. ¿El bot tiene estas prendas en su inventario?")

        # =========================================================================
        # 👔 CONJUNTO 2: LOOK CANCHERO CON MOCHILA Y CAMPERA UNIVERSITARIA
        # =========================================================================
        elif opcion == "2":
            await self.bot.highrise.chat("👔 Cambiando al outfit 2 (Canchero Universitario)... ✨")
            
            conjunto_2 = [
                Item(type='clothing', amount=1, id='eyebrow-n_basic2018newbrows07', account_bound=False),
                Item(type='clothing', amount=1, id='hair_front-n_malenew05', account_bound=False),
                Item(type='clothing', amount=1, id='hair_back-n_malenew05', account_bound=False),
                Item(type='clothing', amount=1, id='eye-n_animecollection2018bishoneneyes', account_bound=False),
                Item(type='clothing', amount=1, id='nose-n_basic2018newnose19', account_bound=False),
                Item(type='clothing', amount=1, id='mouth-basic2018thinpeaked', account_bound=False),
                Item(type='clothing', amount=1, id='hat-n_casualteenskypass2021brownsunglasses', account_bound=False),
                Item(type='clothing', amount=1, id='pants-n_room22019longcutoffsdenim', account_bound=False),
                # Se dejó únicamente 1 ítem de tipo shirt para evitar conflicto:
                Item(type='clothing', amount=1, id='shirt-n_vintagethriftjanuaryskypass2023varsityjacketdenim', account_bound=False),
                Item(type='clothing', amount=1, id='bag-n_junedailyrewardscow2018cowbackpack', account_bound=False),
                Item(type='clothing', amount=1, id='shoes-n_room12019sneakersblack', account_bound=False)
            ]

            try:
                await self.bot.highrise.set_outfit(conjunto_2)
            except Exception as e:
                print(f"Error al cambiar al outfit 2: {e}")
                await self.bot.highrise.send_whisper(user.id, "❌ No se pudo aplicar el outfit 2. ¿El bot es dueño de estas prendas?")

        else:
            await self.bot.highrise.send_whisper(user.id, "⚠️ Conjunto no encontrado. Elige entre 1 o 2.")
