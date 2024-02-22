from .client import get_client


def start_test_inside_conatiner(name, volume_path):
    client = get_client()
    container = client.containers.run(
        image="cypress/included:4.4.0",
        name=name,
        remove=True,
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
    
    logs = container.logs()
    
    print(logs)
    return container
