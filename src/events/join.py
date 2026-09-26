import random
import asyncio  # IMPORTANTE: Traemos la librería de tiempo
from highrise.models import User
from config.config import loggers

async def on_join(bot, user: User, position) -> None:
    if loggers.joins:
        print(f"User {user.username} joined the room")

    if user.username == "beBot33":
        return

    # ⏱️ ¡EL SALVAVIDAS!: Hacemos que el bot espere 2 segundos quietito
    # Esto le da tiempo al juego de cargar al usuario y evita que el bot se caiga
    await asyncio.sleep(2)

    # 📝 BANCO DE SALUDOS
    saludos_base = [
        f"¡Hola {user.username}! Bienvenido/a a la sala. Pásala genial. ❤️",
        f"✨ ¡Qué alegría verte por acá {user.username}! Ponete cómodo/a. ✨",
        f"👋 ¡Buenas buenas {user.username}! Bienvenido/a a nuestro rincón."
    ]

    # 🎭 BANCO DE CHISTES
    remates_divertidos = [
        "¡Qué elegancia la de Francia! 🇫🇷",
        "Me encantan tus vibras hoy. 😎",
        "¡Trajiste toda la onda a la sala! ⚡",
        "Cuidado con los pasos de baile, están picantes. 🔥"
    ]

    saludo_final = random.choice(saludos_base)

    if random.random() < 0.5:
        saludo_final += f" {random.choice(remates_divertidos)}"

    # Envío del susurro seguro después de la espera
    try:
        await bot.highrise.send_whisper(user.id, saludo_final)
    except Exception as e:
        print(f"Error al enviar bienvenida a {user.username}: {e}")
