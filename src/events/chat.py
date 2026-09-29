from highrise.models import User
from config.config import loggers, config

async def on_chat(bot, user: User, message: str) -> None:
    if loggers.messages:
        print(f"{user.username}: {message}")

    msg_limpio = message.strip().lower()

    # Si hay una trivia corriendo y escriben la letra justa...
    if hasattr(bot, 'trivia_activa') and bot.trivia_activa and msg_limpio in ['a', 'b', 'c']:
        if msg_limpio == bot.respuesta_correcta:
            # Guardamos los estados antes de apagarlos
            paga_oro = bot.trivia_paga_oro
            
            bot.trivia_activa = False  
            bot.respuesta_correcta = "" 
            bot.trivia_paga_oro = False 
            
            # Anuncio de victoria básico
            await bot.highrise.chat(f"🎉 ¡Felicidades @{user.username}! Respondiste correctamente. 🧠✨")
            
            # 🕺 ¡BAILE DE FESTEJO OBLIGATORIO!: Forzamos al ganador a celebrar
            try:
                # Elegimos una animación divertida de festejo o saludo
                festejos = ["emote-celebrate", "emote-wave"]
                await bot.highrise.send_emote(festejos[0], user.id)
            except Exception as e:
                print(f"No se pudo hacer bailar al ganador: {e}")

            # 💰 ¡PREMIO DE CAJERO AUTOMÁTICO!: Si el dueño activó el modo oro, el bot le paga en el acto
            if paga_oro:
                try:
                    await bot.highrise.chat(f"🎁 Guardando 1 de oro de la alcancía en el bolsillo de @{user.username}...")
                    await bot.highrise.tip_user(user.id, 1)
                except Exception as e:
                    print(f"Error al pagar premio de trivia: {e}")
            
            return 
            
    if message.lstrip().startswith(config.prefix):
        await bot.command_handler.handle_command(user, message)
