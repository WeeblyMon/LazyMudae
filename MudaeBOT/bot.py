import discord
from discord.ext import commands
import re
import asyncio

token = "" # Insert discord token here
CHANNEL_ID = ""  # right-click over the channel that has mudae, "Copy Channel ID"
desiredKakera = 300  # auto claim threshold, change as needed
always_click_emojis = ['kakeraY', 'kakeraO', 'kakeraR', 'kakeraW', 'kakeraL']  # will click on kakeraYellow and onwards
claim_emojis = ['💖', '💗', '💘', '❤️', '💓', '💕', '♥️']  # add emojis here if server uses custom claim emojis
kakera_react_ready = False  # leave this
tu_interval = 7200  # this is set to 2 hours by default
username = "test"  # set this to your username or any other username you'd like to track
channel = None
client = commands.Bot(command_prefix="!")

#its better to use config.json or something similar. made it into string first so users find it easier to edit.
CHANNEL_ID = int(CHANNEL_ID)

@client.event
async def on_ready():
    global channel
    print("Selfbot is ready to be used.")
    print(f"Logged in as {client.user.name}")
    print("Command Prefix is !")
    #this way channel is not created each time repeat_tu is send
    try:
        channel = client.get_channel(CHANNEL_ID)
        if channel is None:
            raise Exception(f"Channel with ID {CHANNEL_ID} not found.")
        asyncio.create_task(repeat_tu())
    except Exception as e:
        print(f"Failed to retrieve channel with id {CHANNEL_ID}\nError: {e}")

"""
not needed:-
async def click_reaction_button(message, button):
    if button.custom_id:
        payload = {
            "type": 3,
            "message_flags": 0,
            "application_id": str(message.author.id),
            "guild_id": str(message.guild.id),
            "channel_id": str(message.channel.id),
            "message_id": str(message.id),
            "session_id": "your_session_id_here",
            "data": {
                "component_type": 2,
                "custom_id": button.custom_id
            }
        }
        await client.http.request(
            discord.http.Route(
                "POST", "/interactions"
            ),
            json=payload
        )
        print(f"Clicked the button with emoji: {button.emoji.name if button.emoji else 'No Emoji'}")"""

async def roll_n_times(channel, rolls):
    print(f"Starting {rolls} roll(s)...")
    for i in range(rolls):
        await channel.send("$w")
        print(f"Rolled {i + 1}/{rolls}")
        await asyncio.sleep(1)

async def repeat_tu():
    global channel, tu_interval
    while True:
        if channel:
            await channel.send("$tu")
            print(f"Sent $tu in channel: {channel.name}")
        else:
            print("Channel not found.")
        await asyncio.sleep(tu_interval)

async def retry_dk(channel, retries=5, delay=5):
    for _ in range(retries):
        await asyncio.sleep(delay)
        await channel.send("$dk")
        print(f"Sent $dk, waiting for Mudae's response...")
        await asyncio.sleep(5)

@client.event
async def on_message(message):
    global kakera_react_ready
    kakera_amount = 0

    if message.channel.id == CHANNEL_ID and message.author != client.user:
        if message.content:
            print(f"Message from {message.author}: {message.content}")

        if "added to your kakera collection!" in message.content:
            print("Kakera successfully added! No need to resend $dk.")
            return

        if "You __can__ react to kakera right now!" in message.content:
            kakera_react_ready = True
            print("Kakera reactions are available!")

        if "you can't react to kakera" in message.content:
            kakera_react_ready = False
            print("Kakera reactions are no longer available.")

        if username in message.content and "you __can__ claim right now" in message.content:
            rolls_match = re.search(r"You have \*\*(\d+)\*\* rolls left", message.content)
            if rolls_match:
                rolls_left = int(rolls_match.group(1))
                print(f"Rolls Left: {rolls_left}")
                if rolls_left > 0:
                    print(f"Conditions met: Rolling {rolls_left} times!")
                    channel = client.get_channel(CHANNEL_ID)
                    await roll_n_times(channel, rolls_left)
                else:
                    print(f"No rolls available. Rolls left: {rolls_left}")

        if "$daily is available" in message.content:
            print("$daily is available! Claiming $daily...")
            channel = client.get_channel(CHANNEL_ID)
            await channel.send("$daily")

        if "$dk is ready" in message.content:
            print("$dk is ready! Claiming $dk...")
            channel = client.get_channel(CHANNEL_ID)
            await retry_dk(channel)

        if message.embeds:
            for embed in message.embeds:
                if embed.author:
                    print("Character Name:", embed.author.name)
                print("Series:", embed.description)

                kakera_text = embed.description.split("**")
                if len(kakera_text) >= 2:
                    try:
                        kakera_amount = int(kakera_text[1].strip().replace(",", ""))
                        print(f"Kakera Amount: {kakera_amount}")
                    except ValueError:
                        print(f"Error parsing Kakera amount: {kakera_text[1]}")

        if message.components and kakera_react_ready:
            for component in message.components:
                for button in component.children:
                    print(f"Found button with custom_id: {button.custom_id}, emoji: {button.emoji}, label: {button.label}")
                    if button.emoji and button.emoji.name in claim_emojis:
                        if kakera_amount >= desiredKakera:
                            print(f"Claim Button (Heart Emoji) Found with Kakera Amount: {kakera_amount}. Clicking...")
                            await button.click()

                    if button.emoji and button.emoji.name in always_click_emojis:
                        print(f"Kakera Button Found: {button.emoji.name}. Clicking...")
                        await button.click()

    await client.process_commands(message)

@client.command()
async def set_tu_interval(ctx, hours: float):
    global tu_interval
    tu_interval = hours * 60 * 60
    await ctx.send(f"Adjusted $tu interval to {hours} hour(s).")

client.run(token)
