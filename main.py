import discord
import os
import asyncio
from dotenv import load_dotenv

from send_email import send_email
from read_email import get_emails

load_dotenv()  # load all the variables from the env file
bot = discord.Bot()
reading = False


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="send", description="Send an email")
async def email(
        ctx,
        recipient_email: str,
        subject: discord.Option(str, "Enter subject", required=False, default=None),
        body: discord.Option(str, "Enter email body", required=False, default=None),
        attachment: discord.Option(discord.SlashCommandOptionType.attachment, "Add attachments", required=False,
                                   default=None)
    ):
    await ctx.respond("Sending email...")
    if send_email(recipient_email, subject, body, attachment):
        await ctx.respond(f"Email sent to {recipient_email} with subject '{subject}'!")
    else:
        await ctx.respond(f"Something went wrong, please try again.")


@bot.slash_command(name="read", description="Read your Emails")
async def read(ctx):
    global reading
    reading = True
    await ctx.respond("Reading emails...")
    while reading:
        email_data = get_emails()
        print(email_data)
        if email_data:
            for mail in email_data:
                message = f"{mail[0]}\n{mail[1]}\n\n{mail[2]}"
                message = "%.2000s" % message
                await ctx.respond(message)
        await asyncio.sleep(10)


@bot.slash_command(name="stop", description="Stop Reading Emails")
async def stop(ctx):
    global reading
    if reading:
        reading = False
        await ctx.respond("Emails have been stopped")
    else:
        await ctx.respond("Emails are not currently being read!")



bot.run(os.getenv('TOKEN'))  # run the bot with the token
