# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers.execute import ExecuteSerializers
import yaml,json
from .build_cypress import generate_cypress_test
from .utils import create_directory, get_full_path,convert_to_unix_path

import subprocess

class ExecuteAPIView(APIView):
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
            with open(f"/automation-tests/{name}/e2e/cypress/integration/{name}.cy.js", "w") as cypress_test_file:
                cypress_test_file.write(cypress_code)

            with open(f"/automation-tests/{name}/e2e/cypress.json", "w") as cypress_json:
                json_data = {
                        "pluginsFile": False,
                        "supportFile": False
                }
                json.dump(json_data,cypress_json)
                                
            volume_path = get_full_path(f"/automation-tests/{name}/e2e")
            volume_path = convert_to_unix_path(volume_path)
            print(volume_path)
            docker_command  = f"docker run -it --name {name}  --rm --workdir /e2e -d -v {volume_path}:/e2e cypress/included:4.4.0 " 
            print(docker_command)
                    # Run the Docker command and capture the output
            result = subprocess.run(docker_command, shell=True, check=True)
            
            #         # Log the output to a file
            # with open(f"/automation-tests/{name}/e2e/log.log", 'w') as log_file:
            #     log_file.write(result.stdout)
            #     log_file.write(result.stderr)
            
            
            return Response(
                {"message": "Data processed successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
