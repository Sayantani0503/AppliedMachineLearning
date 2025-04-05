import subprocess
import time
import requests
import os

class TestDockerContainer:
  def test_docker(self):

    # Step 1: Build Docker image
    build_command = "docker build -t flask_app ."
    build_process = subprocess.run(build_command, shell=True, capture_output=True, text=True)
    assert build_process.returncode == 0, f"Build failed: {build_process.stderr}"

    # Step 2: Run Docker container
    run_command = "docker run -d -p 5000:5000 --name flask_container flask_app"
    run_process = subprocess.run(run_command, shell=True, capture_output=True, text=True)
    assert run_process.returncode == 0, f"Run failed: {run_process.stderr}"

    # Step 3: Wait for the server to be ready
    time.sleep(5)

    try:
        # Step 4: Send request to /score endpoint
        url = "http://localhost:5000/score"
        sample_data = {
            "text": "This is a test message.",
            "threshold": 0.5
        }
        response = requests.post(url, json=sample_data)

        # Step 5: Check response
        assert response.status_code == 200, f"Request failed: {response.text}"
        json_response = response.json()
        assert "prediction" in json_response
        assert "propensity" in json_response
        print("Test passed. Response:", json_response)

    finally:
        # Step 6: Stop and remove the container
        subprocess.run("docker stop flask_container", shell=True)
        subprocess.run("docker rm flask_container", shell=True)
