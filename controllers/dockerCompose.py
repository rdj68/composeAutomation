import subprocess

def update_docker_compose(commit_hash_after, commit_hash_before, docker_compose_path):
    try:
        # Read the current Docker Compose file content
        with open(docker_compose_path, 'r') as f:
            docker_compose_content = f.read()

        # Replace the commit hash_before with commit_hash_after
        updated_content = docker_compose_content.replace(commit_hash_before, commit_hash_after)

        # Write the updated content back to the Docker Compose file
        with open(docker_compose_path, 'w') as f:
            f.write(updated_content)
    except Exception as e:
        print(f'Error updating Docker Compose file: {e}')
        
def restart_docker_compose(docker_compose_path):
    try:
        # Restart the Docker Compose services
        subprocess.run(['docker', 'compose', '-f', docker_compose_path, 'up', '-d'], check=True)
    except Exception as e:
        print(f'Error restarting Docker Compose: {e}')
        