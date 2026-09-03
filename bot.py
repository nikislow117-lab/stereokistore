import discord
import os

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot is online! Logged in as {bot.user}')
    print(f'📊 Connected to {len(bot.guilds)} servers')
    
    # Try to send a message to your channel
    channel = bot.get_channel(int(os.getenv('CHANNEL_ID', 0)))
    if channel:
        await channel.send("🚀 Bot is online! Ready to post transactions.")

bot.run(TOKEN)
