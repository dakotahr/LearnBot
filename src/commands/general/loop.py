import json
import asyncio
from highrise import User
from config.config import config

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "loop"
        self.description = "Baila un emote en bucle infinito. Usa '/loop stop' para parar."
        self.permissions = []
        self.cooldown = 1
        
        # Diccionario interno para saber quién está bailando y qué está bailando
        if not hasattr(bot, 'usuarios_en_bucle'):
            bot.usuarios_en_bucle = {}

    async def bucle_baile_usuario(self, user_id, emote_id):
        """Tarea en segundo plano que repite el baile cada 9 segundos"""
        try:
            # Mientras el usuario siga anotado con este mismo emote, se repite
            while user_id in self.bot.usuarios_en_bucle and self.bot.usuarios_en_bucle[user_id] == emote_id:
                await self.bot.highrise.send_emote(emote_id, user_id)
                # Espera 9 segundos antes de volver a tirar el emote (duración estándar de un baile)
                await asyncio.sleep(9) 
        except Exception as e:
            print(f"Error en el bucle de {user_id}: {e}")

    async def execute(self, user: User, args: list, message: str):
        # 1. Comando especial para DETENER el bucle
        if len(args) > 0 and args[0].lower() == 'stop':
            if user.id in self.bot.usuarios_en_bucle:
                del self.bot.usuarios_en_bucle[user.id] # Lo sacamos de la lista
                await self.bot.highrise.send_whisper(user.id, "🛑 Bucle de baile detenido.")
            else:
                await self.bot.highrise.send_whisper(user.id, "No estabas ejecutando ningún bucle de baile.")
            return

        # 2. Validación de argumentos
        if len(args) == 0:
            await self.bot.highrise.send_whisper(user.id, "Uso: /loop [nombre o número] o /loop stop")
            return

        # 3. Cargamos los 55 emotes del JSON
        emotes_file = 'config/json/emotes.json'
        try:
            with open(emotes_file) as f:
                emotes = json.load(f)
        except Exception as e:
            print(f"Error JSON: {e}")
            return

        # Unimos los argumentos por si escribieron un nombre con espacios
        busqueda = " ".join(args).strip().lower()
        emote_seleccionado = None

        # 4. Buscador por Número o por Nombre
        if busqueda.isdigit():
            numero = int(busqueda) - 1
            if 0 <= numero < len(emotes):
                emote_seleccionado = emotes[numero]
            else:
                await self.bot.highrise.send_whisper(user.id, f"Elige un número entre 1 y {len(emotes)}.")
                return
        else:
            for emote in emotes:
                if busqueda in emote.lower():
                    emote_seleccionado = emote
                    break

        # 5. Activación del Bucle Infinito
        if emote_seleccionado:
            # Anotamos al usuario en el diccionario del bot
            self.bot.usuarios_en_bucle[user.id] = emote_seleccionado
            await self.bot.highrise.send_whisper(user.id, f"🕺 Bucle iniciado. Usa '/loop stop' para detenerlo.")
            
            # Lanzamos la tarea repetitiva en segundo plano (asíncrona)
            asyncio.create_task(self.bucle_baile_usuario(user.id, emote_seleccionado))
        else:
            await self.bot.highrise.send_whisper(user.id, f"No encontré el emote '{busqueda}'.")
