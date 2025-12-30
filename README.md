# Telegram-Discord Relay Bot

A Python bot that relays messages from Telegram groups/channels to a Discord channel with @everyone mentions. Perfect for bridging communication between Telegram and Discord communities.

## Features

- 📨 Automatically forwards all messages from Telegram to Discord
- 👥 Preserves sender information (username and chat name)
- 🔔 Includes @everyone mentions in Discord for important notifications
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
