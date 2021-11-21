import discord
from discord.ext import commands, tasks
from datetime import datetime
from pytz import timezone
import asyncio

TOKEN = token

bot = commands.Bot(command_prefix="-", case_insensitive=True)

@bot.command()
async def ping(ctx):
    await ctx.channel.send('pong')

@bot.event
async def on_ready():
    change_status.start()
    print("Time Lord is in the tardis")
    print("-------------")
    return await bot.change_presence(status=discord.Status.online)

@tasks.loop(seconds=60)
async def change_status():
    # PST, MST, CST, EST, CEST, MSK, CEST
    format = "%H:%M"

    nowutc = datetime.now(timezone('UTC'))
    nowpt = nowutc.astimezone(timezone('America/Los_Angeles'))
    nowmt = nowutc.astimezone(timezone('America/Denver'))
    nowct = nowutc.astimezone(timezone('America/Chicago'))
    nowet = nowutc.astimezone(timezone('America/New_York'))
    nowcet = nowutc.astimezone(timezone('Europe/Paris'))
    nowmsk = nowutc.astimezone(timezone('Europe/Oslo'))
    nowcst = nowutc.astimezone(timezone('Asia/Shanghai'))

    name = (f"{nowutc.strftime(format)} UTC | Time Lord")
    await bot.edit(nick=name)

    await bot.change_presence(activity=discord.Game(f"""{nowpt.strftime(format)} PT | {nowmt.strftime(format)} MT | {nowct.strftime(format)} CT | {nowet.strftime(format)} ET | {nowcet.strftime(format)} CET | {nowmsk.strftime(format)} MSK | {nowcst.strftime(format)} CST
    """))


@bot.command()
async def reload(ctx):
    change_status.cancel()
    async with ctx.typing():
        await asyncio.sleep(3)
        change_status.start()
    msg = await ctx.channel.send("Time Reloaded")


bot.run(TOKEN)

