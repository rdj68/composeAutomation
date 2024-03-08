import discord
from discord.ext import commands
from app.controllers.dockerCompose import restart_docker_compose
import os

description = '''A bot to restart the Docker Compose services when a request is made.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.command(name='restart')
async def restart(ctx):
    guild_name = os.environ.get('GUILD_NAME')
    success_info = restart_docker_compose(os.environ.get('DOCKER_COMPOSE_PATH'))
    await send_message_to_default_channel(guild_name, success_info)
    
# The login command sets the GUILD_NAME environment variable to the name of the guild (server) where the bot will operate.
@bot.command(name='login')
async def login(ctx, login_pass: str):
    if login_pass == os.environ.get('LOGIN_PASS'):
        guild_name = ctx.guild.name
        os.environ['GUILD_NAME'] = guild_name
        await ctx.send(f'Logged in as {guild_name}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

async def send_message_to_default_channel(guild_name: str, message_content: str):
    # Ensure that the bot is a commands.Bot instance
    if not isinstance(bot, commands.Bot):
        raise ValueError("Invalid bot instance. Must be a commands.Bot.")
    print("send_message_to_default_channel")

    # Fetch the guild (server) by name
    guild = discord.utils.get(bot.guilds, name=guild_name)

    if guild:
        # Fetch or create the channel named "dockercomposeautomated"
        channel_name = 'docker-compose-automated'
        channel = discord.utils.get(guild.channels, name=channel_name)

        if not channel:
            # If the channel doesn't exist, create it
            channel = await guild.create_text_channel(channel_name)
            print(f'Channel "{channel_name}" created in guild "{guild_name}"')

        try:
            # Send the message to the channel
            await channel.send(message_content)
            print(f'Message sent to channel "{channel_name}" in guild "{guild_name}"')
        except discord.HTTPException as e:
            print(f'Error sending message to channel "{channel_name}" in guild "{guild_name}": {e}')
    else:
        print(f'Guild with name "{guild_name}" not found')

def run_bot(token: str):
    bot.start(token)

if __name__ == '__main__':
    print("run app.py")