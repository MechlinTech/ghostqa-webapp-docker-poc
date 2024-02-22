# views.py
import json
import mimetypes
import os
import subprocess
from io import BytesIO

import yaml
from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse
from PIL import Image as PILImage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .build_cypress import generate_cypress_test
from .serializers.execute import ExecuteSerializers
from .utils import (
    check_container_status,
    convert_to_unix_path,
    create_directory,
    directory_exists,
    get_full_path,
    list_files_in_directory,
)
from .docker.containers import start_test_inside_conatiner


class VideosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        video_path = request.GET.get("path", None)

        # Open the video file
        chunk_size = 8192  # Adjust the chunk size according to your needs

        # Set appropriate content type for video streaming
        content_type, encoding = mimetypes.guess_type(video_path)
        response = HttpResponse(content_type=content_type)
        response["Content-Disposition"] = (
            f'inline; filename="{os.path.basename(video_path)}"'
        )

        # Stream the video content
        with open(video_path, "rb") as video_file:
            for chunk in iter(lambda: video_file.read(chunk_size), b""):
                response.write(chunk)

        return response
        return Response(
            {"message": "Data processed successfully"},
            status=status.HTTP_201_CREATED,
        )


class ScreenshotsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Open the image using PIL
        file_path = request.GET.get("path", None)
        pil_image = PILImage.open(file_path)

        # Convert the PIL image to bytes
        image_bytes = BytesIO()
        pil_image.save(image_bytes, format="PNG")
        image_data = image_bytes.getvalue()

        # Create the HTTP response with the image data
        response = HttpResponse(image_data, content_type="image/png")
        response["Content-Disposition"] = f'attachment; filename="{file_path}"'
        return response


class ExecuteAPIView(APIView):
    def get(self, request, *args, **kwargs):
        name = request.GET.get("name", None)

        if name is None:
            return Response(
                {"error": "Query Parameter: name is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        exited = check_container_status(name)

        message = None
        result = {
            "videos": [],
            "screenshots": [],
        }
        if exited or exited is None:
            message = ""
            if directory_exists(
                f"/automation-tests/{name}/e2e/cypress/screenshots/{name}.cy.js"
            ):
                screenshots = list_files_in_directory(
                    os.path.join(
                        "/automation-tests",
                        name,
                        "e2e",
                        "cypress",
                        "screenshots",
                        f"{name}.cy.js",
                    )
                )
                result["screenshots"] = screenshots

            if directory_exists(f"/automation-tests/{name}/e2e/cypress/videos"):
                videos = list_files_in_directory(
                    os.path.join("/automation-tests", name, "e2e", "cypress", "videos")
                )
                result["videos"] = videos

        return Response(
            {"message": "Data processed successfully", "exited": exited, **result},
            status=status.HTTP_201_CREATED,
        )

    def post(self, request, *args, **kwargs):
        serializer = ExecuteSerializers(data=request.data)

        if serializer.is_valid():
            # Process your data or save it to the database here
            # For example, you might save the uploaded file and name to the database
            # or perform some specific action with the data.
            validated_data = serializer.validated_data

            name = validated_data.get("name")
            upload_file = validated_data.get("upload_file")
            tests = yaml.safe_load(upload_file)

            cypress_code = generate_cypress_test(tests)

            create_directory(f"/automation-tests/{name}/e2e/cypress/integration/")
            create_directory(f"/automation-tests/{name}/e2e/logs")

            with open(
                f"/automation-tests/{name}/e2e/cypress/integration/{name}.cy.js", "w"
            ) as cypress_test_file:
                cypress_test_file.write(cypress_code)

            with open(
                f"/automation-tests/{name}/e2e/cypress.json", "w"
            ) as cypress_json:
                json_data = {"pluginsFile": False, "supportFile": False}
                json.dump(json_data, cypress_json)

            volume_path = f"/automation-tests/{name}/e2e"
            volume_path = get_full_path(volume_path)
            volume_path = convert_to_unix_path(volume_path)
            if settings.SHARED_PATH:
                volume_path = f"{settings.SHARED_PATH}/{name}/e2e"

            docker_command = f"docker run -it --name {name} --workdir /e2e  -v {volume_path}:/e2e cypress/included:4.4.0"
            print(docker_command)

            # try:
            #     # Run the Docker command and capture the output
            #     # result = subprocess.run(docker_command, shell=True, check=True, capture_output=True, text=True)

            #     # Use subprocess.Popen to capture real-time output
            #     with open(
            #         f"/automation-tests/{name}/e2e/logs/{name}.log",
            #         "w",
            #         encoding="utf-8",
            #     ) as output_file:
            #         with open(
            #             f"/automation-tests/{name}/e2e/logs/{name}.err.log",
            #             "w",
            #             encoding="utf-8",
            #         ) as output_log_file:
            #             # process = subprocess.run(docker_command,  stdout=output_file,stderr=output_log_file, shell=True,check=False, capture_output=True, text=True,encoding='utf-8')
            #             process = subprocess.Popen(
            #                 docker_command,
            #                 stdout=output_file,
            #                 stderr=output_log_file,
            #                 shell=True,
            #                 text=True,
            #                 encoding="utf-8",
            #             )
            #             # Wait for the command to complete
            #             # Check if the process is still running
            #             exit_code = None
            #             message = None
            #             if process.poll() is None:
            #                 message = "The process is still running."
            #             else:
            #                 # Get the exit code if the process has finished
            #                 exit_code = process.returncode
            #                 message = (
            #                     f"The process has finished with exit code: {exit_code}"
            #                 )
            #             return Response(
            #                 {
            #                     "message": message,
            #                     "process_pid": process.pid,
            #                     "exit_code": exit_code,
            #                 },
            #                 status=status.HTTP_201_CREATED,
            #             )
            # except subprocess.CalledProcessError as e:
            #     return Response(
            #         {
            #             "error": f"Failed to execute Docker command: {e}",
            #             "logs": e.stdout,
            #         },
            #         status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            #     )

            container = start_test_inside_conatiner(name, volume_path)
            return Response(
                {
                    "message": "Data processed successfully",
                    "container": {
                        "id": container.id,
                        "status": container.status,
                        "name": container.name,
                        "labels": container.labels,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
