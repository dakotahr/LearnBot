from highrise.models import User
from config.config import loggers, config


async def on_chat(bot, user: User, message: str) -> None:
    # 1. Registro de consola original
    if loggers.messages:
        print(f"{user.username}: {message}")

    # 🔮 INTERCEPTOR DE TRIVIA:
    # Limpiamos el mensaje de espacios y lo pasamos a minúsculas
    msg_limpio = message.strip().lower()

    # Si hay una trivia corriendo en la sala y el usuario escribió "a", "b" o "c"...
    if hasattr(bot, 'trivia_activa') and bot.trivia_activa and msg_limpio in ['a', 'b', 'c']:
        # Comparamos si la letra coincide exactamente con la respuesta ganadora
        if msg_limpio == bot.respuesta_correcta:
            bot.trivia_activa = False  # Apagamos la trivia inmediatamente para que nadie más gane
            bot.respuesta_correcta = "" # Limpiamos la respuesta de la memoria
            
            # El bot grita el ganador en la sala celebrando
            await bot.highrise.chat(f"🎉 ¡Felicidades @{user.username}! Respondiste correctamente y ganaste la trivia. 🧠✨")
            return # Frenamos el código acá para que no intente procesar la letra como un comando

    # 2. Procesador de comandos original con prefijo (ejemplo: /loop)
    if message.lstrip().startswith(config.prefix):
        await bot.command_handler.handle_command(user, message)
