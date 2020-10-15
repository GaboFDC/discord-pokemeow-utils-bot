import os
import json
import discord
import settings
from discord.utils import find

client = discord.Client()

config_file_sufix = "config.json"


def get_channel(name, guild):
    return find(lambda x: x.name == name, guild.text_channels)


def conf_set(conf, key, value):
    conf[key] = value
    save_config(conf)


def conf_get(conf, key):
    if conf.get(key):
        return conf[key]
    return None


def new_conf(guild):
    conf = {"notify_channel": "general"}
    conf_set(conf, "guild", guild.name + str(guild.id))
    return conf


def save_config(conf):
    with open(conf["guild"] + "_" + config_file_sufix, "w") as f:
        json.dump(conf, f)


def load_config(guild):
    file_name = guild.name + str(guild.id) + "_" + config_file_sufix
    if not os.path.isfile(file_name):
        return new_conf(guild)
    with open(file_name, "r") as f:
        return json.load(f)


# from discord.ext import commands
# bot = commands.Bot(command_prefix="/")
#
# @bot.command()
# async def set_(ctx):
#    pass


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="PokéMeow"))
    settings.logger.info("We have logged in as {0.user}".format(client))


set_notify_channel_command = "/utils set notify channel"


guild_join_message = (
    "Hello {}!\n I'm the PokéMeow utils bot created by @GaboFDC#2764\n"
    + " To settup the notification channel please use: `"
    + set_notify_channel_command
    + "` \n Have fun!"
)

fishing_state_message = "Water state changed. Current water state is:\n"


@client.event
async def on_guild_join(guild):
    new_conf(guild)
    await get_channel("general", guild.name).send(guild_join_message.format(guild.name))


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    settings.logger.info("Got message")
    if message.content == set_notify_channel_command:
        settings.logger.info("Got set_notify_channel_command")
        # load guild conf only when needed
        conf = load_config(message.guild)
        conf_set(conf, "notify_channel", message.channel.name)
        message.channel.send(
            "Successfully changed notify channel to: {}".format(message.channel.name)
        )

    if message.author.name == "PokéMeow":
        settings.logger.info("Got PokéMeow message")
        try:
            data = message.embeds[0].to_dict()
            settings.logger.info("Got embeds message")
            try:
                fishing_state = data["author"]["name"]
                settings.logger.info("Got author.name message")
                fishing_messages = ["cast out", "into the water"]
                if all(x in data["description"] for x in fishing_messages):
                    settings.logger.info("Got fishing_messages message")
                    # load guild conf only when needed
                    conf = load_config(message.guild)
                    prev_fishing_state = conf_get(conf, "fishing_state")
                    if fishing_state != prev_fishing_state:
                        conf_set(conf, "fishing_state", fishing_state)
                        save_config(conf)
                        notify_channel = conf_get(conf, "notify_channel")
                        await get_channel(notify_channel, message.guild).send(
                            fishing_state_message + fishing_state
                        )
            except KeyError:
                pass
        except (AttributeError, IndexError):
            pass

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")


client.run(os.getenv("DISCORD_BOT_TOKEN"))
