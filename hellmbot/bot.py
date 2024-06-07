# -*- coding: utf-8 -*-

from hellmbot.env import ENV
from hellmbot.db import ServersDB
from discord import Intents, Member, VoiceState, Permissions
from discord.utils import oauth_url
from discord.ext import commands


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
    bot.run(ENV.BOT_TOKEN.fget(None))


@bot.event
async def on_ready() -> None:
    """
    Displays a link to add a bot to the server
    """
    await bot.tree.sync()
    client_id = ENV.CLIENT_ID.fget(None)
    invite = oauth_url(client_id, permissions=Permissions(
        manage_channels=True,
        move_members=True
    ))
    print(f"Your bot invite link: {invite}")


@bot.hybrid_command(name="create", description="Creates a group of vc to move users")
async def create(ctx: commands.Context) -> None:
    """
    Creates a group of voice channels to move the user and adds their id to the database

    :param ctx: Command context
    """
    server = ctx.guild
    db = ServersDB(server.id)
    circles_count = ENV.CIRCLES_COUNT.fget(None)
    group = await server.create_category(f"{circles_count} Circles of Hell")
    await ctx.send("Creating vc's...", ephemeral=True)
    if db:
        channels = db.channels
        for channel in channels:
            channel = bot.get_channel(channel)
            await channel.delete()
        db.clear_channels()
    for circle in range(circles_count):
        vc = await server.create_voice_channel(f"{circle + 1} Circle", category=group)
        db.add_channel(vc.id, circle + 1)


user_before_channels = {}


@bot.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState) -> None:
    """
    Moves the user through the group channels if the user has been connected to one of them

    :param member: Discord member class objet
    :param before: Before state of voice channel
    :param after: After state of voice channel
    """
    server = member.guild.id
    if before.channel != after.channel:
        db = ServersDB(server)
        channels = db.channels
        if after.channel and after.channel.id in channels:
            if member.id not in tuple(user_before_channels.keys()):
                user_before_channels[member.id] = None
                if before.channel is not None:
                    user_before_channels[member.id] = before.channel.id
            current_idx = channels.index(after.channel.id)
            if current_idx + 1 != len(channels):
                next_channel = bot.get_channel(channels[current_idx + 1])
            else:
                next_id = user_before_channels[member.id]
                del user_before_channels[member.id]
                if next_id is None:
                    next_channel = next_id
                else:
                    next_channel = bot.get_channel(next_id)
            await member.move_to(next_channel)


if __name__ == "__main__":
    start()
