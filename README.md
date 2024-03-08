# compose-automation

## Overview

`composeautomation` is a project designed to automate Docker Compose operations using GitHub webhooks and a Discord bot. By integrating with GitHub webhooks, the project allows for seamless updates to a Docker Compose file upon receiving a webhook event. Additionally, it sends informative messages to a specified Discord server channel to keep the team informed about the changes.

## Features

- **GitHub Webhooks Integration:** The project exposes an endpoint at `/webhook` to receive GitHub webhook events. When a webhook request is received, the Docker Compose file is updated accordingly.

- **Discord Bot Integration:** The Discord bot sends messages to a specified channel in the configured Discord server, providing real-time updates on Docker Compose changes.

- **FastAPI Server:** The server is built using FastAPI, a modern, fast, web framework for building APIs with Python 3.7+.

## Configuration

To use `dockercomposeautomation`, you need to set up the following environment variables:

- `BOT_TOKEN`: Discord bot token for authentication.
- `DOCKER_COMPOSE_PATH`: Path to the Docker Compose file that will be updated.
- `GUILD_NAME`: Name of the Discord server (guild) where the bot will operate.
- `WEBHOOK_SECRET`: Secret key for securing the GitHub webhook endpoint.

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/dockercomposeautomation.git
    cd dockercomposeautomation
    ```

2. Set up the required environment variables in your environment or through a configuration file.

3. Run the FastAPI server:

    ```bash
    uvicorn server:app --reload
    ```

4. **Configure Discord Bot Permissions:**
   - Make sure the Discord bot has the following permissions in the Discord server (guild) where it operates:
      - Read Messages (`READ_MESSAGES`)
      - Send Messages (`SEND_MESSAGES`)
      - View Channel (`VIEW_CHANNEL`)
      - Manage Channels (`MANAGE_CHANNELS`)
      - Read Message History (`READ_MESSAGE_HISTORY`)
      - Use Slash Commands (`USE_SLASH_COMMANDS`)

5. Configure your GitHub repository to send webhook events to the `/webhook` endpoint.

6. The Discord bot will send messages to the specified channel in the configured Discord server upon receiving webhook events.

## Contributing

Feel free to contribute to the project by opening issues or submitting pull requests. Your feedback and contributions are highly appreciated.

## License

This project is licensed under the [Apache License](LICENSE). See the LICENSE file for details.
