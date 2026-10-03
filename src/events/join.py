import random
import asyncio
from highrise.models import User
from config.config import loggers


async def on_join(bot, user: User, position) -> None:
    if loggers.joins:
        print(f"User {user.username} joined the room")

    if user.username == "beBot33":
        return

    # Esperamos 2 segundos para que el usuario termine de cargar.
    await asyncio.sleep(2)

    # SALUDOS DE BIENVENIDA
    saludos_base = [
        f"¡Hola {user.username}! Bienvenido/a a la sala. ❤️",
        f"✨ ¡Qué alegría verte por acá {user.username}! Ponete cómodo/a. ✨",
        f"👋 ¡Buenas buenas {user.username}! Bienvenido/a a nuestro rincón."
    ]

    remates_divertidos = [
        "¡Qué elegancia la de Francia! 🇫🇷",
        "Me encantan tus vibras hoy. 😎",
        "¡Trajiste toda la onda a la sala! ⚡",
        "Cuidado con los pasos de baile, están picantes. 🔥"
    ]

    saludo_final = random.choice(saludos_base)

    if random.random() < 0.5:
        saludo_final += f" {random.choice(remates_divertidos)}"

    # Si automatico.py está cargado, sus saludos pueden apagarse
    # independientemente de las frases y anuncios.
    automatico = bot.command_handler.commands.get("automatico")

    if automatico is not None:
        if not getattr(automatico, "saludos_activos", True):
            return

    try:
        await bot.highrise.send_whisper(user.id, saludo_final)
    except Exception as e:
        print(f"Error al enviar bienvenida a {user.username}: {e}")
