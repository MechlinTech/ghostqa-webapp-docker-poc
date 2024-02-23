from .client import get_client
from cypress.models import TestContainersRuns,TestArtifacts
import threading
import os
from cypress.utils import list_files_in_directory,directory_exists
from django.core.files import File

def get_container(id_or_name):
    client = get_client()
    
    return client.containers.get(id_or_name)

def monitor_docker_conatiner(container_id,volume_path):
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
                    
                    result ={
                        "screenshots":[],
                        "videos":[]
                    }
                    screenshots_path = f"{volume_path}/cypress/screenshots/{container_run.container_name}.cy.js"
                    videos_path = f"{volume_path}/cypress/videos"
                    
                    if directory_exists(screenshots_path):
                        screenshots = list_files_in_directory(screenshots_path)
                        result["screenshots"] = screenshots
                        


                    if directory_exists(videos_path):
                        videos = list_files_in_directory(videos_path)
                        result["videos"] = videos

                        
                    
                    for screenshot in result["screenshots"]:
                        print(screenshot)
                        test_artifact_instance = TestArtifacts.objects.create(
                            container_runs=container_run,
                            suite=container_run.suite,
                            type='screenshot',  # Replace with the actual type
                        )
                        with open(screenshot, 'rb') as file:
                            test_artifact_instance.files.save(os.path.basename(file.name), File(file))
                            test_artifact_instance.save()
                    
                    for video in result["videos"]:
                        print(video)
                        test_artifact_instance = TestArtifacts.objects.create(
                            container_runs=container_run,
                            suite=container_run.suite,
                            type='video',  # Replace with the actual type
                        )
                        with open(video, 'rb') as file:
                            test_artifact_instance.files.save(os.path.basename(file.name), File(file))
                            test_artifact_instance.save()
                    
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
        thread = threading.Thread(target=monitor_docker_conatiner, args=(container_run.id,volume_path,))
        thread.start()
    return container






