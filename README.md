# Inbot
Inbot is a discord bot submission to LyonHacks III.

## How to use it
- First go to the Discord Developer Portal: https://discord.com/developers/applications
- Click "New Application" to make a new bot ![New application button](https://cdn.discordapp.com/attachments/1091179196425965668/1094807448361127936/image.png)
- Navigate to the "Bot" section and copy the token ![Bot token](https://cdn.discordapp.com/attachments/1091179196425965668/1094807448545656883/image.png)
- Navigate to "OAuth2" and "URL Generator" and select these 2 options and invite the bot to a server [Permissions](https://cdn.discordapp.com/attachments/1091179196425965668/1094807448767959081/image.png)
- Finally change the .env file to contain your bot token and run main.py

## What it does

Inbot uses Gmail API and py-cord in order to create a bot that functions as a inbox. The bot has 2 main functions, reading emails and sending emails. Reading emails sends you and message every time you receieve a new email, containing the sender, subject and body content. After, the bot makes the email read. Sending emails allows users to send emails to 1 specified email address. They are able to attach 1 file.

## How we built it

We first made a Discord bot in Python that can accept slash commands. Then we researched about the Gmail API and them intergrated that into our Discord bot. We then spent a long time figuring out how Google monitors and enforces security. 

## Challenges we ran into

Badly documented code. _Someone's(Alex's)_  sleep schedule, No previous experience with API's, databases and setting up webservers.

## Accomplishments that we're proud of

Functional discord bot to access Gmail, with the ability to read and send emails. 
An almost-functional SQL webserver 

## What we learned

We learned a lot about how Python works as a language, and also to connect it with making a Discord bot. In addition, the Gmail API taught us a lot about the security and safety precautions used by Google to keep your private mail safe. We also learned how to use SQL with Python, despite not using it, and it provides us with the basic knowledge for future projects.

## What's next for Inbot

In the future, we want to make our bot run globally, allowing other users to access the bot. This requires us to host a server for all users to connect to and databases to hold each person's token. 
