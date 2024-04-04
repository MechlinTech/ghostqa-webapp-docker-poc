# Define the URL of the Docker Compose file
$composeFileUrl = "https://raw.githubusercontent.com/MechlinTech/ghostqa-webapp-docker-poc/main/deploy.yml"

# Download the Docker Compose file
Invoke-WebRequest -Uri $composeFileUrl -OutFile "docker-compose.yml"

docker pull ghostqa/codeengine:latest
# Run docker-compose up command
docker compose up
