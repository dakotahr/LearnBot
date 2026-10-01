from highrise import User
from config.config import permissions
from src.handlers.handleCommands import get_user_permissions


class Command:
    def __init__(self, bot):
        self.bot = bot
        self.name = 'help'
        self.description = "Muestra los comandos disponibles según tus permisos"
        self.aliases = ['info', 'hmm']

        # Help debe estar disponible para todos.
        self.permissions = []

        self.cooldown = 5

    async def execute(self, user: User, args: list, message: str):
        # ============================================================
        # DETERMINAR EL NIVEL DE ACCESO DEL USUARIO
        # ============================================================
        user_permissions = get_user_permissions(user)

        if user.id in permissions.owners:
            nivel = "👑 Propietario"
            puede_ver_todo = True
        elif user.id in permissions.moderators:
            nivel = "🛡️ Administrador"
            puede_ver_todo = True
        elif user_permissions:
            nivel = "⭐ Usuario con permisos"
            puede_ver_todo = False
        else:
            nivel = "👤 Visitante"
            puede_ver_todo = False

        # ============================================================
        # SI SE ESCRIBE /help comando, MOSTRAR INFORMACION ESPECIFICA
        # ============================================================
        if args:
            nombre = args[0].lower()
            comando = self.bot.command_handler.commands.get(nombre)

            if not comando:
                await self.bot.highrise.send_whisper(
                    user.id,
                    f"❌ No encontré el comando /{nombre}."
                )
                return

            permisos_requeridos = getattr(comando, "permissions", [])

            if puede_ver_todo or all(p in user_permissions for p in permisos_requeridos):
                descripcion = getattr(
                    comando,
                    "description",
                    "Sin descripción disponible."
                )

                aliases = getattr(comando, "aliases", [])
                texto_aliases = ""

                if aliases:
                    texto_aliases = f" | Alias: {', '.join('/' + a for a in aliases)}"

                if permisos_requeridos:
                    texto_permiso = (
                        f" | Permiso: {', '.join(permisos_requeridos)}"
                    )
                else:
                    texto_permiso = " | Público"

                await self.bot.highrise.send_whisper(
                    user.id,
                    f"📖 /{comando.name}: {descripcion}"
                    f"{texto_aliases}{texto_permiso}"
                )
            else:
                await self.bot.highrise.send_whisper(
                    user.id,
                    f"🔒 No tienes permiso para ver la información de /{nombre}."
                )

            return

        # ============================================================
        # CONSTRUIR LISTA DE COMANDOS VISIBLES
        # ============================================================
        comandos = {}
        for comando in self.bot.command_handler.commands.values():
            nombre = getattr(comando, "name", None)

            if not nombre or nombre in comandos:
                continue

            permisos_requeridos = getattr(comando, "permissions", [])

            if puede_ver_todo or all(
                p in user_permissions for p in permisos_requeridos
            ):
                comandos[nombre] = comando

        # Orden alfabético para que la lista sea fácil de leer.
        comandos = dict(sorted(comandos.items()))

        await self.bot.highrise.send_whisper(
            user.id,
            f"📚 AYUDA DE beBot33\n"
            f"Tu nivel: {nivel}\n"
            f"Comandos disponibles:"
        )

        # Enviamos cada comando por separado para evitar un mensaje
        # demasiado largo.
        for comando in comandos.values():
            descripcion = getattr(
                comando,
                "description",
                "Sin descripción disponible."
            )

            await self.bot.highrise.send_whisper(
                user.id,
                f"/{comando.name} — {descripcion}"
            )
