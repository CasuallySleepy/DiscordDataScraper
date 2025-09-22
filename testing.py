import os
import asyncio

DOWNLOAD_DIR = r"C:\Users\YOUR_USERNAME\Downloads\DiscordScraper"
RATE_LIMIT = 1  # seconds

class MockAttachment:
    def __init__(self, filename):
        self.filename = filename
    
    async def save(self, path):
        # Instead of downloading, it creates a test textfile
        with open(path, "w") as f:
            f.write("This is a test file.")
        await asyncio.sleep(0.1)  # simulate async delay

class MockMessage:
    def __init__(self, attachments):
        self.attachments = attachments

class MockChannel:
    def __init__(self, name, messages):
        self.name = name
        self.messages = messages

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

async def main():
    # Simulates server with 2 channels
    channels = [
        MockChannel("general", [MockMessage([MockAttachment("test1.txt"), MockAttachment("test2.txt")])]),
        MockChannel("random", [MockMessage([MockAttachment("fun.txt")])])
    ]

    for channel in channels:
        print(f"\nScraping channel: {channel.name}")
        channel_folder = os.path.join(DOWNLOAD_DIR, channel.name)
        os.makedirs(channel_folder, exist_ok=True)

        for message in channel.messages:
            for attachment in message.attachments:
                await download_attachment(attachment, channel_folder)

    print("\nScraping complete!")

asyncio.run(main())
