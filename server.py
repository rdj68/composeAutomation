from fastapi import FastAPI, HTTPException
import hmac
import hashlib
import os
from schemas.webhook import WebhookResponse
from schemas.restart import RestartResponse, RestartReq
from controllers.dockerCompose import update_docker_compose, restart_docker_compose
from dotenv import load_dotenv


app = FastAPI()

# Load env file and get the secret from the environment variable
load_dotenv()
SECRET = os.environ.get('WEBHOOK_SECRET')
RESTART_SECRET = os.environ.get('RESTART_SECRET')
DOCKER_COMPOSE_PATH = os.environ.get('DOCKER_COMPOSE_PATH')

@app.post('/webhook', response_model=WebhookResponse)
async def webhook(request_data: dict):
    # Validate GitHub webhook secret
    if not is_valid_signature(request_data, request_data.headers.get('X-Hub-Signature')):
        raise HTTPException(status_code=403, detail='Invalid signature')

    # Check if the event is a push to the main branch
    if is_main_branch_push(request_data):
        commit_hash_after = request_data['after']  # Extract commit hash
        commit_hash_before = request_data['before']  # Extract commit hash

        #Update Docker Compose file with the commit hash
        update_docker_compose(commit_hash_after, commit_hash_before)
        return WebhookResponse(message='Docker Compose file updated successfully')

    # Return a response using the Pydantic model
    return WebhookResponse(message='No action taken')

@app.post('/restart', response_model=RestartResponse)
async def restart(req: RestartReq):
    # Check if the secret is correct
    if req.secret != RESTART_SECRET:
        raise HTTPException(status_code=403, detail='Invalid secret')

    # Restart the Docker Compose services
    restart_docker_compose()
    return RestartResponse(message='Docker Compose services restarted successfully', success=True)

def is_main_branch_push(payload):
    return payload['ref'] == 'refs/heads/main' and payload['after']

def is_valid_signature(data, signature):
    if not signature:
        return False

    hmac_digest = hmac.new(bytes(SECRET, 'utf-8'), data, hashlib.sha1).hexdigest()
    expected_signature = f"sha1={hmac_digest}"

    return hmac.compare_digest(signature, expected_signature)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=5000)