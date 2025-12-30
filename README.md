# Telegram-Discord Relay Bot

A Python bot that relays messages from Telegram groups/channels to a Discord channel with @everyone mentions. Perfect for bridging communication between Telegram and Discord communities.

## Features

- 📨 Automatically forwards all messages from Telegram to Discord
- 📷 Supports photos, videos, and documents with captions
- 🔗 Preserves links in text and media captions
- 👥 Preserves sender information (username and chat name)
- 🔔 Customizable role mentions using Role ID (defaults to @everyone)
- 🔄 Real-time message relay
- 🛡️ Environment variable configuration for security

## How It Works

The bot runs two bots simultaneously:
1. **Telegram Bot** - Listens for messages in Telegram groups/channels
2. **Discord Bot** - Forwards received messages to a specified Discord channel

Messages are formatted as: `@everyone **[Telegram Group Name]** Username: Message text`

## Prerequisites

- Python 3.8 or higher
- A Telegram Bot Token
- A Discord Bot Token
- Discord Channel ID where messages will be sent

## Installation

1. **Clone or download this repository**

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** in the project directory with the following content:
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   DISCORD_BOT_TOKEN=your_discord_bot_token_here
   DISCORD_CHANNEL_ID=your_discord_channel_id_here
   # DISCORD_ROLE_ID=your_role_id_here  # Optional: defaults to @everyone
   ```

## Configuration Setup

### 1. Create a Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token provided by BotFather
5. Add your bot to the Telegram group you want to monitor
6. Make sure the bot has permission to read messages

### 2. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Under the bot's token section, click "Reset Token" and copy the token
5. Enable "Message Content Intent" under Privileged Gateway Intents
6. Go to "OAuth2" > "URL Generator"
7. Select scopes: `bot`
8. Select bot permissions: `Send Messages`, `Read Messages/View Channels`
9. Copy the generated URL and open it in your browser to invite the bot to your Discord server

### 3. Get Discord Channel ID

1. Enable Developer Mode in Discord (User Settings > Advanced > Developer Mode)
2. Right-click on the channel where you want messages to be sent
3. Click "Copy Channel ID"

### 4. Update `.env` file

Paste all the tokens and IDs into your `.env` file:
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
DISCORD_BOT_TOKEN=MTIzNDU2Nzg5MDEyMzQ1Njc4OQ.GaBcDe.FgHiJkLmNoPqRsTuVwXyZ
DISCORD_CHANNEL_ID=123456789012345678
```

#### Optional: Customize Discord Role Mention

By default, the bot uses `@everyone` to mention all users. You can customize this to mention a specific role using its Role ID:

**How to get a Role ID:**
1. Enable Developer Mode in Discord (User Settings > Advanced > Developer Mode)
2. Go to Server Settings > Roles
3. Right-click on the role you want to mention (e.g., "groomsmen")
4. Click "Copy Role ID"

**Add to your `.env` file:**
```env
# To mention a specific role by ID
DISCORD_ROLE_ID=1455619074427064380

# To use default @everyone, simply don't set DISCORD_ROLE_ID or comment it out:
# DISCORD_ROLE_ID=
```

**Example:** If you set `DISCORD_ROLE_ID=1455619074427064380`, messages will appear as:
- `<@&1455619074427064380> **[Telegram Group]** Username: Message text`
- This will properly ping everyone with that role in Discord!

## Usage

Run the bot with:
```bash
python relay_bot.py
```

You should see output like:
```
🚀 Starting bots...
🤖 Starting Telegram bot...
✅ Discord bot logged in as YourBot#1234
✅ Discord bot ID: 123456789
✅ Found Discord channel: general (ID: 123456789)
✅ Ready to relay messages!
✅ Both bots are running!
💬 Send a message in your Telegram group to test!
Press Ctrl+C to stop
```

To stop the bot, press `Ctrl+C`.

## Deploying to Railway.app

Railway.app provides free hosting for bots. Follow these steps to deploy:

### 1. Prepare Your Repository

Ensure your repository has these files:
- `relay_bot.py` - Your bot script
- `requirements.txt` - Python dependencies
- `Procfile` - Tells Railway how to run your bot
- `runtime.txt` - Specifies Python version

### 2. Deploy to Railway

1. Go to [Railway.app](https://railway.app) and sign in with GitHub
2. Click "New Project" > "Deploy from GitHub repo"
3. Select your `telegram-discord-relay` repository
4. Railway will automatically detect it's a Python project

### 3. Configure Environment Variables

In Railway dashboard:
1. Go to your project > "Variables" tab
2. Add the following environment variables:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
DISCORD_BOT_TOKEN=your_discord_bot_token_here
DISCORD_CHANNEL_ID=your_discord_channel_id_here
DISCORD_ROLE_ID=your_role_id_here
```

**Important:** Do NOT include quotes around the values.

### 4. Deploy

1. Railway will automatically deploy your bot
2. Check the "Deployments" tab to see logs
3. You should see the same startup messages as when running locally

### Notes for Railway Deployment

- **No .env file needed** - Railway uses environment variables directly
- **Always-on**: Railway keeps your bot running 24/7
- **Logs**: View real-time logs in the Railway dashboard
- **Free tier**: Includes 500 hours/month (enough for one bot running continuously)
- **Automatic redeploys**: Push to GitHub to automatically redeploy

### Troubleshooting Railway Deployment

**Bot not starting:**
- Check logs in Railway dashboard for error messages
- Verify all environment variables are set correctly
- Ensure `Procfile` contains: `worker: python relay_bot.py`

**File download errors:**
- Railway has `/tmp` directory that works for temporary files
- The bot uses `tempfile.gettempdir()` which works on Railway's Linux servers

## Troubleshooting

### Bot doesn't relay messages
- Ensure the Telegram bot is added to your group and has permission to read messages
- Check that the Discord bot has permission to send messages in the target channel
- Verify all tokens and IDs in the `.env` file are correct

### "Could not find channel" error
- Double-check your Discord Channel ID
- Ensure the Discord bot has been invited to your server
- Verify the bot has access to view the channel

### Environment variable errors
- Make sure your `.env` file is in the same directory as `relay_bot.py`
- Check that there are no extra spaces or quotes around the values
- Ensure the file is named exactly `.env` (not `.env.txt`)

## Security Notes

- **Never commit your `.env` file** to version control
- Keep your bot tokens private
- Regenerate tokens if they are accidentally exposed

## License

This project is open source and available for personal and educational use.
