# This example requires the 'members' and 'message_content' privileged intents to function.

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
    print(ctx.guild.name)
    success_info = restart_docker_compose(os.environ.get('DOCKER_COMPOSE_PATH'))
    send_message_to_default_channel(os.environ.get('GUILD_NAME'), success_info)


async def send_message_to_default_channel(guild_name: str, message_content: str):
    # Ensure that the bot is a commands.Bot instance
    if not isinstance(bot, commands.Bot):
        raise ValueError("Invalid bot instance. Must be a commands.Bot.")

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')

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

            # Send the message to the channel
            await channel.send(message_content)
            print(f'Message sent to channel "{channel_name}" in guild "{guild_name}"')
        else:
            print(f'Guild with name "{guild_name}" not found')


def run_bot(token: str):
    bot.start(token)

if __name__ == '__main__':
    print("run app.py")