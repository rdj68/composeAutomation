import subprocess
import flock 

def update_docker_compose(commit_hash_after, commit_hash_before, docker_compose_path):
    try:
        # Read the current Docker Compose file content
        with open(docker_compose_path, 'r') as f:
            docker_compose_content = f.read()

        # Replace the commit hash_before with commit_hash_after
        updated_content = docker_compose_content.replace(commit_hash_before, commit_hash_after)

        # Write the updated content back to the Docker Compose file
        with flock.Flock(docker_compose_path, flock.LOCK_EX):
            with open(docker_compose_path, 'w') as f:
                f.write(updated_content)
    except Exception as e:
        print(f'Error updating Docker Compose file: {e}')
        
def restart_docker_compose(docker_compose_path: str) -> str:
    try:
        # Restart the Docker Compose services and capture the logs
        completed_process = subprocess.run(['docker', 'compose', '-f', docker_compose_path, 'up', '-d'], capture_output=True, text=True, check=True)

        # Check if the Docker Compose services restarted properly
        if completed_process.returncode == 0:
            success_message = "Docker Compose services restarted successfully."
            logs = completed_process.stdout
            # You can include 'logs' in the returned string if needed
            return success_message
        else:
            error_message = f"Error restarting Docker Compose. Exit code: {completed_process.returncode}\n"
            error_message += f"Error output: {completed_process.stderr}"
            return error_message
    except subprocess.CalledProcessError as e:
        return f'Error restarting Docker Compose: {e}'     