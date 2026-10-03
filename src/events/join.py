import asyncio
from highrise.models import User
from config.config import loggers


async def on_join(bot, user: User) -> None:
    if loggers.joins:
        print(f"User {user.username} joined the room")

    if user.username == "beBot33":
        return

    # Esperamos 2 segundos para que el usuario termine de cargar.
    await asyncio.sleep(2)

    # ============================================================
    # SISTEMA AUTOMÁTICO
    #
    # automatico.py controla:
    # - saludos de entrada
    # - frases automáticas
    # - anuncios automáticos
    #
    # No necesitas editar nada aquí.
    # ============================================================
    automatico = bot.command_handler.commands.get("automatico")

    if automatico:
        # Inicia el ciclo de frases y anuncios.
        automatico.iniciar_tarea_mensajes()

        # Envía el saludo de bienvenida si está activado.
        if hasattr(automatico, "on_user_join"):
            await automatico.on_user_join(user)
