import discord
import os  # default module
from dotenv import load_dotenv

# test
from send_email_test import send_email

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
        subject: discord.Option(str, "Enter subject", required = False, default = None),
        body: discord.Option(str, "Enter email body", required = False, default = None),
        attachment: discord.Option(discord.SlashCommandOptionType.attachment, "Add attachments", required = False, default = None)
    ):
    send_email(recipient_email, subject, body, attachment)
    await ctx.send(f"Email sent to {recipient_email} with subject '{subject}'!")

@bot.slash_command(name="test")
async def command(ctx, file: discord.SlashCommandOptionType.attachment):
    print(str(file))
    await ctx.respond(str(file))


bot.run(os.getenv('TOKEN'))  # run the bot with the token
