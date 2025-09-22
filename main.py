import discord
import os
import aiohttp
import asyncio

TOKEN = "YOUR_USER_TOKEN"  # User account token | DO NOT USE YOUR MAIN ACCOUNT
GUILD_ID = 123456789       # Server ID
DOWNLOAD_DIR = r"C:\Users\YOUR_USERNAME\Downloads\DiscordScraper"  # Folder
RATE_LIMIT = 1             # Time between each download <-- Avoids bot detection

intents = discord.Intents.all()
client = discord.Client(intents=intents)

async def download_attachment(attachment, folder_path):
    file_path = os.path.join(folder_path, attachment.filename)
    if os.path.exists(file_path):
        print(f"Skipped (already exists): {attachment.filename}")
        return
    
    try:
        await attachment.save(file_path)
        print(f"Downloaded: {attachment.filename}")
        await asyncio.sleep(RATE_LIMIT)
    except Exception as e:
        print(f"Error downloading {attachment.filename}: {e}")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    guild = client.get_guild(GUILD_ID)

    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).read_messages:
            print(f"\nScraping channel: {channel.name}")
            channel_folder = os.path.join(DOWNLOAD_DIR, channel.name)
            os.makedirs(channel_folder, exist_ok=True)

            async for message in channel.history(limit=None, oldest_first=True):
                for attachment in message.attachments:
                    await download_attachment(attachment, channel_folder)

    print("\nScraping complete!")
    await client.close()

client.run(TOKEN, bot=False)
