from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse
import subprocess
import hmac
import hashlib
from pydantic import BaseModel

app = FastAPI()

# Replace 'your_secret' with the secret you set in the GitHub webhook configuration
SECRET = 'your_secret'
DOCKER_COMPOSE_PATH = '/path/to/your/docker-compose-file.yml'

# Create a Pydantic model for the response
class WebhookResponse(BaseModel):
    message: str

@app.post('/webhook', response_model=WebhookResponse)
async def webhook(request_data: dict):
    # Validate GitHub webhook secret
    if not is_valid_signature(request_data, request_data.headers.get('X-Hub-Signature')):
        raise HTTPException(status_code=403, detail='Invalid signature')

    # Check if the event is a push to the main branch
    if is_main_branch_push(request_data):
        commit_hash = request_data['after']  # Extract commit hash

        # Update Docker Compose file with the commit hash
        # update_docker_compose(commit_hash)

        # Return a response using the Pydantic model
        return WebhookResponse(message='Docker Compose file updated successfully')

    # Return a response using the Pydantic model
    return WebhookResponse(message='No action taken')


def is_main_branch_push(payload):
    return payload['ref'] == 'refs/heads/main' and payload['after']

def is_valid_signature(data, signature):
    if not signature:
        return False

    hmac_digest = hmac.new(bytes(SECRET, 'utf-8'), data, hashlib.sha1).hexdigest()
    expected_signature = f"sha1={hmac_digest}"

    return hmac.compare_digest(signature, expected_signature)

# def update_docker_compose(commit_hash):
#     try:
#         # Read the current Docker Compose file content
#         with open(DOCKER_COMPOSE_PATH, 'r') as f:
#             docker_compose_content = f.read()

#         # Append the commit hash to a specific location in the file
#         updated_content = docker_compose_content + f'\n# Updated commit hash: {commit_hash}'

#         # Write the updated content back to the Docker Compose file
#         with open(DOCKER_COMPOSE_PATH, 'w') as f:
#             f.write(updated_content)

#         # Commit and push the changes to the repository
#         subprocess.run(['git', 'add', DOCKER_COMPOSE_PATH])
#         subprocess.run(['git', 'commit', '-m', 'Update Docker Compose with latest commit hash'])
#         subprocess.run(['git', 'push', 'origin', 'main'])

#     except Exception as e:
#         print(f'Error updating Docker Compose file: {e}')

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=5000)
