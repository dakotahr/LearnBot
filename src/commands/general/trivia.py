import asyncio
import random
from highrise import User

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "trivia"
        self.description = "Lanza una pregunta de trivia. El dueño puede activar premio de oro usando '/trivia oro'."
        self.permissions = [] # Libre para que cualquiera inicie una gratis
        self.cooldown = 10     

        if not hasattr(bot, 'trivia_activa'):
            bot.trivia_activa = False
        if not hasattr(bot, 'respuesta_correcta'):
            bot.respuesta_correcta = ""
        # Nueva variable interna para saber si la pregunta actual paga oro
        if not hasattr(bot, 'trivia_paga_oro'):
            bot.trivia_paga_oro = False

        self.banco_preguntas = [
            {"p": "¿Cuál es el planeta más cercano al Sol?", "o": "A) Marte | B) Mercurio | C) Venus", "r": "b"},
            {"p": "¿Cuántos minutos tiene una hora?", "o": "A) 50 | B) 100 | C) 60", "r": "c"},
            {"p": "¿Qué gas necesitamos respirar para vivir?", "o": "A) Oxígeno | B) Hidrógeno | C) Nitrógeno", "r": "a"},
            {"p": "¿Cuál es el océano más grande del mundo?", "o": "A) Atlántico | B) Pacífico | C) Índico", "r": "b"},
            {"p": "¿Qué país tiene forma de bota?", "o": "A) España | B) Italia | C) Francia", "r": "b"},
            {"p": "¿Cuántos días tiene un año bisiesto?", "o": "A) 365 | B) 364 | C) 366", "r": "c"}
        ]

    async def reloj_trivia(self, juego_id):
        """Reloj invisible de 30 segundos"""
        await asyncio.sleep(30)
        if self.bot.trivia_activa and self.bot.respuesta_correcta == juego_id:
            self.bot.trivia_activa = False
            self.bot.trivia_paga_oro = False  # Apagamos el premio de oro si vence el tiempo
            r_mayuscula = self.bot.respuesta_correcta.upper()
            await self.bot.highrise.chat(f"⏱️ ¡Tiempo agotado! Nadie respondió a tiempo. La respuesta correcta era la ({r_mayuscula}).")

    async def execute(self, user: User, args: list, message: str):
        if self.bot.trivia_activa:
            await self.bot.highrise.send_whisper(user.id, "⚠️ Ya hay una trivia en curso. ¡Espera a que termine!")
            return

        # Revisamos si pasaron el argumento 'oro'
        argumento = " ".join(args).strip().lower()
        
        # FILTRO DE SEGURIDAD: Solo vos (IamDakota) podés activar el modo oro
        if argumento == "oro" and user.username.lower() == "iamdakota":
            # Verificamos si el bot tiene oro en la billetera antes de prometerlo
            try:
                billetera = await self.bot.highrise.get_wallet()
                oro_disponible = 0
                for item in billetera.content:
                    if item.type == 'gold':
                        oro_disponible = item.amount
                        break
                
                if oro_disponible >= 1:
                    self.bot.trivia_paga_oro = True
                    await self.bot.highrise.chat("💰 ¡ATENCIÓN COLA DE LA SALA! Esta trivia tiene premio especial de 1 ORO para el ganador. 💰")
                else:
                    await self.bot.highrise.send_whisper(user.id, "⚠️ No pude activar el modo oro porque la alcancía del bot está vacía.")
                    self.bot.trivia_paga_oro = False
            except Exception as e:
                print(f"Error al verificar billetera en trivia: {e}")
                self.bot.trivia_paga_oro = False
        else:
            self.bot.trivia_paga_oro = False

        # Lanzamos el juego normal
        juego = random.choice(self.banco_preguntas)
        self.bot.trivia_activa = True
        self.bot.respuesta_correcta = juego["r"]

        await self.bot.highrise.chat(f"🧠 ¡TRIVIA TIME! 🧠\nPregunta: {juego['p']}\n👉 Opciones:\n{juego['o']}\n\n⏱️ ¡Tienen 30 segundos!")
        asyncio.create_task(self.reloj_trivia(juego["r"]))
