import json
import asyncio
from highrise import User

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "me"  # El comando será /me
        self.description = "Baila 100 emotes en bucle por número o aproximación. Usa '/me stop' para parar."
        self.permissions = [] # Libre para toda la sala
        self.cooldown = 1

        # Diccionario en la RAM del bot para controlar quién está en bucle
        if not hasattr(bot, 'usuarios_me_bucle'):
            bot.usuarios_me_bucle = {}

        # 🕺 CATÁLOGO INDEXADO DE 100 EMOTES DEL SERVIDOR
        self.lista_completa = [
            "dance-macarena", "dance-tiktok8", "dance-blackpink", "dance-tiktok2", "dance-pennywise",
            "dance-russian", "dance-shoppingcart", "dance-tiktok9", "dance-weird", "dance-tiktok10",
            "idle-dance-casual", "emote-kiss", "emote-no", "emote-sad", "emote-yes",
            "emote-laughing", "emote-hello", "emote-wave", "emote-shy", "emote-tired",
            "emoji-angry", "idle-loop-sitfloor", "emoji-thumbsup", "emote-lust", "emoji-cursing",
            "emote-greedy", "emoji-flex", "emoji-gagging", "emoji-celebrate", "emote-model",
            "emote-bow", "emote-curtsy", "emote-snowball", "emote-hot", "emote-snowangel",
            "emote-charging", "emote-confused", "idle-enthusiastic", "emote-telekinesis", "emote-float",
            "emote-teleporting", "emote-swordfight", "emote-maniac", "emote-energyball", "emote-snake",
            "idle-singing", "emote-frog", "emote-superpose", "emote-cute", "emote-pose7",
            "emote-pose8", "emote-pose1", "emote-pose3", "emote-pose5", "emote-cutey",
            "dance-voguehands", "dance-breakdance", "dance-orangejam", "dance-shuffle", "dance-lazy",
            "emote-headout", "emote-peekaboo", "emote-falling", "emote-splits", "emote-handstand",
            "emote-zombie", "emote-monster", "emote-vampire", "emote-ghost", "emote-werewolf",
            "dance-reggaeton", "dance-salsa", "dance-bachata", "dance-hiphop", "dance-pop",
            "emote-heartfingers", "emote-wink", "emote-blowkiss", "emote-flyingkiss", "emote-airkiss",
            "emoji-scared", "emoji-crying", "emoji-laughing", "emoji-sleeping", "emoji-shocked",
            "idle-guitar", "idle-violin", "idle-piano", "idle-drums", "idle-dance",
            "dance-tiktok1", "dance-tiktok3", "dance-tiktok4", "dance-tiktok5", "dance-tiktok6",
            "dance-tiktok7", "dance-anime", "dance-kpop", "dance-jpop", "dance-disco"
        ]

    async def reloj_bucle_me(self, user_id, emote_id):
        """Reloj en segundo plano que repite el baile cada 9 segundos"""
        try:
            while user_id in self.bot.usuarios_me_bucle and self.bot.usuarios_me_bucle[user_id] == emote_id:
                await self.bot.highrise.send_emote(emote_id, user_id)
                await asyncio.sleep(9) # Duración estándar de la animación
        except Exception as e:
            print(f"Error en bucle /me para {user_id}: {e}")

    async def execute(self, user: User, args: list, message: str):
        # 1. Comando especial para DETENER el bucle
        if len(args) > 0 and args[0].lower() == 'stop':
            if user.id in self.bot.usuarios_me_bucle:
                del self.bot.usuarios_me_bucle[user.id]
                await self.bot.highrise.send_whisper(user.id, "🛑 Tu bucle de baile se ha detenido.")
            else:
                await self.bot.highrise.send_whisper(user.id, "No tenías ningún bucle activo.")
            return

        # 2. Validación de argumentos vacíos
        if len(args) == 0:
            await self.bot.highrise.send_whisper(
                user.id, 
                f"Uso: /me [número 1 al {len(self.lista_completa)}] o /me [palabra] o /me stop"
            )
            return

        busqueda = " ".join(args).strip().lower()
        emote_encontrado = None

        # 3. Buscador por número
        if busqueda.isdigit():
            numero = int(busqueda) - 1
            if 0 <= numero < len(self.lista_completa):
                emote_encontrado = self.lista_completa[numero]
            else:
                await self.bot.highrise.send_whisper(user.id, f"Elige un número entre 1 y {len(self.lista_completa)}.")
                return
        # 4. Buscador por palabra aproximada
        else:
            for emote in self.lista_completa:
                if busqueda in emote.lower():
                    emote_encontrado = emote
                    break

        # 5. Activación del Bucle en Segundo Plano
        if emote_encontrado:
            # Guardamos al usuario y el baile elegido en la RAM del bot
            self.bot.usuarios_me_bucle[user.id] = emote_encontrado
            await self.bot.highrise.send_whisper(user.id, f"🕺 Bucle iniciado por defecto. Usa '/me stop' para frenar.")
            
            # Lanzamos la tarea repetitiva
            asyncio.create_task(self.reloj_bucle_me(user.id, emote_encontrado))
        else:
            await self.bot.highrise.send_whisper(user.id, f"🔍 No encontré ningún emote con '{busqueda}'.")
