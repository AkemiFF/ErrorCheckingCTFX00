import docker
from docker.errors import DockerException


class DockerManager:
    def __init__(self, base_path="./docker_challenges"):
        """
        Initialize the DockerManager with the path to the challenges.
        :param base_path: Path where Docker challenge folders are located.
        """
        self.client = docker.from_env()
        self.base_path = base_path

    def start_container(self, challenge_name, port):
        """
        Start a container for a specific challenge.
        :param challenge_name: Name of the challenge folder.
        :param port: Port to expose for the container.
        :return: Container object or None if failed.
        """
        try:
            container = self.client.containers.run(
                image=f"{challenge_name}_image",
                detach=True,
                ports={"80/tcp": port},
                name=f"{challenge_name}_container"
            )
            return container
        except DockerException as e:
            print(f"Error starting container for {challenge_name}: {e}")
            return None

    def stop_container(self, challenge_name):
        """
        Stop and remove a container by its challenge name.
        :param challenge_name: Name of the challenge folder.
        """
        try:
            container = self.client.containers.get(f"{challenge_name}_container")
            container.stop()
            container.remove()
            print(f"Container for {challenge_name} stopped and removed.")
        except DockerException as e:
            print(f"Error stopping container for {challenge_name}: {e}")

    def restart_container(self, challenge_name, port):
        """
        Restart a container for a specific challenge.
        :param challenge_name: Name of the challenge folder.
        :param port: Port to expose for the container.
        :return: Updated container object or None if failed.
        """
        self.stop_container(challenge_name)
        return self.start_container(challenge_name, port)

    def build_image(self, challenge_name, level):
        """
        Build a Docker image for a specific challenge.
        :param challenge_name: Name of the challenge folder.
        :param level: Difficulty level (beginner, intermediate, advanced).
        """
        try:
            path = f"{self.base_path}/{level}/{challenge_name}"
            self.client.images.build(path=path, tag=f"{challenge_name}_image")
            print(f"Image for {challenge_name} built successfully.")
        except DockerException as e:
            print(f"Error building image for {challenge_name}: {e}")

    def list_containers(self):
        """
        List all active containers.
        :return: List of container details.
        """
        try:
            containers = self.client.containers.list()
            return [
                {
                    "id": container.id,
                    "name": container.name,
                    "status": container.status,
                    "ports": container.attrs['NetworkSettings']['Ports']
                } for container in containers
            ]
        except DockerException as e:
            print(f"Error listing containers: {e}")
            return []

    def update_flag(self, challenge_name, new_flag):
        """
        Update the flag for a running container without rebuilding.
        :param challenge_name: Name of the challenge folder.
        :param new_flag: New flag value.
        """
        try:
            container = self.client.containers.get(f"{challenge_name}_container")
            exec_result = container.exec_run(["/bin/bash", "-c", f"echo '{new_flag}' > /flag.txt"])
            print(f"Flag updated for {challenge_name}: {exec_result.output}")
        except DockerException as e:
            print(f"Error updating flag for {challenge_name}: {e}")

if __name__ == "__main__":
    manager = DockerManager()

    # Example usage
    manager.build_image("example_challenge", "beginner")
    container = manager.start_container("example_challenge", 8080)
    if container:
        print(f"Started container: {container.name}")
    manager.update_flag("example_challenge", "new_flag{example}")
    manager.list_containers()
    manager.stop_container("example_challenge")