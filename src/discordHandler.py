import discord 
import logging
import os
import imgHandler
import io
from datetime import datetime
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("Discord token missing from environment variables")

log_handler =  logging.FileHandler(filename="QBot.log", encoding="utf-8", mode="w")

async def scrape_msg(msg):
    name = msg.author.name
    content = msg.content
    avatarBytes = await msg.author.display_avatar.with_format('png').with_size(512).read()
    time = datetime.now().strftime("%d/%m/%Y")
    
    return name, content, avatarBytes, time


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    
    if msg.content.startswith("$hello"):
        await msg.channel.send("Wagwan")

    if msg.content.startswith("$quotets") and msg.reference is not None:
        replyMsg = msg.reference.resolved

        if isinstance(replyMsg, discord.Message):
            scrapedMsg = await scrape_msg(replyMsg)

            img = imgHandler.imgQuote(*scrapedMsg) # unpack tuple 
            
            with io.BytesIO() as bin:
                img.save(bin, "PNG")
                bin.seek(0) # reset stream pointer

                await msg.channel.send(file = discord.File(fp=bin, filename="quote.png"))

    
        

client.run(TOKEN, log_handler=log_handler)

    