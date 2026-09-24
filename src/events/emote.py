from highrise.models import User
from config.config import loggers

async def on_emote(bot, user: User, emote_id: str, receiver: User) -> None:
    # Mantenemos el log original de Haseinha por si lo activás en el config
    if loggers.emotes:
        receiver_name = receiver.username if receiver else "None"
        print(f"User {user.username} sent {emote_id} to {receiver_name}")

    # 🔮 LA MAGIA DE LA IMITACIÓN:
    # Verificamos si hay un usuario seleccionado y si ese usuario es el que acaba de bailar
    if hasattr(bot, 'usuario_a_imitar') and bot.usuario_a_imitar == user.id:
        try:
            # beBot33 ejecuta exactamente el mismo ID de emote que usó el objetivo
            await bot.highrise.send_emote(emote_id)
        except Exception as e:
            print(f"Error al imitar emote: {e}")
