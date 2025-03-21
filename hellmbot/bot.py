# -*- coding: utf-8 -*-

from hellmbot.env import env
from hellmbot.db import ServersDB
from hellmbot.logger import formatter, logger, handler
from discord import Intents, Member, VoiceState, Permissions, errors
from discord.utils import oauth_url
from discord.ext import commands
from asyncio import create_task, gather
from asyncio import run as aiorun


###############
# Bot's logic #
###############

def init_bot() -> commands.Bot:
    """
    Initializes the bot object

    :return: Bot class object
    """
    intents = Intents.default()
    intents.members = True
    intents.message_content = True
    return commands.Bot(command_prefix="/", intents=intents)


# Init bot object
bot = init_bot()


def start() -> None:
    """
    Starts bot polling
    """
    aiorun(ServersDB(0).gen_table())
    bot.run(env.BOT_TOKEN, log_formatter=formatter, log_handler=handler)


@bot.event
async def on_ready() -> None:
    """
    Displays a link to add a bot to the server
    """
    await bot.tree.sync()
    client_id = env.CLIENT_ID
    invite = oauth_url(client_id, permissions=Permissions(
        manage_channels=True,
        move_members=True
    ))
    logger.info(f"Your bot invite link: {invite}")


async def clear_channels(db: ServersDB) -> None:
    """
    Clear previously created channels

    :param db: Database
    """
    channels = await db.channels

    async def rm_channel(channel_id: int) -> None:
        await bot.get_channel(channel_id).delete()

    tasks = tuple(map(lambda ch: create_task(rm_channel(ch)), channels))
    await gather(*tasks)
    await db.clear_channels()


async def create_group(server: commands.Context.guild, db: ServersDB) -> None:
    """
    Creates a group of voice channels to move the user and adds their id to the database

    :param server: Discord server
    :param db: Database
    """

    async def task(circle_number: int) -> None:
        vc = await server.create_voice_channel(f"{circle_number + 1} Circle", category=group)
        await db.add_channel(vc.id, circle_number + 1)

    circles_count = env.CIRCLES_COUNT
    group = await server.create_category(f"{circles_count} Circles of Hell")
    for circle in range(circles_count):
        await task(circle)
    logger.info(f"server id {server.id} channels have been added to database")


@bot.hybrid_command(name="create", description="Creates a group of vc to move users")
async def create(ctx: commands.Context) -> None:
    """
    Creates a group of voice channels to move the user and adds their id to the database

    :param ctx: Command context
    """
    server = ctx.guild
    db = ServersDB(server.id)
    await ctx.send("Creating group...", ephemeral=True)
    try:
        if await db.check_server_exists():
            await clear_channels(db)
        await create_group(server, db)
        await ctx.send("Group was created! HF!", ephemeral=True)
    except errors.Any:
        await ctx.send("An error occurred!", ephemeral=True)


lock = []


@bot.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState) -> None:
    """
    Moves the user through the group channels if the user has been connected to one of them

    :param member: Discord member class objet
    :param before: Before state of voice channel
    :param after: After state of voice channel
    """
    server = member.guild.id
    channels = await ServersDB(server).channels

    async def move(initial_channel):
        current_idx = channels.index(after.channel.id)
        logger.info(f"Moving member {member.id} on server {server} ({len(channels) - current_idx} loops)")
        if current_idx + 1 != len(channels):
            tasks = tuple(map(lambda i: member.move_to(bot.get_channel(channels[i + 1])),
                              range(current_idx, len(channels) - 1)))
            for task in tasks:
                await task
        await member.move_to(initial_channel)
        lock.remove(member.id)

    if member.id not in lock:
        if after.channel and after.channel.id in channels:
            lock.append(member.id)
            initial_channel = before.channel
            if initial_channel is not None:
                initial_channel = initial_channel.id
            await move(before.channel)


if __name__ == "__main__":
    start()
