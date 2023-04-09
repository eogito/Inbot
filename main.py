import time

import discord
import os  # default module
import asyncio
from dotenv import load_dotenv

# test
from send_email_test import send_email
from read_email import get_emails

load_dotenv()  # load all the variables from the env file
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")


@bot.slash_command(name="send", description="Send an email")
async def email(
        ctx,
        recipient_email: str,
        subject: discord.Option(str, "Enter subject", required=False, default=None),
        body: discord.Option(str, "Enter email body", required=False, default=None),
        attachment: discord.Option(discord.SlashCommandOptionType.attachment, "Add attachments", required=False,
                                   default=None)
):
    if send_email(recipient_email, subject, body, attachment):
        await ctx.respond(f"Email sent to {recipient_email} with subject '{subject}'!")
    else:
        await ctx.respond(f"Something went wrong, please try again.")


@bot.slash_command(name="test")
async def command(ctx, file: discord.SlashCommandOptionType.attachment):
    print(str(file))
    await ctx.respond(str(file))


@bot.slash_command(name="read", description="Read your Emails")
async def read(ctx):
    await ctx.respond("Reading emails...")
    while True:
        email_data = get_emails()
        print(email_data)
        if email_data:
            for mail in email_data:
                message = f"{mail[0]}\n{mail[1]}\n\n{mail[2]}"
                message = "%.2000s" % message
                await ctx.respond(message)
        await asyncio.sleep(10)

bot.run(os.getenv('TOKEN'))  # run the bot with the token
