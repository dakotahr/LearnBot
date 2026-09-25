import asyncio
import random
from highrise import User

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = "trivia"
        self.description = "Lanza una pregunta de trivia por tiempo en la sala. Responde con A, B o C."
        self.permissions = [] # Libre para que cualquier visitante la pueda iniciar
        self.cooldown = 10     # Evita que tiren trivias seguidas todo el tiempo

        # Creamos las variables en la memoria del bot si no existen
        if not hasattr(bot, 'trivia_activa'):
            bot.trivia_activa = False
        if not hasattr(bot, 'respuesta_correcta'):
            bot.respuesta_correcta = ""

        # Nuestro banco de preguntas interno para el juego
        self.banco_preguntas = [
            {"p": "¿Cuál es el planeta más cercano al Sol?", "o": "A) Marte | B) Mercurio | C) Venus", "r": "b"},
            {"p": "¿Cuántos minutos tiene una hora?", "o": "A) 50 | B) 100 | C) 60", "r": "c"},
            {"p": "¿Qué gas necesitamos respirar para vivir?", "o": "A) Oxígeno | B) Hidrógeno | C) Nitrógeno", "r": "a"},
            {"p": "¿Cuál es el océano más grande del mundo?", "o": "A) Atlántico | B) Pacífico | C) Índico", "r": "b"},
            {"p": "¿Qué país tiene forma de bota?", "o": "A) España | B) Italia | C) Francia", "r": "b"},
            {"p": "¿Cuántos días tiene un año bisiesto?", "o": "A) 365 | B) 364 | C) 366", "r": "c"}
        ]

    async def reloj_trivia(self, juego_id):
        """Reloj invisible que espera 30 segundos en segundo plano"""
        await asyncio.sleep(30)
        # Si pasaron los 30 segundos y la trivia sigue activa con esta misma pregunta...
        if self.bot.trivia_activa and self.bot.respuesta_correcta == juego_id:
            self.bot.trivia_activa = False
            r_mayuscula = self.bot.respuesta_correcta.upper()
            await self.bot.highrise.chat(f"⏱️ ¡Tiempo agotado! Nadie respondió correctamente a tiempo. La respuesta era la ({r_mayuscula}).")

    async def execute(self, user: User, args: list, message: str):
        # Si ya hay un juego corriendo, avisamos y frenamos
        if self.bot.trivia_activa:
            await self.bot.highrise.send_whisper(user.id, "⚠️ Ya hay una trivia en curso. ¡Espera a que termine o responde A, B o C!")
            return

        # Elegimos una pregunta al azar del banco
        juego = random.choice(self.banco_preguntas)
        
        # Guardamos el estado en la memoria global del bot
        self.bot.trivia_activa = True
        self.bot.respuesta_correcta = juego["r"] # Guarda la letra 'a', 'b' o 'c'

        # Lanzamos el anuncio en la sala
        await self.bot.highrise.chat(f"🧠 ¡TRIVIA TIME! 🧠\nPregunta: {juego['p']}\n👉 Opciones:\n{juego['o']}\n\n⏱️ ¡Tienen 30 segundos para responder con la letra en el chat!")

        # Activamos el reloj en segundo plano
        asyncio.create_task(self.reloj_trivia(juego["r"]))
