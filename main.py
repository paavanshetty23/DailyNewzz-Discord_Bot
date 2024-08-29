from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import requests

# Load environment variables from the .env file
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')


# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True  # Ensure the bot can receive DM messages

# Initialize the bot
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# In-memory storage for user preferences and interaction states
user_preferences = {}

# List of available genres
GENRES = ['Technology', 'Sports', 'Entertainment', 'Business', 'Health', 'Science', 'General']

@bot.event
async def on_ready():
    """Triggered when the bot is connected and ready."""
    print(f'✅ Bot is online as {bot.user}')

@bot.event
async def on_message(message):
    """Handle incoming messages, including greetings and genre selection."""
    if message.author == bot.user:
        return  # Ignore messages from the bot itself

    # Check if the message is a DM to the bot
    if isinstance(message.channel, discord.DMChannel):
        user_id = message.author.id
        content = message.content.strip().lower()

        # Start interaction with 'hi'
        if content == 'hi':
            await send_genre_selection(message.author)
            return

        # Handle genre selection
        elif user_id in user_preferences and not user_preferences[user_id]:
            selected_genre = parse_genre_selection(content)
            if selected_genre:
                user_preferences[user_id] = selected_genre
                await message.author.send(f'✅ You have selected: **{selected_genre}**.\nYou can now use `!get_news` to fetch the latest news.')
            else:
                await message.author.send("❌ Invalid selection. Please choose a genre by number or name from the list provided.")
            return

    # Process commands after handling on_message events
    await bot.process_commands(message)

async def send_genre_selection(user):
    """Sends a message to the user to select a genre."""
    user_preferences[user.id] = None  # Initialize user preference
    genre_list = '\n'.join([f"{idx + 1}. {genre}" for idx, genre in enumerate(GENRES)])
    message = (
        "👋 **Hello! Welcome to DailyNewzz Bot.**\n"
        "Please choose a genre from the following list by typing the **number** or **name**:\n\n"
        f"{genre_list}"
    )
    await user.send(message)

def parse_genre_selection(selection):
    """Parses user input and returns the corresponding genre if valid."""
    if selection.isdigit():
        index = int(selection) - 1
        if 0 <= index < len(GENRES):
            return GENRES[index]
    else:
        selection_capitalized = selection.capitalize()
        if selection_capitalized in GENRES:
            return selection_capitalized
    return None

@bot.command(name='get_news')
async def get_news(ctx):
    """Fetches and sends news articles based on the user's selected genre."""
    user_id = ctx.author.id

    # Check if command is used in DM
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("❌ Please use this command in a **direct message** with the bot.")
        return

    genre = user_preferences.get(user_id)
    if not genre:
        await ctx.send("❌ You haven't selected a genre yet. Please say 'hi' to start the setup.")
        return

    await ctx.send(f"🔄 Fetching latest news for **{genre}**...")
    news = fetch_news(genre)

    # Split message if it exceeds 2000 characters
    if len(news) > 2000:
        chunks = [news[i:i + 2000] for i in range(0, len(news), 2000)]
        for chunk in chunks:
            await ctx.send(chunk)
    else:
        await ctx.send(news)

@bot.command(name='reset')
async def reset(ctx):
    """Resets the user's genre preference."""
    user_id = ctx.author.id

    # Check if command is used in DM
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("❌ Please use this command in a **direct message** with the bot.")
        return

    user_preferences.pop(user_id, None)
    await ctx.send("🔄 Your preferences have been reset.")
    await send_genre_selection(ctx.author)


def fetch_news(genre):
    url = (
        f'https://newsapi.org/v2/top-headlines?'
        f'category={genre.lower()}&'
        f'country=us&'
        f'apiKey={NEWS_API_KEY}'
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get('status') != 'ok' or not data.get('articles'):
            return "❌ Sorry, I couldn't find any news articles for that genre at the moment."

        articles = data['articles'][:5]
        news_list = []

        for idx, article in enumerate(articles):
            title = article['title']
            description = article.get('description') or article.get('content') or 'No description available.'
            description = description.split('.')[0][:150] if description else 'No description available.'
            url = article['url']
            news_item = f"**{idx + 1}. {title}**\n{description}...\n[Read more]({url})"
            news_list.append(news_item)

        message_content = "\n\n".join(news_list)
        if len(message_content) > 2000:
            message_content = message_content[:1997] + "..."

        return f"📰 **Top news articles in {genre}:**\n\n{message_content}"

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return "❌ There was an error fetching the news. Please try again later."


@bot.command(name='help')
async def help_command(ctx):
    """Provides information about bot commands."""
    help_message = (
        "📚 **DailyNewzz Bot Commands:**\n\n"
        "**hi** - Start the setup and choose your preferred news genre.\n"
        "**!get_news** - Fetch the latest news articles for your selected genre.\n"
        "**!reset** - Reset your genre preference and choose again.\n"
        "**!help** - Display this help message."
    )
    await ctx.send(help_message)

# Run the bot
if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)
