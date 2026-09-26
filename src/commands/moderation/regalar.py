from highrise import User
from config.config import permissions

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "regalar"
        self.description = "Ordena al bot transferir oro de su billetera a un usuario. Uso: /regalar @usuario [monto]"
        # Exigimos permiso de moderación/dueño para que los visitantes no puedan usarlo
        self.permissions = ["moderation"]
        self.cooldown = 3

    async def execute(self, user: User, args: list, message: str):
        # 1. Validación de argumentos (Necesitamos el @usuario y el monto)
        if len(args) < 2:
            await self.bot.highrise.send_whisper(user.id, "⚠️ Uso correcto: /regalar @usuario [monto]\nEjemplo: /regalar @IamDakota 5")
            return

        target_username = args[0]
        monto_texto = args[1]

        # Limpiamos el arroba si lo pusieron en el nombre
        if target_username.startswith('@'):
            target_username = target_username[1:]

        # 2. Validamos que el monto sea un número entero válido y positivo
        if not monto_texto.isdigit():
            await self.bot.highrise.send_whisper(user.id, "⚠️ El monto debe ser un número entero de oro.")
            return
            
        monto = int(monto_texto)
        if monto <= 0:
            await self.bot.highrise.send_whisper(user.id, "⚠️ El monto a regalar debe ser mayor a 0.")
            return

        # 3. Buscamos si el usuario objetivo está en la sala para poder extraer su ID técnico
        try:
            response = await self.bot.highrise.get_room_users()
            users_in_room = [content for content in response.content]
            
            target_user = next((u for u in users_in_room if u.username.lower() == target_username.lower()), None)
            
            if not target_user:
                await self.bot.highrise.send_whisper(user.id, f"❌ El usuario '@{target_username}' no está en la sala.")
                return

            # 4. Verificamos la billetera del bot antes de transferir para que no se rompa por falta de fondos
            billetera = await self.bot.highrise.get_wallet()
            oro_disponible = 0
            
            # Buscamos cuánto oro real (Gold) tiene el bot acumulado
            for item in billetera.content:
                if item.type == 'gold':
                    oro_disponible = item.amount
                    break

            if oro_disponible < monto:
                await self.bot.highrise.send_whisper(user.id, f"⚠️ Fondos insuficientes. La alcancía del bot solo tiene {oro_disponible} de oro.")
                return

            # 5. ¡LA TRANSFERENCIA!: El bot le envía el oro de su billetera al usuario
            await self.bot.highrise.chat(f"💰 ¡@{user.username} ha ordenado un regalo! 🤖 beBot33 abriendo alcancía...")
            
            # Función nativa del SDK para enviar propinas desde el bot
            await self.bot.highrise.tip_user(target_user.id, monto)
            
            await self.bot.highrise.chat(f"🎉 ¡Transferencia exitosa! Le envié {monto} de oro a @{target_user.username}. ✨")

        except Exception as e:
            print(f"Error en comando regalar: {e}")
            await self.bot.highrise.send_whisper(user.id, "❌ Ocurrió un error técnico al intentar enviar el oro.")
