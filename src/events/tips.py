import random
from highrise.models import User, CurrencyItem, Item
from config.config import loggers

async def on_tip(bot, sender: User, receiver: User, tip: CurrencyItem | Item) -> None:
    # 1. Registro de consola original por si está activo
    if loggers.tips:
        print(f"User {sender.username} tipped {receiver.username}")

    # 🔮 LÓGICA DE LA ALCANCÍA:
    # Solo reaccionamos si el oro se lo están dando al BOT (beBot33)
    if receiver.username == "beBot33":
        
        # Verificamos que sea una propina de oro (Gold)
        if isinstance(tip, CurrencyItem):
            monto_oro = tip.amount  # Guardamos la cantidad de oro recibida

            # 🎭 Mensajes divertidos para el contestador automático público
            frases_agradecimiento = [
                f"🐷 ¡Monedita a la alcancía! Gracias @{sender.username} por los {monto_oro} de oro. 🎉",
                f"🥳 ¡Rompemos los ahorros! Muchas gracias @{sender.username} por aportar {monto_oro} de oro. ✨",
                f"💰 ¡BotiNero se está volviendo rico! Gracias @{sender.username} por esos {monto_oro} golds."
            ]

            # El bot elige un mensaje al azar para responder en el chat general
            mensaje_chat = random.choice(frases_agradecimiento)
            await bot.highrise.chat(mensaje_chat)

            # 🚀 CONTESTADOR INTELIGENTE POR MONTOS ALTOS:
            # Si te dan una propina generosa (por ejemplo, 10 de oro o más)
            if monto_oro >= 10:
                # El bot grita un mensaje especial de agradecimiento gigante
                await bot.highrise.chat(f"💎 ¡WOW! 🎉 @{sender.username} se pasó con una super propina de {monto_oro} de oro. ¡Qué elegancia la de Francia! 🇫🇷✨")
                
                # ¡El bot tira un baile al azar de celebración en el acto!
                bailes_festejo = ["dance-tiktok8", "emote-celebrate", "dance-shoppingcart", "dance-russian"]
                baile_elegido = random.choice(bailes_festejo)
                try:
                    await bot.highrise.send_emote(baile_elegido)
                except Exception as e:
                    print(f"Error al bailar festejo: {e}")
