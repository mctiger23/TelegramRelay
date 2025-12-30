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
DISCORD_ROLE_ID = os.getenv("DISCORD_ROLE_ID")  # Optional: Role ID to mention

# Determine the mention string to use
if DISCORD_ROLE_ID:
    DISCORD_MENTION = f"<@&{DISCORD_ROLE_ID}>"  # Proper Discord role mention format
else:
    DISCORD_MENTION = "@everyone"  # Default to @everyone if no role specified

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

async def send_to_discord(message_text, username, chat_name=None, file_path=None, file_name=None):
    """Send message to Discord with configurable mention and optional file attachment"""
    print(f"🔄 send_to_discord called with: username={username}, chat_name={chat_name}, file={file_name}")
    print(f"🔍 Discord bot ready: {discord_bot.is_ready()}")

    channel = discord_bot.get_channel(DISCORD_CHANNEL_ID)

    if channel:
        if chat_name:
            content = f"{DISCORD_MENTION} **[{chat_name}]** {username}: {message_text}" if message_text else f"{DISCORD_MENTION} **[{chat_name}]** {username}"
        else:
            content = f"{DISCORD_MENTION} {username}: {message_text}" if message_text else f"{DISCORD_MENTION} {username}"

        try:
            if file_path:
                # Send message with file attachment
                with open(file_path, 'rb') as f:
                    discord_file = discord.File(f, filename=file_name)
                    await channel.send(content=content, file=discord_file)
                print(f"📤 Successfully sent to Discord with file: {file_name}")
                # Clean up the downloaded file
                try:
                    os.remove(file_path)
                    print(f"🗑️ Cleaned up temporary file: {file_path}")
                except Exception as e:
                    print(f"⚠️ Could not delete temp file {file_path}: {e}")
            else:
                # Send text-only message
                await channel.send(content)
                print(f"📤 Successfully sent to Discord: {content[:80]}...")
        except Exception as e:
            print(f"❌ Error sending to Discord: {e}")
            # Clean up file if send failed
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except:
                    pass
    else:
        print(f"❌ Channel not found! Check your DISCORD_CHANNEL_ID: {DISCORD_CHANNEL_ID}")
        print(f"🔍 Available channels: {[c.id for c in discord_bot.get_all_channels()]}")

# Telegram Bot Setup
async def handle_telegram_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming Telegram messages including text, photos, videos, and documents"""
    print(f"🔔 handle_telegram_message triggered!")
    print(f"📋 Update type: {type(update)}")
    print(f"📋 Has message: {update.message is not None}")

    if update.message:
        message = update.message
        print(f"📋 Message details:")
        print(f"   - Chat type: {message.chat.type}")
        print(f"   - Chat ID: {message.chat.id}")
        print(f"   - Chat title: {message.chat.title}")
        print(f"   - Has text: {message.text is not None}")
        print(f"   - Has photo: {message.photo is not None and len(message.photo) > 0 if message.photo else False}")
        print(f"   - Has video: {message.video is not None}")
        print(f"   - Has document: {message.document is not None}")

        user = message.from_user
        username = user.first_name or user.username or "Unknown"
        chat_name = message.chat.title if message.chat.title else None

        # Get caption or text
        message_text = message.caption if message.caption else message.text

        file_path = None
        file_name = None

        # Handle different message types
        try:
            # Handle photos
            if message.photo:
                print(f"📷 Processing photo message...")
                # Get the largest photo size
                photo = message.photo[-1]
                file = await context.bot.get_file(photo.file_id)
                file_name = f"photo_{photo.file_id}.jpg"
                file_path = f"/tmp/{file_name}"
                await file.download_to_drive(file_path)
                print(f"📥 Downloaded photo: {file_name}")

            # Handle videos
            elif message.video:
                print(f"🎥 Processing video message...")
                video = message.video
                file = await context.bot.get_file(video.file_id)
                file_name = video.file_name or f"video_{video.file_id}.mp4"
                file_path = f"/tmp/{file_name}"
                await file.download_to_drive(file_path)
                print(f"📥 Downloaded video: {file_name}")

            # Handle documents
            elif message.document:
                print(f"📄 Processing document message...")
                document = message.document
                file = await context.bot.get_file(document.file_id)
                file_name = document.file_name or f"document_{document.file_id}"
                file_path = f"/tmp/{file_name}"
                await file.download_to_drive(file_path)
                print(f"📥 Downloaded document: {file_name}")

            # Handle text-only messages
            elif message.text:
                print(f"💬 Processing text message...")

            else:
                print(f"⚠️ Message type not supported (might be sticker, audio, etc.)")
                return

            # Send to Discord
            if message_text or file_path:
                print(f"📨 Received from Telegram [{chat_name}] {username}: {message_text[:50] if message_text else '[Media]'}...")
                await send_to_discord(message_text or "", username, chat_name, file_path, file_name)
            else:
                print(f"⚠️ No content to relay")

        except Exception as e:
            print(f"❌ Error processing message: {e}")
            # Clean up file if download succeeded but processing failed
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except:
                    pass
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