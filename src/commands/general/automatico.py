import random
import asyncio
from datetime import datetime

from highrise import User


class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "automatico"
        self.description = "Controla saludos, frases y anuncios automáticos"
        self.aliases = ["auto"]
        self.permissions = []
        self.cooldown = 3

        # ============================================================
        # EDITA AQUÍ EL INTERVALO DE FRASES Y ANUNCIOS
        # 180 = 3 minutos | 240 = 4 minutos | 300 = 5 minutos
        # ============================================================
        self.intervalo = 240

        # ============================================================
        # EDITA AQUÍ LOS SALUDOS DE BIENVENIDA
        # Usa {username} para colocar el nombre del usuario.
        # ============================================================
        self.saludos = [
            "👋 ¡Bienvenido/a a la sala, @{username}! Siéntete como en casa... pero no te lleves nada. 😂",
            "🎉 ¡Bienvenido/a, @{username}! Pasa, ponte cómodo/a y disfruta de la sala.",
            "😎 ¡@{username} acaba de llegar! Bienvenido/a. El bot confirma que puedes quedarte.",
            "🚪 ¡Bienvenido/a, @{username}! La puerta está abierta y el bot está vigilando... más o menos. 😂",
            "✨ ¡Hola @{username}! Bienvenido/a. Siéntete como en casa, pero recuerda que aquí todo tiene dueño.",
        ]

        # ============================================================
        # EDITA AQUÍ LAS FRASES DE LA MAÑANA
        # ============================================================
        self.frases_manana = [
            "☀️ Buenos días. El bot ya está despierto... técnicamente.",
            "☕ Buenos días. Si todavía no tomaste café, este es un buen momento.",
            "🌅 Buenos días, gente. Que hoy pase algo interesante.",
        ]

        # ============================================================
        # EDITA AQUÍ LAS FRASES DE LA TARDE
        # ============================================================
        self.frases_tarde = [
            "🌤️ Buenas tardes. La sala sigue en funcionamiento y el bot también.",
            "😎 Buenas tardes. Todo tranquilo... sospechosamente tranquilo.",
            "🎉 La tarde avanza. Aprovechen mientras el bot todavía tiene batería imaginaria.",
        ]

        # ============================================================
        # EDITA AQUÍ LAS FRASES DE LA NOCHE
        # ============================================================
        self.frases_noche = [
            "🌙 Buenas noches. La sala sigue abierta y el bot sigue vigilando.",
            "👀 La noche acaba de empezar. El bot recomienda no hacer nada sospechoso.",
            "🌃 Buenas noches, gente. Si escuchan algo raro... probablemente fue el bot.",
        ]

        # ============================================================
        # EDITA AQUÍ LOS ANUNCIOS AUTOMÁTICOS
        # ============================================================
        self.anuncios = [
            "📢 Recuerda respetar a los demás y disfrutar de la sala.",
            "📢 ¡Gracias por pasar por la sala! Espero que estés disfrutando.",
            "📢 Siéntete libre de usar /help para ver los comandos disponibles.",
            "📢 El bot está trabajando. Por favor, no alimentar al bot. 🤖",
            "📢 Anuncio importante: este anuncio fue anunciado oficialmente. 😂",
        ]

        self.saludos_activos = True
        self.mensajes_activos = True
        self.tarea_mensajes = None

    async def execute(self, user: User, args: list, message: str):
        opcion = args[0].lower() if args else ""

        if opcion == "silencio":
            self.mensajes_activos = False
            await self.bot.highrise.send_whisper(
                user.id,
                "🔇 Frases y anuncios automáticos desactivados. Los saludos no cambian."
            )
            return

        if opcion == "hablar":
            self.mensajes_activos = True
            self.iniciar_tarea_mensajes()
            await self.bot.highrise.send_whisper(
                user.id,
                "🔊 Frases y anuncios automáticos activados."
            )
            return

        if opcion == "saludos":
            if len(args) >= 2 and args[1].lower() in ["off", "apagar", "silencio"]:
                self.saludos_activos = False
                await self.bot.highrise.send_whisper(
                    user.id,
                    "👋 Saludos de entrada desactivados."
                )
                return

            if len(args) >= 2 and args[1].lower() in ["on", "activar", "hablar"]:
                self.saludos_activos = True
                await self.bot.highrise.send_whisper(
                    user.id,
                    "👋 Saludos de entrada activados."
                )
                return

            estado = "ACTIVADOS" if self.saludos_activos else "DESACTIVADOS"
            await self.bot.highrise.send_whisper(
                user.id,
                f"👋 Saludos de entrada: {estado}"
            )
            return

        estado_mensajes = "ACTIVOS" if self.mensajes_activos else "DESACTIVADOS"
        estado_saludos = "ACTIVADOS" if self.saludos_activos else "DESACTIVADOS"

        await self.bot.highrise.send_whisper(
            user.id,
            f"🤖 Automático\n"
            f"Frases y anuncios: {estado_mensajes}\n"
            f"Saludos de entrada: {estado_saludos}\n"
            f"Intervalo: {self.intervalo // 60} minutos"
        )

    def iniciar_tarea_mensajes(self):
        if self.tarea_mensajes is None or self.tarea_mensajes.done():
            self.tarea_mensajes = asyncio.create_task(self.ciclo_mensajes())

    async def ciclo_mensajes(self):
        while self.mensajes_activos:
            await asyncio.sleep(self.intervalo)

            if not self.mensajes_activos:
                break

            if random.choice([True, False]):
                mensaje = self.obtener_frase_horaria()
            else:
                mensaje = random.choice(self.anuncios)

            await self.bot.highrise.chat(mensaje)

    def obtener_frase_horaria(self):
        hora = datetime.now().hour

        if 6 <= hora < 12:
            return random.choice(self.frases_manana)
        if 12 <= hora < 19:
            return random.choice(self.frases_tarde)
        return random.choice(self.frases_noche)

    async def on_user_join(self, user: User):
        if not self.saludos_activos:
            return

        saludo = random.choice(self.saludos)
        saludo = saludo.replace("{username}", user.username)
        await self.bot.highrise.chat(saludo)
