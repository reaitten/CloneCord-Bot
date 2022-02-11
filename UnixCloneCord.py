# This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# ----------------------------------------------------------------------------------------------------------------------

# CloneCord Bot V6 BETA by REKULOUS with help from Tasky Lizard & Razorback! GClone made by Donwa on GitHub. Original Discord "GClone-Bot" by KushTheApplusser!

# Bot tested by MineRocker, Saaz, REKULOUS, and KushTheApplusser. Inspired by Telegram GClone, GDrive, and Mirror Bots.
# Also inspired by RoshanConnor and Tommmmyums GClone Batch Script for Windows.
# Thank you to all the testers, devs, and all the people over at BIOHAZARD, FREEMEDIAHECKYEAH, The MegaDrive! Thank you to the users of this bot too!

# If you want to help with the development of this bot, you can fork it on GitHub, edit the code you think needs work / add a feature, and create a pull request! Doing this helps me a lot!

# Python module imports. DO NOT TOUCH UNLESS YOU ARE ADDING A NEW FEATURE! These imports make the bot work and function properly!
import logging, subprocess, sys, platform, os, asyncio, time, discord

# unused imports
import json, random, struct

from dotenv import load_dotenv
from time import sleep
from typing import Optional
from discord.ext import commands
from discord.utils import get

# Fetch .env configuration. DO NOT TOUCH
if not os.path.isfile(".env"):
    sys.exit(
        "Your Discord bot '.env' was not found! Please add it and try again. Make sure you CD into the directory of this Python script before you run it and check .env is in there as well!\n\nYour bot config needs to have a prefix and a token for your bot to function and run. Make sure you also have edited your rclone.conf file in Notepad or a Text Editor to get your Service Accounts!"
    )
else:
    load_dotenv()

    TOKEN = os.getenv("TOKEN")
    PREFIX = os.getenv("PREFIX")

# Some sweet bot logging. I don't think it logs GClone commands and stuff like that
LOGGER = logging.getLogger("discord")
LOGGER.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
LOGGER.addHandler(handler)

# Bot prefix set to the one in your config.json file. Don't modify or touch this!
bot = commands.Bot(command_prefix=PREFIX)

# Print this if the bot is ready and start bot status + give GClone details.
@bot.event
async def on_ready():
    LOGGER.info("CloneCord Version 5 Beta")
    LOGGER.info("Connected to bot: {}".format(bot.user.name))
    LOGGER.info("Bot ID: {}".format(bot.user.id))
    # LOGGER.info("CloneCord is Ready!")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            # name=PREFIX + "help to get help! CloneCord V6 BETA",
            name=PREFIX + "help to get help! CloneCord V6 BETA",
        )
    )
    # LOGGER.info("CloneCord Status Ready!")
    LOGGER.info("Python Version: {}".format(platform.python_version()))
    LOGGER.info("Discord.py API version: {}".format(discord.__version__))
    LOGGER.info("GClone Version: %s", subprocess.run(["gclone", "version"]))
    LOGGER.info("GClone Remotes: %s", subprocess.run(["gclone", "listremotes"]))
    LOGGER.info("Setup complete!")


# Block commands in bot DMs for security. If you are using the bot for your own private use and its not in a server, you can remove the bot check.
@bot.check
async def globally_block_dms(ctx: commands.Context):
    return ctx.guild is not None


# Remove default Discord.py help message and replace it with embed one. Send "<your prefix>help <command>" to get info on how to use a command and get GDrive IDs.
# If you want, you can change the help message to what you want it to explain / say!
bot.remove_command("help")


@bot.command()
async def help(ctx: commands.Context, command: Optional[str]):
    list_of_commands = [
        {"command": "clone", "value": "`<source id> <destination id>`"},
        {"command": "move", "value": "`<source id> <destination id>`"},
        {"command": "sync", "value": "`<source id> <destination id>`"},
        {"command": "emptdir", "value": "`<source id>`"},
        {"command": "md5", "value": "`<source id>`"},
        {"command": "rmdi", "value": "`<source id>`"},
        {"command": "dedupe", "value": "`<source id>`"},
        {"command": "mkdir", "value": "`<source id>`"},
        {"command": "purge", "value": "`<source id>`"},
        {"command": "ping", "value": ""},
    ]

    helpEmbed = discord.Embed(
        title="Here are the available bot commands:",
        description="**CloneCord is a Discord bot made to run GClone, an RClone mod for Multiple Service Account support in Discord.**\n\n*Note: All commands below can be ran more than once at the same time, but there is a cooldown, so you don't overload / break the bot!*",
        color=0x87CEEB,
    )
    helpEmbed.set_author(
        name="CloneCord V6 BETA",
        icon_url="https://www.debian-fr.org/uploads/default/original/2X/3/328f860878d4acb13d550a2b12505d181f181713.png",
    )
    helpEmbed.set_footer(
        text="Bot originally created by Kush The A++er#2976. Revamped version by REKULOUS#5580. Thanks to Pratyush.#6969 and Razorback#4637 for the help!",
        icon_url="https://cdn.discordapp.com/emojis/754736642761424986.png",
    )
    helpEmbed.add_field(
        name="help",
        value="Shows this message. Message `?help <command>` to get more info on a command",
        inline=False,
    )
    helpEmbed.add_field(name="clone", value="Clone files / folders to other places")
    helpEmbed.add_field(name="move", value="Move files / folders to other places")
    helpEmbed.add_field(name="sync", value="Sync source links to destination links")
    helpEmbed.add_field(name="emptdir", value="Empty folder contents to the trash can")
    helpEmbed.add_field(
        name="md5", value="Produce an MD5 File hash for all contents in a folder"
    )
    helpEmbed.add_field(name="rmdi", value="Remove empty directories in a folder")
    helpEmbed.add_field(
        name="dedupe",
        value="Deduplicate files / folders. Great for mass removing duplicates of cloned files",
    )
    helpEmbed.add_field(name="mkdir", value="Create directories / folders")
    helpEmbed.add_field(name="purge", value="Delete a directory and all its contents")
    helpEmbed.add_field(
        name="ping", value="Get the bot's current websocket and API latency"
    )
    if command:
        for com in list_of_commands:
            if com["command"] == command:
                embed1 = discord.Embed(
                    title=command,
                    description=f"?{command} {com['value']}",
                    color=0x87CEEB,
                )
                embed1.set_author(
                    name="CloneCord V6 BETA",
                    icon_url="https://1.bp.blogspot.com/-M5PLcSana6M/XgBHF7jUjiI/AAAAAAAAUzs/S24qhuijluwKlzIOnc2gntoI-U83ZsrJACLcBGAsYHQ/s1600/rclone_logo.png",
                )
                embed1.set_footer(
                    text="Source and Destination IDs can be found by finding the jumbled up letters & numbers at the end of a GDrive folder / file URL. Example: 1Zsh8DctvvWZzJgiEI_sqxVoxvKv9VsYp",
                    icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Google_Drive_logo.png/1200px-Google_Drive_logo.png",
                )
                await ctx.send(embed=embed1)
    else:
        await ctx.send(embed=helpEmbed)


# = = = = { GCLONE BOT COMMANDS } = = = =
# All bot commands here can be ran more than once at the same time, but running too many commands at once can create problems that you don't want.
# It is recommended you not touch most of this code if you don't know what you are doing!
# As of now, there is no code for checking GDrive Folder IDs so you probably have to check a folder for yourself or check logs.

# GClone Folder / File Clone Command
@bot.command()
@commands.cooldown(1, 140, commands.BucketType.user)
async def clone(ctx: commands.Context, source, destination):
    s1 = "{" + source + "}"
    d1 = "{" + destination + "}"
    await ctx.send(
        "***Check the destination folder in 5 minutes if your clone is couple terabytes. If your clone is less than a terabyte, the clone will be complete within a couple of seconds!***"
    )
    proc = await asyncio.create_subprocess_exec(
        [
            "gclone",
            "copy",
            f"GC:{s1}",
            f"GC:{d1}",
            "--transfers",
            "50",
            "-vP",
            "--stats-one-line",
            "--stats=15s",
            "--ignore-existing",
            "--drive-server-side-across-configs",
            "--drive-chunk-size",
            "128M",
            "--drive-acknowledge-abuse",
            "--drive-keep-revision-forever",
        ]
    )
    await proc.wait()
    await ctx.send(
        "**Cloning Complete** --- https://drive.google.com/drive/folders/{}".format(
            destination
        )
    )
    LOGGER.info("Cloning Complete)!")


# GClone Folder / File Move Command
@bot.command()
@commands.cooldown(1, 140, commands.BucketType.user)
async def move(ctx: commands.Context, source, destination):
    s1 = "{" + source + "}"
    d1 = "{" + destination + "}"
    await ctx.send(
        "***Check the destination folder in 5 minutes if your transfer is couple terabytes. If your transfer is less than a terabyte, the clone will be complete within a couple of seconds!***"
    )
    proc = await asyncio.create_subprocess_exec(
        [
            "gclone",
            "move",
            f"GC:{s1}",
            f"GC:{d1}",
            "--transfers",
            "50",
            "--tpslimit-burst",
            "50" "--checkers",
            "10",
            "-vP",
            "--stats-one-line",
            "--stats=15s",
            "--ignore-existing",
            "--drive-server-side-across-configs",
            "--drive-chunk-size",
            "128M",
            "--drive-acknowledge-abuse",
            "--drive-keep-revision-forever",
            "--fast-list",
        ]
    )
    await proc.wait()
    await ctx.send(
        "**Moved files to destination sucessfully.** --- https://drive.google.com/drive/folders/{}".format(
            destination
        )
    )
    LOGGER.info("Moved files to destination sucessfully.")


# GClone Sync Command
@bot.command()
@commands.cooldown(1, 140, commands.BucketType.user)
async def sync(ctx: commands.Context, source, destination):
    s1 = "{" + source + "}"
    d1 = "{" + destination + "}"
    await ctx.send(
        "***CloneCord is syncing... it should be done syncing in a couple of minutes!***"
    )
    proc = await asyncio.create_subprocess_exec(
        [
            "gclone",
            "sync",
            f"GC:{s1}",
            f"GC:{d1}",
            "--transfers",
            "50",
            "--tpslimit-burst",
            "50",
            "--checkers",
            "10",
            "-vP",
            "--stats-one-line",
            "--stats=15s",
            "--drive-server-side-across-configs",
            "--drive-chunk-size",
            "128M",
            "--drive-acknowledge-abuse",
            "--drive-keep-revision-forever",
            "--fast-list",
        ]
    )
    await proc.wait()
    await ctx.send(
        "**Sync Completed** --- https://drive.google.com/drive/folders/{}".format(
            destination
        )
    )
    LOGGER.info("Syncronized Sucessfully.")


# GClone Empty / Clear Directory Command
@bot.command()
@commands.cooldown(1, 140, commands.BucketType.user)
async def emptdir(ctx: commands.Context, source):
    s1 = "{" + source + "}"
    await ctx.send(
        "*CloneCord is emptying the directory... it should be done in around 5 minutes if your directory is big!* **If you are worried about losing your deleted files forever, don't worry! You can recover stuff from your trash can!**"
    )
    proc = await asyncio.create_subprocess_exec(
        ["gclone", "delete", f"GC:{s1}", "-vP", "--drive-trashed-only", "--fast-list"]
    )
    await proc.wait()
    await ctx.send(
        "**Deleted Sucessfully!** --- https://drive.google.com/drive/folders/{}".format(
            source
        )
    )
    LOGGER.info("Deleted Sucessfully!")


# GClone md5sum file creation for all the objects in a directory
@bot.command()
@commands.cooldown(1, 140, commands.BucketType.user)
async def md5(ctx: commands.Context, source):
    s1 = "{" + source + "}"
    await ctx.send("***Producing MD5 Hash, please wait...***")
    proc = await asyncio.create_subprocess_exec(
        ["gclone", "md5sum", f"GC:{s1}", "--fast-list"]
    )
    await proc.wait()
    await ctx.send(
        "**Finished Producing MD5** --- https://drive.google.com/drive/folders/{}".format(
            source
        )
    )
    LOGGER.info("Sucessfully created MD5 Hash!")


# GClone Remove Empty Directories
@bot.command()
@commands.cooldown(1, 140, commands.BucketType.user)
async def rmdi(ctx: commands.Context, source):
    s1 = "{" + source + "}"
    await ctx.send(
        "*Removing empty directories... this should take a few seconds or more.* **If you want to recover your empty folders, don't worry, they will be in your trash can!**"
    )
    proc = await asyncio.create_subprocess_exec(
        [
            "gclone",
            "rmdirs" f"GC:{s1}",
            "-v",
            "--stats-one-line",
            "--stats=15s",
            "--fast-list",
        ]
    )
    await proc.wait()
    await ctx.send(
        "**Deleted all empty directories!** --- https://drive.google.com/drive/folders/{}".format(
            source
        )
    )
    LOGGER.info("Deleted all empty directories!")


# GClone Dedupe Files / Folders
@bot.command()
@commands.cooldown(1, 140, commands.BucketType.user)
async def dedupe(ctx: commands.Context, source):
    s1 = "{" + source + "}"
    await ctx.send(
        "*Deduplicating files... this should take a few seconds or more.* **If you want to recover your files / folders, don't worry, they will be in your trash can!**"
    )
    proc = await asyncio.create_subprocess_exec(
        ["gclone", "dedupe", "--dedupe-mode", "newest", f"GC:{s1}", "-v", "--fast-list"]
    )
    await proc.wait()
    await ctx.send(
        "**Finished Dedupe** --- https://drive.google.com/drive/folders/{}".format(
            source
        )
    )
    LOGGER.info("Sucess on deduplicating!")


# GClone Create Directory
@bot.command()
@commands.cooldown(1, 140, commands.BucketType.user)
async def mkdir(ctx: commands.Context, source):
    s1 = "{" + source + "}"
    await ctx.send("***Creating directory...***")
    proc = await asyncio.create_subprocess_exec(["gclone", "mkdir", f"GC:{s1}"])
    await proc.wait()
    await ctx.send(
        "**Created directory** --- https://drive.google.com/drive/folders/{}".format(
            source
        )
    )
    LOGGER.info("Created Directory!")


# GClone Purge Folders
@bot.command()
@commands.cooldown(1, 140, commands.BucketType.user)
async def purge(ctx: commands.Context, source):
    s1 = "{" + source + "}"
    await ctx.send("***Purging directory...***")
    proc = await asyncio.create_subprocess_exec(
        [
            "gclone",
            "purge",
            f"GC:{s1}",
            "-vP",
            "--stats-one-line",
            "--stats=15s",
            "--fast-list",
        ]
    )
    await proc.wait()
    await ctx.send(
        "**Deleted folder & its contents sucessfully!** --- https://drive.google.com/drive/folders/{}".format(
            source
        )
    )
    LOGGER.info("Deleted folder & its contents sucessfully!")


# CloneCord Error Messages to make the bot have a command cooldown and send error messages about invalid commands / arguments
@clone.error
@move.error
@sync.error
@emptdir.error
@md5.error
@rmdi.error
@dedupe.error
@mkdir.error
@purge.error
# All commands by default have a 140 Second Cooldown. If you want, you can remove the code before "else:" to remove cooldowns. Don't remove @<command>.error stuff!
# Not recommended to remove this if you are using this bot in a server with other people than you though.
# Be sure to remove the @commands.cooldown(1, 140, commands.BucketType.user) stuff too in the code for commands if you want to remove cooldowns.
async def error(ctx: commands.Context, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(error)
        return
    else:
        await ctx.send(
            "**There is an error in your command:** `{}`".format(error)
            + "\n**Use `?help` or `?help <command>` to get help on commands!**"
        )


# = = = = {EXTRA COMMANDS / BOT UTILITY} = = = =

# Ping Command to get the bot's current websocket and API latency
@bot.command()
async def ping(ctx: commands.Context):
    start_time = time.time()
    message = await ctx.send("Pinging...")
    end_time = time.time()

    await message.edit(
        content=f":ping_pong:    *Pong!*    **`{round(bot.latency * 1000)}ms`**    :ping_pong:\n:ping_pong:    **API Ping:** **`{round((end_time - start_time) * 1000)}ms`**  :ping_pong:"
    )
    LOGGER.debug("Recieved ping!")


# Start the bot, DO NOT TOUCH!
bot.run(TOKEN)
