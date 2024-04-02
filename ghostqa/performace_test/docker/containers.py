from .client import get_client
from ..models import TestContainersRuns,TestArtifacts
import threading
import os,json
from cypress.utils import list_files_in_directory,directory_exists
from django.core.files import File
from django.conf import settings
import pandas,time
from ..utils.jmx_reporting import get_json_metrics,csv_to_json
import pandas as pd 
BASE_DIR  = settings.BASE_DIR
import logging  
logger = logging.getLogger(__name__)
CYPRESS_CONFIG_PATH = os.path.abspath(os.path.join(BASE_DIR,"cypress","cypress"))

def get_container(id_or_name):
    client = get_client()
    
    return client.containers.get(id_or_name)


def monitor_jmx_docker_conatiner(container,container_id,volume_path):
    # Simulate a time-consuming task
    while True:
        try:
            container_run = TestContainersRuns.objects.get(id=container_id)
            try:
                containe2r =  get_container(container_run.container_name)
                print(containe2r)
            except Exception as e:
                print(e)
            container_data = container.wait()
            print("monitor_jmx_docker_conatiner",container_data)
            if container_data.get('Error') == None:
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
                    logs_path = f"{volume_path}/log.csv"
                    statistics_path = f"{volume_path}/html-results/statistics.json"
                    html_path = f"{volume_path}/html-results"
                    print('monitor_jmx_docker_conatiner: logs_path',logs_path)
                    print('monitor_jmx_docker_conatiner: statistics_path',statistics_path)
                    test_artifact_instance = TestArtifacts.objects.create(
                        container_runs=container_run,
                        suite=container_run.suite,
                        type='logs',  # Replace with the actual type
                    )
                    print('monitor_jmx_docker_conatiner: test_artifact_instance:' ,test_artifact_instance)
                    with open(logs_path, 'rb') as file:
                        test_artifact_instance.files.save(os.path.basename(file.name), File(file))
                        test_artifact_instance.save()
                        print('monitor_jmx_docker_conatiner: file:' , file)
                    
                    test_artifact_instance = TestArtifacts.objects.create(
                        container_runs=container_run,
                        suite=container_run.suite,
                        type='statistics',  # Replace with the actual type
                    )
                    with open(statistics_path, 'rb') as file:
                        test_artifact_instance.files.save(os.path.basename(file.name), File(file))
                        test_artifact_instance.save()
                        file_data = test_artifact_instance.files.read().decode('utf-8')
                        data = json.loads(file_data)
                        container_run.json = data
                        container_run.save()
                        
                    
                    # test_artifact_instance = TestArtifacts.objects.create(
                    #     container_runs=container_run,
                    #     suite=container_run.suite,
                    #     type='html_zip',  # Replace with the actual type
                    # )
                    # with open(logs_path, 'rb') as file:
                    #     test_artifact_instance.files.save(os.path.basename(file.name), File(file))
                    #     test_artifact_instance.save()
                        
                                      
                    container.remove()
                    
                    print(container.status)
                    break
        except Exception as e:
            print("Exception",e)
            logger.exception(e)
            break

def live_update_from_container(container_run,logs_path):
        try:
            raw_data = csv_to_json(logs_path)
            container_run.raw_data = raw_data
            container_run.save()
            data = get_json_metrics(logs_path)
            container_run.json = data
            container_run.save()
        except pd.errors.EmptyDataError as pe: 
            pass   
        except Exception as e:
            logger.exception(e)

def monitor_jmx_docker_conatiner_With_live_reporting(container_originally_ran,container_id,volume_path):
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
                
                logs_path = f"{volume_path}/log.csv"
                live_update_from_container(container_run,logs_path)
                
                if container.status == "exited":
                
                    container_run.container_logs_str = container.logs()
                    container_run.save()
                    
                    result ={
                        "logs":[],
                        "statistics":[],
                        "html_zip":[],
                    }
                    logs_path = f"{volume_path}/log.csv"
                    statistics_path = f"{volume_path}/html-results/statistics.json"
                    html_path = f"{volume_path}/html-results"
                    print('monitor_jmx_docker_conatiner: logs_path',logs_path)
                    print('monitor_jmx_docker_conatiner: statistics_path',statistics_path)
                    test_artifact_instance = TestArtifacts.objects.create(
                        container_runs=container_run,
                        suite=container_run.suite,
                        type='logs',  # Replace with the actual type
                    )
                    print('monitor_jmx_docker_conatiner: test_artifact_instance:' ,test_artifact_instance)
                    with open(logs_path, 'rb') as file:
                        test_artifact_instance.files.save(os.path.basename(file.name), File(file))
                        test_artifact_instance.save()
                        print('monitor_jmx_docker_conatiner: file:' , file)
                        raw_data = csv_to_json(logs_path)
                        container_run.raw_data = raw_data
                        container_run.save()
                    
                    test_artifact_instance = TestArtifacts.objects.create(
                        container_runs=container_run,
                        suite=container_run.suite,
                        type='statistics',  # Replace with the actual type
                    )
                    with open(statistics_path, 'rb') as file:
                        test_artifact_instance.files.save(os.path.basename(file.name), File(file))
                        test_artifact_instance.save()
                        file_data = test_artifact_instance.files.read().decode('utf-8')
                        data = json.loads(file_data)
                        container_run.json = data
                        container_run.save()
                        
                    
                    # test_artifact_instance = TestArtifacts.objects.create(
                    #     container_runs=container_run,
                    #     suite=container_run.suite,
                    #     type='html_zip',  # Replace with the actual type
                    # )
                    # with open(logs_path, 'rb') as file:
                    #     test_artifact_instance.files.save(os.path.basename(file.name), File(file))
                    #     test_artifact_instance.save()
                        
                                      
                    container.remove()
                    
                    print(container.status)
                    break
              
            time.sleep(1)      
       
        except Exception as e:
            print("Exception",e)
            logger.exception(e)
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
        thread = threading.Thread(target=monitor_jmx_docker_conatiner, args=(container,container_run.id,volume_path,))
        thread.start()
    return container


def start_jmeter_test2(name, volume_path,Jthreads=10,Jrampup=10,container_run=None):
    client = get_client()
    # print('volume_path',volume_path)
    print(f"{__name__}: volume_path: {volume_path}")
    
    # Build the Docker image from the Dockerfile
    image, build_logs = client.images.build(path=volume_path, dockerfile=os.path.join(volume_path,'Dockerfile'), tag='jmeter_apline')

    container = client.containers.run(
        image='jmeter_apline',
        name=name,
        remove=False,
        command=f'-Jthreads={Jthreads} -Jrampup={Jrampup} -n -t /jmeter-scripts/test.jmx -l /jmeter-scripts/log.csv -e -o /jmeter-scripts/html-results',
        tty=True,
         volumes={
        volume_path: {'bind': '/jmeter-scripts', 'mode': 'rw'},
        # f"{volume_path}/bin/filename.csv": {'bind': '/opt/apache-jmeter-5.6.3/bin/filename.csv', 'mode': 'rw'}
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
        thread = threading.Thread(target=monitor_jmx_docker_conatiner_With_live_reporting, args=(container,container_run.id,volume_path,))
        thread.start()
    return container




