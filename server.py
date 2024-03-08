from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
import hmac
import hashlib
import os
from app.schemas.webhook import WebhookResponse
from app.controllers.dockerCompose import update_docker_compose
from starlette.requests import Request
from dotenv import load_dotenv
import asyncio
from app.discordBot.discord_bot import bot, send_message_to_default_channel
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Discord bot")
    load_dotenv()
    
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    asyncio.create_task(bot.start(BOT_TOKEN))
    yield
    print("Stopping Discord bot")

app = FastAPI(lifespan=lifespan)

SECRET = os.environ.get('WEBHOOK_SECRET')
DOCKER_COMPOSE_PATH = os.environ.get('DOCKER_COMPOSE_PATH')
GUILD_NAME = os.environ.get('GUILD_NAME')

@app.post('/webhook')
async def webhook(request: Request):
    # Get the GitHub webhook signature from the headers
    signature = request.headers.get('X-Hub-Signature')
    
    # Read the request body
    body = await request.body()
    
    # Validate the GitHub webhook signature
    if not is_valid_signature(body, signature):
        raise HTTPException(status_code=403, detail='Invalid signature')

    # Parse the JSON payload directly
    request_data = await request.json()

    # Check if the event is a push to the main branch
    if is_main_branch_push(request_data):
        commit_hash_after = request_data['after']
        commit_hash_before = request_data['before']

        # Update Docker Compose file with the commit hash
        update_docker_compose(commit_hash_after, commit_hash_before)

        send_message_to_default_channel(GUILD_NAME)
        return {'message': 'Docker Compose file updated successfully'}

    return {'message': 'No action taken'}


def is_main_branch_push(payload):
    return (payload['ref'] == 'refs/heads/main' or payload['ref'] == 'refs/heads/master') and payload['after']

def is_valid_signature(data, signature):
    if not signature:
        return False

    # Calculate HMAC digest
    hmac_digest = hmac.new(bytes(SECRET, 'utf-8'), data, hashlib.sha1).hexdigest()
    expected_signature = f"sha1={hmac_digest}"

    return hmac.compare_digest(signature, expected_signature)

if __name__ == '__main__':
    uvicorn.run(app, port=8080)