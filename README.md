# League Lookup Discord Bot

A Discord bot that provides League of Legends player profile information directly in your Discord server. Get detailed statistics, rankings, champion masteries, and current game status for any League of Legends player.

## Features

- **Player Profile Lookup**: Get comprehensive player information including level, rank, and mastery score
- **Ranked Statistics**: View Solo/Duo and Flex queue rankings with LP, wins, losses, and winrate
- **Champion Mastery**: Display top 3 most played champions with mastery points
- **Live Game Status**: Check if a player is currently in a game with game mode, map, duration, and champion
- **Interactive Embeds**: Beautiful Discord embeds with progressive loading for better user experience

## Prerequisites

Before running the bot, you'll need:

1. **Python 3.7+** installed on your system
2. **Riot Games API Key** - Get one from the [Riot Developer Portal](https://developer.riotgames.com/)
3. **Discord Bot Token** - Create a bot application in the [Discord Developer Portal](https://discord.com/developers/applications)

## Installation

1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install discord.py requests
   ```

3. Create a `credentials.json` file in the project directory:
   ```json
   {
       "api_key": "YOUR_RIOT_API_KEY_HERE",
       "bot_token": "YOUR_DISCORD_BOT_TOKEN_HERE"
   }
   ```

4. Replace the placeholder values with your actual API keys:
   - `YOUR_RIOT_API_KEY_HERE`: Your Riot Games API key
   - `YOUR_DISCORD_BOT_TOKEN_HERE`: Your Discord bot token

## Discord Bot Setup

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Navigate to the "Bot" section
4. Create a bot and copy the token
5. Under "Privileged Gateway Intents", enable:
   - Message Content Intent
   - Server Members Intent (if needed)
6. Generate an invite link with the following permissions:
   - Send Messages
   - Use Slash Commands
   - Embed Links
   - Read Message History

## Usage

### Starting the Bot

Run the bot with:
```bash
python profilebot.py
```

### Discord Commands

- **`!profile <summoner_name>#<tag>`**: Get detailed profile information for a League of Legends player

#### Examples:
```
!profile Faker#KR1
!profile RiotGames#NA1
!profile YourSummonerName#EUW
```

### Bot Response

The bot will display:
- **General Information**: Player level, rank, and mastery score
- **Ranked Solo/Duo**: Tier, LP, wins, losses, and winrate
- **Ranked Flex**: Tier, LP, wins, losses, and winrate
- **Top 3 Champions**: Most played champions with mastery points
- **Player Status**: Current game information or offline status

## Supported Regions

The bot currently supports the EUW (Europe West) region. To modify for other regions, update the API endpoints in the code:

- **Europe**: `europe.api.riotgames.com`
- **Americas**: `americas.api.riotgames.com`
- **Asia**: `asia.api.riotgames.com`

Regional server endpoints:
- **EUW**: `euw1.api.riotgames.com`
- **NA**: `na1.api.riotgames.com`
- **KR**: `kr.api.riotgames.com`
- And more...

## File Structure

```
LeagueLookup/
├── profilebot.py        # Main bot script
├── credentials.json     # API keys and tokens (not included in repo)
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore file
```

## API Rate Limits

- **Personal API Key**: 100 requests every 2 minutes
- **Production API Key**: Higher limits available upon request
- The bot includes basic error handling for API failures

## Security Notes

⚠️ **Important Security Considerations:**

1. **Never commit** `credentials.json` to version control
2. Add `credentials.json` to your `.gitignore` file
3. Keep your API keys and bot token secure
4. Riot API keys may expire and need renewal
5. Don't share your credentials with others

## Troubleshooting

### Common Issues:

1. **"Impossible de trouver le profil"**: 
   - Check if the summoner name and tag are correct
   - Ensure the player exists in the EUW region

2. **API Key Errors**:
   - Verify your Riot API key is valid and not expired
   - Check if you've exceeded rate limits

3. **Bot Not Responding**:
   - Ensure the bot has proper permissions in your Discord server
   - Check that the bot token is correct
   - Verify the bot is online and running

4. **Module Import Errors**:
   - Install required packages: `pip install -r requirements.txt`
   - Or install manually: `pip install discord.py requests`

## Contributing

Feel free to submit issues and enhancement requests! Some potential improvements:

- Support for multiple regions
- Additional statistics (match history, detailed champion stats)
- Slash commands support
- Database integration for user preferences
- More detailed error handling

## License

This project is for educational purposes. Please respect Riot Games' API Terms of Service and Discord's Terms of Service when using this bot.

## Disclaimer

This project is not affiliated with Riot Games or Discord. League of Legends is a trademark of Riot Games, Inc.
