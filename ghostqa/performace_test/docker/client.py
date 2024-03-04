

import docker
from django.conf import settings


def get_client():
    DOCKER_HOST = getattr(settings, 'DOCKER_HOST',None)
    
    if DOCKER_HOST:

        client = docker.DockerClient(base_url=DOCKER_HOST)
        return client
    else:
        client = docker.from_env()
        return client
