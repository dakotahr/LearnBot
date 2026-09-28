from highrise import User
from highrise.models import Item

class Command:
def **init**(self, bot):
self.bot = bot
self.name = "outfit"
self.description = "Cambia el look del bot. Uso: /outfit 1 o /outfit 2"
self.permissions = []
self.cooldown = 5

```
async def execute(self, user: User, args: list, message: str):

    if not args:
        await self.bot.highrise.send_whisper(
            user.id,
            "⚠️ Uso: /outfit 1 o /outfit 2"
        )
        return

    opcion = args[0].strip()

    # ============================================================
    # OUTFIT 1 - SIN CAMBIOS
    # ============================================================

    if opcion == "1":

        await self.bot.highrise.chat(
            "👕 Cambiando al outfit 1... ✨"
        )

        conjunto_1 = [

            Item(
                type="clothing",
                amount=1,
                id="body-flesh",
                account_bound=False,
                active_palette=27
            ),

            Item(
                type="clothing",
                amount=1,
                id="hair_front-n_malenew05",
                account_bound=False
            ),

            Item(
                type="clothing",
                amount=1,
                id="hair_back-n_malenew05",
                account_bound=False
            ),

            Item(
                type="clothing",
                amount=1,
                id="eye-n_basic2018malesquaresleepy",
                account_bound=False
            ),

            Item(
                type="clothing",
                amount=1,
                id="eyebrow-n_basic2018newbrows07",
                account_bound=False
            ),

            Item(
                type="clothing",
                amount=1,
                id="nose-n_basic2018newnose05",
                account_bound=False
            ),

            Item(
                type="clothing",
                amount=1,
                id="mouth-basic2018chippermouth",
                account_bound=False
            ),

            Item(
                type="clothing",
                amount=1,
                id="freckle-n_basic2018freckle04",
                account_bound=False
            ),

            Item(
                type="clothing",
                amount=1,
                id="shirt-n_room32019denimjackethoodie",
                account_bound=False
            ),

            Item(
                type="clothing",
                amount=1,
                id="pants-n_starteritems2019cuffedjeanswhite",
                account_bound=False
            ),

            Item(
                type="clothing",
                amount=1,
                id="shoes-n_room32019socksneakersgrey",
                account_bound=False
            )
        ]

        try:

            await self.bot.highrise.set_outfit(conjunto_1)

            await self.bot.highrise.send_whisper(
                user.id,
                "✅ Outfit 1 aplicado correctamente."
            )

        except Exception as e:

            print(f"[OUTFIT 1] Error: {e}")

            await self.bot.highrise.send_whisper(
                user.id,
                "❌ No pude aplicar el outfit 1. Revisá los logs de Render."
            )

        return

    # ============================================================
    # OUTFIT 2 - BASADO EN LA LISTA QUE PASASTE
    # ============================================================

    elif opcion == "2":

        await self.bot.highrise.chat(
            "👔 Cambiando al outfit 2... ✨"
        )

        conjunto_2 = [

            Item(
                type="clothing",
                amount=1,
                id="body-flesh",
                account_bound=False,
                active_palette=1
            ),

            Item(
                type="clothing",
                amount=1,
                id="eyebrow-n_basic2018newbrows07",
                account_bound=False,
                active_palette=14
            ),

            Item(
                type="clothing",
                amount=1,
                id="nose-n_basic2018newnose05",
                account_bound=False,
                active_palette=0
            ),

            Item(
                type="clothing",
                amount=1,
                id="hair_front-n_malenew05",
                account_bound=False,
                active_palette=6
            ),

            Item(
                type="clothing",
                amount=1,
                id="hair_back-n_malenew05",
                account_bound=False,
                active_palette=6
            ),

            Item(
                type="clothing",
                amount=1,
                id="eye-n_animecollection2018bishoneneyes",
                account_bound=False,
                active_palette=22
            ),

            Item(
                type="clothing",
                amount=1,
                id="mouth-basic2018fullpeaked",
                account_bound=False,
                active_palette=22
            ),

            Item(
                type="clothing",
                amount=1,
                id="hat-n_casualteenskypass2021brownsunglasses",
                account_bound=False,
                active_palette=0
            ),

            Item(
                type="clothing",
                amount=1,
                id="shirt-n_room32019jerseywhite",
                account_bound=False,
                active_palette=0
            ),

            Item(
                type="clothing",
                amount=1,
                id="shirt-n_vintagethriftjanuaryskypass2023varsityjacketdenim",
                account_bound=False,
                active_palette=0
            ),

            Item(
                type="clothing",
                amount=1,
                id="shoes-n_room12019sneakersblack",
                account_bound=False,
                active_palette=0
            ),

            Item(
                type="clothing",
                amount=1,
                id="pants-n_room22019longcutoffsdenim",
                account_bound=False,
                active_palette=0
            ),

            Item(
                type="clothing",
                amount=1,
                id="bag-n_junedailyrewardscow2018cowbackpack",
                account_bound=False,
                active_palette=0
            )
        ]

        try:

            await self.bot.highrise.set_outfit(conjunto_2)

            await self.bot.highrise.send_whisper(
                user.id,
                "✅ Outfit 2 aplicado correctamente."
            )

        except Exception as e:

            print(f"[OUTFIT 2] Error: {e}")

            await self.bot.highrise.send_whisper(
                user.id,
                "❌ No pude aplicar el outfit 2. Revisá los logs de Render."
            )

        return

    # ============================================================
    # OPCIÓN INCORRECTA
    # ============================================================

    else:

        await self.bot.highrise.send_whisper(
            user.id,
            "⚠️ Outfit no encontrado. Usá /outfit 1 o /outfit 2."
        )
