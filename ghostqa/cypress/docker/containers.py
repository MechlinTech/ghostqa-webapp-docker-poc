from .client import get_client
from cypress.models import TestContainersRuns,TestArtifacts
import threading
import os,json
from cypress.utils import list_files_in_directory,directory_exists,list_recurssive_files_in_directory
from django.core.files import File
from django.conf import settings
BASE_DIR  = settings.BASE_DIR

CYPRESS_CONFIG_PATH = os.path.abspath(os.path.join(BASE_DIR,"cypress","cypress"))

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




def monitor_docker_conatinerv2(container_id,volume_path):
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
                        "videos":[],
                        "results":[],
                    }
                    screenshots_path = f"{volume_path}/e2e/cypress/screenshots/"
                    videos_path = f"{volume_path}/e2e/cypress/videos"
                    results_path = f"{volume_path}/e2e/cypress/results"
                    
                    if directory_exists(screenshots_path):
                        screenshots = list_recurssive_files_in_directory(screenshots_path)
                        result["screenshots"] = screenshots
                        


                    if directory_exists(videos_path):
                        videos = list_files_in_directory(videos_path)
                        result["videos"] = videos

                    if directory_exists(results_path):
                        results = list_files_in_directory(results_path)
                        result["results"] = results
                    
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
                    json_result_data = {}
                    for result_json in result["results"]:
                        print(result_json)
                        test_artifact_instance = TestArtifacts.objects.create(
                            container_runs=container_run,
                            suite=container_run.suite,
                            type='result',  # Replace with the actual type
                        )
                        with open(result_json, 'rb') as file:
                            test_artifact_instance.files.save(os.path.basename(file.name), File(file))
                            test_artifact_instance.save()
                            base_name = os.path.basename(file.name)
                            file_data = test_artifact_instance.files.read().decode('utf-8')
                            data = json.loads(file_data)
                            try:
                                suite_name = data.get('results')[0]['file']
                                path_parts = suite_name.split("/")
                                file_name = path_parts[-1]
                                file_name_parts = file_name.split(".")
                                test_suite_name = file_name_parts[0]
                                json_result_data[test_suite_name] = data
                            except Exception as e:
                                json_result_data[base_name] = data
                                    
                    container_run.json = json_result_data
                    container_run.save()
                    
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
    



def start_test_inside_conatinerV2(name, volume_path,container_run=None):
    client = get_client()
    # print('volume_path',volume_path)
    print(f"{__name__}: volume_path: {volume_path}")
    
    # Build the Docker image from the Dockerfile
    image, build_logs = client.images.build(path=volume_path, dockerfile=os.path.join(volume_path,'Dockerfile'), tag='ghost_qa_cypress')
    try:
        for log in build_logs:
            print("LOGS:",log)
    except Exception as e:
        print("Exception",e)
        
        
    container = client.containers.run(
        image="ghost_qa_cypress",
        name=name,
        # remove=True,
        command='cypress run --reporter mochawesome --reporter-options reportDir="cypress/results",overwrite=false,html=false,json=true',
        tty=True,
        working_dir="/e2e",
        volumes={
            os.path.join(volume_path,'e2e','cypress'): {'bind': '/e2e/cypress', 'mode': 'rw'},
            os.path.join(volume_path,'e2e','cypress.config.js'): {'bind': '/e2e/cypress.config.js', 'mode': 'rw'}
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
        thread = threading.Thread(target=monitor_docker_conatinerv2, args=(container_run.id,volume_path,))
        thread.start()
    return container






