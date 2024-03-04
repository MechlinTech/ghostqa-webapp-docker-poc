from .client import get_client
from ..models import TestContainersRuns,TestArtifacts
import threading
import os,json
from cypress.utils import list_files_in_directory,directory_exists
from django.core.files import File
from django.conf import settings
BASE_DIR  = settings.BASE_DIR

CYPRESS_CONFIG_PATH = os.path.abspath(os.path.join(BASE_DIR,"cypress","cypress"))

def get_container(id_or_name):
    client = get_client()
    
    return client.containers.get(id_or_name)


def monitor_docker_conatinerv2(container,container_id,volume_path):
    # Simulate a time-consuming task
    while True:
        try:
            container_run = TestContainersRuns.objects.get(id=container_id)
            # container =  get_container(container_run.container_name)
            container_data = container.wait()
            if container_data['Error'] == None:
                container_run.container_id = container.id
                container_run.container_status = container.status
                container_run.container_labels = ""
                container_run.container_short_id = container.short_id
                container_run.save()
                container
                if container_data['StatusCode'] == 0 :
                    container_run.container_logs_str = container.logs()
                    container_run.save()
                    
                    result ={
                        "logs":[],
                        "statistics":[],
                        "html_zip":[],
                    }
                    logs_path = f"{volume_path}/log.jtl"
                    statistics_path = f"{volume_path}/html-results/statistics.json"
                    html_path = f"{volume_path}/html-results"
                    
                    test_artifact_instance = TestArtifacts.objects.create(
                        container_runs=container_run,
                        suite=container_run.suite,
                        type='logs',  # Replace with the actual type
                    )
                    with open(logs_path, 'rb') as file:
                        test_artifact_instance.files.save(os.path.basename(file.name), File(file))
                        test_artifact_instance.save()
                    
                    test_artifact_instance = TestArtifacts.objects.create(
                        container_runs=container_run,
                        suite=container_run.suite,
                        type='statistics',  # Replace with the actual type
                    )
                    with open(statistics_path, 'rb') as file:
                        test_artifact_instance.files.save(os.path.basename(file.name), File(file))
                        test_artifact_instance.save()
                    
                    test_artifact_instance = TestArtifacts.objects.create(
                        container_runs=container_run,
                        suite=container_run.suite,
                        type='html_zip',  # Replace with the actual type
                    )
                    with open(logs_path, 'rb') as file:
                        test_artifact_instance.files.save(os.path.basename(file.name), File(file))
                        test_artifact_instance.save()
                        
                                      
                    container.remove()
                    
                    print(container.status)
                    break
        except Exception as e:
            print("Exception",e)
            break
    



def start_jmeter_test(name, volume_path,Jthreads=10,Jrampup=10,container_run=None):
    client = get_client()
    # print('volume_path',volume_path)
    print(f"{__name__}: volume_path: {volume_path}")
    
    # Build the Docker image from the Dockerfile
    # image, build_logs = client.images.build(path=volume_path, dockerfile=os.path.join(volume_path,'Dockerfile'), tag='ghost_qa_scypress')

    container = client.containers.run(
        image='alpine/jmeter',
        name=name,
        remove=False,
        command=f'-Jthreads={Jthreads} -Jrampup={Jrampup} -n -t /jmeter-scripts/test.jmx -l /jmeter-scripts/log.jtl -e -o /jmeter-scripts/html-results',
        tty=True,
         volumes={
        volume_path: {'bind': '/jmeter-scripts', 'mode': 'rw'}
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
        thread = threading.Thread(target=monitor_docker_conatinerv2, args=(container,container_run.id,volume_path,))
        thread.start()
    return container






