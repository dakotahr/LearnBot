from highrise.models import User
from config.config import loggers, config

async def on_chat(bot, user: User, message: str) -> None:
    if loggers.messages:
        print(f"{user.username}: {message}")

    msg_limpio = message.strip().lower()

    # =========================================================================
    # 📬 PARCHE CARTERO MSN: Entregar recados guardados en privado
    # =========================================================================
    if hasattr(bot, 'mensajes_msn') and user.id in bot.mensajes_msn:
        recados = bot.mensajes_msn[user.id]
        if recados: # Si hay cartas pendientes...
            for nota in recados:
                try:
                    # El bot le susurra en secreto los mensajes guardados
                    await bot.highrise.send_whisper(
                        user.id, 
                        f"✉️ [MSN Messenger] Tenés un mensaje dejado por @{nota['remitente']}: \"{nota['texto']}\""
                    )
                except Exception as e:
                    print(f"Error al entregar susurro de cartero: {e}")
            
            # ¡Muy importante!: Borramos el buzón de este usuario para que no le repita los mensajes
            del bot.mensajes_msn[user.id]

    # =========================================================================
    # 🧠 INTERCEPTOR DE TRIVIA
    # =========================================================================
    if hasattr(bot, 'trivia_activa') and bot.trivia_activa and msg_limpio in ['a', 'b', 'c']:
        if msg_limpio == bot.respuesta_correcta:
            paga_oro = bot.trivia_paga_oro
            
            bot.trivia_activa = False  
            bot.respuesta_correcta = "" 
            bot.trivia_paga_oro = False 
            
            await bot.highrise.chat(f"🎉 ¡Felicidades @{user.username}! Respondiste correctamente. 🧠✨")
            
            try:
                festejos = ["emote-celebrate", "emote-wave"]
                import random
                await bot.highrise.send_emote(random.choice(festejos), user.id)
            except Exception as e:
                print(f"No se pudo hacer bailar al ganador: {e}")

            if paga_oro:
                try:
                    await bot.highrise.chat(f"🎁 Guardando 1 de oro de la alcancía en el bolsillo de @{user.username}...")
                    await bot.highrise.tip_user(user.id, 1)
                except Exception as e:
                    print(f"Error al pagar premio de trivia: {e}")
            
            return 
            
    # =========================================================================
    # ⚙️ PROCESADOR DE COMANDOS ORIGINAL
    # =========================================================================
    if message.lstrip().startswith(config.prefix):
        await bot.command_handler.handle_command(user, message)
