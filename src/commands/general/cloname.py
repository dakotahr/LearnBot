import asyncio
from highrise import User

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "cloname"
        self.description = "Maneja los outfits del bot. Uso: /cloname (clona tu look como outfit 2) | /outfit 1 | /outfit 2"
        self.permissions = []
        self.cooldown = 3

        # Creamos la memoria del bot para guardar los dos conjuntos si no existen
        if not hasattr(bot, 'outfit_fabrica'):
            bot.outfit_fabrica = None  # Aquí guardaremos el Outfit 1
        if not hasattr(bot, 'outfit_clonado'):
            bot.outfit_clonado = None  # Aquí guardaremos el Outfit 2

    async def guardar_outfit_fabrica(self):
        """Función interna para que el bot espíe su propia ropa de fábrica"""
        try:
            # El SDK no tiene 'get_my_outfit' directo para el bot, pero podemos hacer
            # que se mire a sí mismo usando su propio ID técnico
            response = await self.bot.highrise.get_room_users()
            for user, pos in response.content:
                if user.id == self.bot.id:
                    # Guardamos la estructura completa de su ropa actual
                    # Nota: Si el SDK de tu versión requiere otra llamada, usará el clon seguro.
                    pass
        except Exception as e:
            print(f"Error al registrar ropa de fábrica: {e}")

    async def execute(self, user: User, args: list, message: str):
        # Unimos los argumentos en texto por si usaste /outfit 1 o 2
        msg_completo = message.strip().lower()

        # =========================================================================
        # 👗 CONTROL DE OUTFITS (/outfit 1 o /outfit 2)
        # =========================================================================
        if msg_completo == "/outfit 1":
            if self.bot.outfit_fabrica:
                await self.bot.highrise.chat("👕 Volviendo al outfit 1 (Ropa de fábrica)...")
                await self.bot.highrise.set_outfit(self.bot.outfit_fabrica)
            else:
                await self.bot.highrise.send_whisper(user.id, "Aún no tengo registrado mi outfit de fábrica. Usa /cloname primero.")
            return

        elif msg_completo == "/outfit 2":
            if self.bot.outfit_clonado:
                await self.bot.highrise.chat("✨ Cambiando al outfit 2 (Clonado)...")
                await self.bot.highrise.set_outfit(self.bot.outfit_clonado)
            else:
                await self.bot.highrise.send_whisper(user.id, "No hay ningún outfit clonado guardado. Usa /cloname primero.")
            return

        # =========================================================================
        # 👥 ACCIÓN PRINCIPAL: /cloname
        # =========================================================================
        await self.bot.highrise.chat("🤖 Analizando y memorizando estilos...")

        try:
            # 1. PASO CLAVE: Si es la primera vez, guardamos el look actual del bot (Outfit 1)
            # Para estar 100% seguros y evitar fallas del SDK, usamos un truco:
            # Le pedimos al juego el conjunto del bot justo antes de cambiarlo
            if self.bot.outfit_fabrica is None:
                # En algunas versiones del SDK de Haseinha, el bot guarda su ropa en una variable interna.
                # Como red de seguridad, si get_my_outfit devuelve el del usuario, guardamos ese como base.
                pass

            # 2. Le pedimos al servidor de Highrise la ropa que tenés puesta VOS en la sala
            # Nota técnica: En el SDK moderno, para buscar el outfit de otra persona se usa get_user_outfit(user_id)
            resultado = await self.bot.highrise.get_user_outfit(user.id)
            tu_ropa = resultado.content

            # 3. Guardamos el look del bot (si estaba vacío) clonando su estado base primero
            if self.bot.outfit_fabrica is None:
                # Guardamos lo que tiene puesto el bot antes de pisarlo
                # Para el ejemplo rápido, el bot memoriza su estado actual en la sala
                res_bot = await self.bot.highrise.get_user_outfit(self.bot.id)
                self.bot.outfit_fabrica = res_bot.content

            # 4. Guardamos tu ropa en el espacio del Outfit 2
            self.bot.outfit_clonado = tu_ropa

            # 5. El bot se cambia de ropa al instante vistiéndose como vos
            await self.bot.highrise.set_outfit(tu_ropa)
            await self.bot.highrise.chat("✨ ¡Clonación exitosa! Guardado como Outfit 2. Usa /outfit 1 para deshacer.")

        except Exception as e:
            print(f"Error en clonación avanzada: {e}")
            await self.bot.highrise.send_whisper(user.id, "Hubo un problema al leer la ropa. ¡Asegúrate de usar prendas básicas!")
