import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration - Load from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# Validate that all required environment variables are set
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
if not DISCORD_BOT_TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN not found in environment variables")
if not DISCORD_CHANNEL_ID:
    raise ValueError("DISCORD_CHANNEL_ID not found in environment variables")

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
discord_bot = commands.Bot(command_prefix="!", intents=intents)

@discord_bot.event
async def on_ready():
    print(f'✅ Discord bot logged in as {discord_bot.user}')
    print(f'✅ Discord bot ID: {discord_bot.user.id}')
    channel = discord_bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        print(f'✅ Found Discord channel: {channel.name} (ID: {channel.id})')
    else:
        print(f'❌ WARNING: Could not find channel with ID {DISCORD_CHANNEL_ID}')
    print(f'✅ Ready to relay messages!')

async def send_to_discord(message_text, username, chat_name=None):
    """Send message to Discord with @everyone mention"""
    print(f"🔄 send_to_discord called with: username={username}, chat_name={chat_name}")
    print(f"🔍 Discord bot ready: {discord_bot.is_ready()}")

    channel = discord_bot.get_channel(DISCORD_CHANNEL_ID)

    if channel:
        if chat_name:
            content = f"@everyone **[{chat_name}]** {username}: {message_text}"
        else:
            content = f"@everyone {username}: {message_text}"

        try:
            await channel.send(content)
            print(f"📤 Successfully sent to Discord: {content[:80]}...")
        except Exception as e:
            print(f"❌ Error sending to Discord: {e}")
    else:
        print(f"❌ Channel not found! Check your DISCORD_CHANNEL_ID: {DISCORD_CHANNEL_ID}")
        print(f"🔍 Available channels: {[c.id for c in discord_bot.get_all_channels()]}")

# Telegram Bot Setup
async def handle_telegram_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming Telegram messages"""
    print(f"🔔 handle_telegram_message triggered!")
    print(f"📋 Update type: {type(update)}")
    print(f"📋 Has message: {update.message is not None}")

    if update.message:
        print(f"📋 Message details:")
        print(f"   - Chat type: {update.message.chat.type}")
        print(f"   - Chat ID: {update.message.chat.id}")
        print(f"   - Chat title: {update.message.chat.title}")
        print(f"   - Has text: {update.message.text is not None}")

        if update.message.text:
            message_text = update.message.text
            user = update.message.from_user
            username = user.first_name or user.username or "Unknown"
            chat_name = update.message.chat.title if update.message.chat.title else None

            print(f"📨 Received from Telegram [{chat_name}] {username}: {message_text[:50]}...")

            # Send to Discord
            await send_to_discord(message_text, username, chat_name)
        else:
            print(f"⚠️ Message has no text content")
    else:
        print(f"⚠️ Update has no message")

async def main():
    """Run both bots"""
    print("🚀 Starting bots...")

    # Build Telegram app
    print("🤖 Starting Telegram bot...")
    telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handler for ALL messages (for debugging)
    # This will help us see what type of messages are coming in
    message_handler = MessageHandler(filters.ALL, handle_telegram_message)
    telegram_app.add_handler(message_handler)
    print(f"📝 Added handler for ALL messages (debugging mode)")

    # Initialize Telegram app
    await telegram_app.initialize()
    await telegram_app.start()

    # Start Discord bot
    discord_task = asyncio.create_task(discord_bot.start(DISCORD_BOT_TOKEN))

    # Wait for Discord bot to be ready
    await asyncio.sleep(3)

    print("✅ Both bots are running!")
    print("💬 Send a message in your Telegram group to test!")
    print("Press Ctrl+C to stop")

    # Start Telegram polling
    await telegram_app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    print("🔄 Telegram polling started - waiting for messages...")
    print(f"📡 Bot username: {telegram_app.bot.username if hasattr(telegram_app.bot, 'username') else 'Unknown'}")

    # Keep running until interrupted
    try:
        await asyncio.Future()  # Run forever
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        # Cleanup
        await telegram_app.updater.stop()
        await telegram_app.stop()
        await telegram_app.shutdown()
        await discord_bot.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bots stopped!")