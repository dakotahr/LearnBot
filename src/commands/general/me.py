import random
from highrise import User

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "me"  # El comando será /me [número o palabra]
        self.description = "Buscador inteligente e indexado de más de 100 emotes del juego por número o aproximación."
        self.permissions = [] # Libre para todos los visitantes de tu sala
        self.cooldown = 2

        # 🕺 CATÁLOGO INDEXADO DE 100 EMOTES POPULARES DEL SERVIDOR
        # El bot los reconocerá por su número de orden (del 1 al 100) o por palabras cortas
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

    async def execute(self, user: User, args: list, message: str):
        # 1. Si no escriben nada, el bot les da una pista e instrucciones
        if len(args) == 0:
            await self.bot.highrise.send_whisper(
                user.id, 
                f"💡 Uso de /me:\n🔢 Por número: /me 1 al {len(self.lista_completa)}\n🔤 Por aproximación: /me maca o /me tik"
            )
            return

        # Unimos lo que escribió el usuario (ejemplo: 'maca' o '19')
        busqueda = " ".join(args).strip().lower()
        emote_encontrado = None

        # 2. LÓGICA POR NÚMERO DIRECTO (Del 1 al 100)
        if busqueda.isdigit():
            numero = int(busqueda) - 1  # Restamos 1 porque en programación se cuenta desde 0
            if 0 <= numero < len(self.lista_completa):
                emote_encontrado = self.lista_completa[numero]
            else:
                await self.bot.highrise.send_whisper(user.id, f"⚠️ Elige un número válido entre 1 y {len(self.lista_completa)}.")
                return

        # 3. LÓGICA POR APROXIMACIÓN DE PALABRA
        else:
            # El bot busca de forma predictiva si la palabra corta está metida adentro de algún emote
            for emote in self.lista_completa:
                if busqueda in emote.lower():
                    emote_encontrado = emote
                    break  # Frena al encontrar la primera coincidencia válida

        # 4. ENVIAR LA ORDEN DE BAILE AL SERVIDOR
        if emote_encontrado:
            try:
                # Hace bailar al usuario que ejecutó el comando /me
                await self.bot.highrise.send_emote(emote_encontrado, user.id)
            except Exception as e:
                print(f"Error en /me con {emote_encontrado}: {e}")
                await self.bot.highrise.send_whisper(user.id, "❌ No se pudo ejecutar el baile. ¿Lo tienes en tu inventario?")
        else:
            await self.bot.highrise.send_whisper(user.id, f"🔍 No encontré ningún emote que coincida con '{busqueda}'. ¡Prueba con otra palabra!")
