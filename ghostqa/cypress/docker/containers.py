from .client import get_client
from cypress.models import TestContainersRuns
import threading


def get_container(id_or_name):
    client = get_client()
    
    return client.containers.get(id_or_name)

def monitor_docker_conatiner(container_id):
    # Simulate a time-consuming task
    while True:
        try:
            container_run = TestContainersRuns.objects.get(id=container_id)
            container =  get_container(container_run.container_id)
            if container:
                container_run.container_id = container.id
                container_run.container_status = container.status
                container_run.container_labels = ""
                container_run.container_short_id = container.short_id
                container_run.save()
                
                if container.status == "exited":
                    container_run.container_logs_str = container.logs()
                    container_run.save()
                    
                    container.remove()
                    
                    print(container.status)
                    break
        except Exception as e:
            print("Exception",e)
            break
    

def start_test_inside_conatiner(name, volume_path,container_run=None):
    client = get_client()
    container = client.containers.run(
        image="cypress/included:4.4.0",
        name=name,
        # remove=True,
        tty=True,
        working_dir="/e2e",
        volumes={
            volume_path: {
                "bind": "/e2e",
                "mode": "rw",
            },
        },
        detach=True,
    )
    
    if container_run:
        container_run.container_id = container.id
        container_run.container_status = container.status
        container_run.container_labels = ""
        container_run.container_short_id = container.short_id
        container_run.save()
        
                # Start the threaded task
        thread = threading.Thread(target=monitor_docker_conatiner, args=(container_run.id,))
        thread.start()
    return container


