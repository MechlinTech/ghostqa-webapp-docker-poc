import docker

def initialize_docker_client(remote_host_ip, port):
    return docker.DockerClient(base_url=f"tcp://{remote_host_ip}:{port}")

def check_remote_docker_listing(remote_host_ip, port):
    client = initialize_docker_client(remote_host_ip, port)
    containers = client.containers.list(all=True)
    return containers

def get_file_from_remote_docker_daemon(remote_host_ip, port, path):
    client = initialize_docker_client(remote_host_ip, port)
    containers = check_remote_docker_listing(remote_host_ip, port)
    container_id = containers[0].id if containers else None
    if container_id:
        container = client.containers.get(container_id)
        print(container)
        # command = "ls -lR /" #["ls", "-lR", "/"] #Recusively list all the files starting from root
        command = f"ls -l {path}"
        output = container.exec_run(command)
        files = output.output.decode('utf-8').split('\n')
        return [file.split()[-1] for file in files[1:-1]]
    else:
        print("No containers found.")

result = get_file_from_remote_docker_daemon("15.207.97.170", "2375", "bin")
print(result)