from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Header, Request
import hmac
import hashlib
import os
from app.schemas.webhook import WebhookResponse
from app.controllers.dockerCompose import update_docker_compose
from dotenv import load_dotenv
import asyncio
from app.discordBot.discord_bot import bot, send_message_to_default_channel
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Discord bot")
    load_dotenv()
    
    global SECRET 
    SECRET = os.environ.get('WEBHOOK_SECRET')
    global DOCKER_COMPOSE_PATH
    DOCKER_COMPOSE_PATH = os.environ.get('DOCKER_COMPOSE_PATH')
    global BOT_TOKEN
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    
    asyncio.create_task(bot.start(BOT_TOKEN))
    yield
    print("Stopping Discord bot")

app = FastAPI(lifespan=lifespan)



@app.post('/webhook')
async def webhook(request: Request,
    x_github_event: str = Header(...),
    x_hub_signature: str = Header(...)):
    
    if x_github_event == 'ping':
        return {'message': 'GitHub Webhook received successfully'}
        
    if x_github_event != 'push':
        raise HTTPException(status_code=400, detail='Invalid event type')


    # Decode the URL-encoded payload
    body = await request.body()
    payload = await request.json()



    # Validate the GitHub webhook signature
    # if x_hub_signature and not is_valid_github_signature(body, x_hub_signature):
        # raise HTTPException(status_code=403, detail='Invalid signature')

    # Check if the event is a push to the main branch
    if is_main_branch_push(payload):
        commit_hash_after = payload['after']
        commit_hash_before = payload['before']

        # Update Docker Compose file with the commit hash
        update_docker_compose(commit_hash_after, commit_hash_before, DOCKER_COMPOSE_PATH)

        await send_message_to_default_channel(os.environ.get('GUILD_NAME'), generate_notification_message(payload))
        return {'message': 'Docker Compose file updated successfully'}
    else:
        return {'message': 'No action required'}
    
    
def is_main_branch_push(payload):
    default_branch = payload['repository']['default_branch']
    return "ref" in payload and  payload['ref'] == f'refs/heads/{default_branch}'

def is_valid_github_signature(
    body: bytes,
    received_signature: str
) -> bool:
    # Convert the secret to bytes (if it's not already)
    secret_bytes = SECRET.encode('utf-8')

    # Ensure the signature is in the expected format
    if not received_signature.startswith("sha1="):
        return False

    # Extract the actual hash value from the signature
    expected_hash = received_signature[5:]

    # Calculate the HMAC digest using the provided secret
    hmac_digest = hmac.new(secret_bytes, body, hashlib.sha1).hexdigest()

    # Compare the calculated hash with the expected hash
    return hmac.compare_digest(expected_hash, hmac_digest)

def generate_notification_message(payload):
    try:
        repository_name = payload['repository']['name']
        action_type = "Push" if 'commits' in payload else "Pull Request"
        branch = payload['ref'].split('/')[-1]
        commit_message = payload['head_commit']['message']
        commit_url = payload['head_commit']['url']
        sender_username = payload['sender']['login']

        message = f"New {action_type} in repository '{repository_name}':\n"
        message += f"Branch: {branch}\n"
        message += f"Commit Message: {commit_message}\n"
        message += f"Commit URL: {commit_url}\n"
        message += f"Triggered by: {sender_username}"

        return message
    except Exception as e:
        return f"Error generating notification: {str(e)}"

if __name__ == '__main__':
    uvicorn.run(app, port=8080)