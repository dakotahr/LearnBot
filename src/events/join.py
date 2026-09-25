import random
from highrise.models import User
from config.config import loggers

async def on_join(bot, user: User, position) -> None:
    # 1. Registro de consola original por si lo activás en config
    if loggers.joins:
        print(f"User {user.username} joined the room")

    # Evitamos saludar al propio bot si es él quien entra o se reconecta
    if user.username == "beBot33":
        return

    # 📝 BANCO DE SALUDOS: El bot elegirá uno de estos tres al azar para empezar
    saludos_base = [
        f"¡Hola {user.username}! Bienvenido/a a la sala. Pásala genial. ❤️",
        f"✨ ¡Qué alegría verte por acá {user.username}! Ponete cómodo/a. ✨",
        f"👋 ¡Buenas buenas {user.username}! Bienvenido/a a nuestro rincón."
    ]

    # 🎭 BANCO DE CHISTES: Frases divertidas que se pueden sumar al final
    remates_divertidos = [
        "¡Qué elegancia la de Francia! 🇫🇷",
        "Me encantan tus vibras hoy. 😎",
        "¡Trajiste toda la onda a la sala! ⚡",
        "Cuidado con los pasos de baile, están picantes. 🔥"
    ]

    # El bot elige un saludo base al azar
    saludo_final = random.choice(saludos_base)

    # El bot tiene un 50% de probabilidad de sumarle un comentario divertido al final
    if random.random() < 0.5:
        saludo_final += f" {random.choice(remates_divertidos)}"

    # 🔮 ENVÍO DEL SUSURRO:
    # Se lo enviamos como susurro privado directo al ID del jugador que entró
    try:
        await bot.highrise.send_whisper(user.id, saludo_final)
    except Exception as e:
        print(f"Error al enviar bienvenida a {user.username}: {e}")
