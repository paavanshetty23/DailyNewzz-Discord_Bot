
# DailyNewzz Discord Bot

**DailyNewzz** is a Discord bot that delivers personalized daily news updates directly to users through direct messages (DMs). Users can select their preferred news genre, and the bot fetches top headlines from NewsAPI based on the selection.

## Features

- Select from various news genres such as Technology, Sports, Entertainment, Business, Health, Science, and General.
- Fetch and receive the latest news headlines for the selected genre.
- Reset the genre preferences and select a new genre.
- All interactions are done through direct messages, ensuring a personalized experience.

## Setup and Installation

### Prerequisites

- Python 3.8+
- A Discord bot token (Create a bot on the [Discord Developer Portal](https://discord.com/developers/applications)).
- A NewsAPI key (Sign up at [NewsAPI](https://newsapi.org) to get your free API key).

### Installation

1. Clone the repository or download the source code.
2. Install the required dependencies using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the project root and add the following keys:

    ```env
    DISCORD_TOKEN=your_discord_bot_token
    NEWS_API_KEY=your_newsapi_key
    ```

4. Run the bot:

    ```bash
    python bot.py
    ```

## Commands

| Command       | Description                                                      |
|---------------|------------------------------------------------------------------|
| `hi`          | Start the bot interaction and choose your preferred news genre.  |
| `!get_news`   | Fetch the latest news articles for your selected genre.          |
| `!reset`      | Reset your genre preference and select a new genre.              |
| `!help`       | Display a help message with available commands.                  |

### Genre Selection

Upon sending a `hi` message to the bot, you will be prompted to choose a news genre from a list of available genres. You can either type the number or name of the genre. After selecting, you can use the `!get_news` command to fetch the latest news.

### Fetching News

After selecting a genre, you can use the `!get_news` command to fetch top news headlines from that genre. The bot will return a list of 5 top headlines along with a short description and a link to read the full article.

### Resetting Preferences

Use the `!reset` command to reset your genre preferences if you'd like to change the genre.

## Environment Variables

- `DISCORD_TOKEN`: Your Discord bot token.
- `NEWS_API_KEY`: Your API key from NewsAPI for fetching news articles.

## Built With

- [discord.py](https://discordpy.readthedocs.io/) - Python library for interacting with the Discord API.
- [NewsAPI](https://newsapi.org/) - News API for fetching top news headlines.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

This README file provides clear instructions for setting up and running the DailyNewzz Discord bot, along with an explanation of available commands and features.
