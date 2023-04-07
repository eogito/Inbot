import discord
import os  # default module

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")


bot.run('MTA5Mzk2NzIzMTk0NTI4NTYzMg.GD-xfj.7mWQC_29XxXxOxOi0qduOqTqpSS69dKOkWKxpo')  # run the bot with the token
