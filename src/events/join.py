import asyncio
from highrise.models import User
from config.config import loggers


async def on_join(bot, user: User, position) -> None:
    if loggers.joins:
        print(f"User {user.username} joined the room")

    if user.username == "beBot33":
        return

    # Esperamos 2 segundos para que el juego termine de cargar al usuario.
    await asyncio.sleep(2)

    # ============================================================
    # SISTEMA AUTOMÁTICO
    #
    # El comando automatico.py controla:
    # - saludos de entrada
    # - frases automáticas
    # - anuncios automáticos
    #
    # No hace falta editar nada aquí.
    # ============================================================
    automatico = bot.command_handler.commands.get("automatico")

    if automatico:
        # Inicia el ciclo de frases/anuncios si todavía no está activo.
        automatico.iniciar_tarea_mensajes()

        # Envía el saludo de bienvenida si está activado.
        if hasattr(automatico, "on_user_join"):
            await automatico.on_user_join(user)
