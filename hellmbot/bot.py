# -*- coding: utf-8 -*-

from hellmbot.env import ENV
from hellmbot.db import ServersDB
from discord import Intents
from discord.ext import commands


###############
# Bot's logic #
###############

def init_bot() -> commands.Bot:
    intents = Intents.default()
    intents.message_content = True
    return commands.Bot(command_prefix="/", intents=intents)


bot = init_bot()


def start() -> None:
    bot.run(ENV.BOT_TOKEN.fget(None))


@bot.command()
async def create(ctx: commands.Context) -> None:
    server = ctx.guild
    db = ServersDB(server.id)
    circles_count = ENV.CIRCLES_COUNT.fget(None)
    group = await server.create_category(f"{circles_count} Circles of Hell")
    if db:
        db.clear_channels()
    for circle in range(circles_count):
        vc = await server.create_voice_channel(f"{circle + 1} Circle", category=group)
        db.add_channel(vc.id, circle + 1)


if __name__ == "__main__":
    start()
