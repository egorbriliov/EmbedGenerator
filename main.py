import sys
import disnake
from disnake.ext import commands
import variable

bot = commands.InteractionBot(
    reload=True,
    activity=None,
    status=disnake.Status.idle

)


@bot.event
async def on_ready():
    print(f'\033[3;32mБот \033[0m\033[35;1m{bot.user.name}\033[0m\033[3;32m запустился и готов к '
          f'использованию!\033[0m')


bot.load_extensions("cogs/bot/slash_commands")

bot.run(variable.token)
