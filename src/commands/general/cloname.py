import asyncio
from highrise import User

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "cloname"
        self.description = "Maneja los outfits del bot. Uso: /cloname | /cloname 1 | /cloname 2"
        self.permissions = []
        self.cooldown = 3

        # Inicializamos los casilleros de memoria en el bot si no existen
        if not hasattr(bot, 'outfit_fabrica'):
            bot.outfit_fabrica = None  # Casillero 1 (Fábrica)
        if not hasattr(bot, 'outfit_clonado'):
            bot.outfit_clonado = None  # Casillero 2 (Tu look)

    async def execute(self, user: User, args: list, message: str):
        # Unimos los argumentos por si pasaron un número (ejemplo: ['1'] -> '1')
        opcion = " ".join(args).strip()

        # =========================================================================
        # 👗 CAMBIAR AL OUTFIT 1 (/cloname 1)
        # =========================================================================
        if opcion == "1":
            if self.bot.outfit_fabrica:
                await self.bot.highrise.chat("👕 Volviendo al outfit 1 (Ropa de fábrica)...")
                try:
                    await self.bot.highrise.set_outfit(self.bot.outfit_fabrica)
                except Exception as e:
                    print(f"Error al poner outfit 1: {e}")
            else:
                await self.bot.highrise.send_whisper(user.id, "Aún no tengo guardado mi outfit de fábrica. Usa /cloname solo primero.")
            return

        # =========================================================================
        # 👗 CAMBIAR AL OUTFIT 2 (/cloname 2)
        # =========================================================================
        elif opcion == "2":
            if self.bot.outfit_clonado:
                await self.bot.highrise.chat("✨ Cambiando al outfit 2 (Clonado)...")
                try:
                    await self.bot.highrise.set_outfit(self.bot.outfit_clonado)
                except Exception as e:
                    print(f"Error al poner outfit 2: {e}")
            else:
                await self.bot.highrise.send_whisper(user.id, "No hay ningún outfit clonado guardado. Usa /cloname solo primero.")
            return

        # =========================================================================
        # 👥 ACCIÓN PRINCIPAL: /cloname (A secas)
        # =========================================================================
        await self.bot.highrise.chat("🤖 Analizando y memorizando estilos...")

        try:
            # 1. El bot memoriza su propia ropa actual antes de cambiarla (Outfit 1)
            if self.bot.outfit_fabrica is None:
                resultado_bot = await self.bot.highrise.get_my_outfit()
                self.bot.outfit_fabrica = resultado_bot.outfit
                print("✅ Outfit de fábrica del bot guardado con éxito.")

            # 2. El bot lee los códigos exactos de la ropa que llevas puesta VOS
            resultado_usuario = await self.bot.highrise.get_user_outfit(user.id)
            tu_ropa = resultado_usuario.outfit

            # 3. Guardamos tu lista de ropa en el casillero 2
            self.bot.outfit_clonado = tu_ropa

            # 4. Le ordenamos al bot vestirse exactamente igual a vos
            await self.bot.highrise.set_outfit(tu_ropa)
            await self.bot.highrise.chat("✨ ¡Clonación exitosa! Guardado como Outfit 2. Usa '/cloname 1' para volver a fábrica.")

        except Exception as e:
            print(f"Error en clonación avanzada: {e}")
            await self.bot.highrise.send_whisper(user.id, "❌ No pude clonar tu ropa. Asegúrate de usar prendas básicas de fábrica.")
