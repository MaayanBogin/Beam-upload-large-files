import os

def write_models(models):
    import requests
    for model_url, directory in models:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        file_name = os.path.join(directory, os.path.basename(model_url))
        
        # Stream the file download
        with requests.get(model_url, stream=True) as response:
            response.raise_for_status()
            with open(file_name, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        
        print(f"Downloaded: {file_name}")

# Step 1: Define environment setup and repository cloning
from beam import task_queue, Image, Volume

@task_queue(
    name="upload-models-to-volume",
    cpu=4,
    memory="16Gi",
    image=Image(
        python_version="python3.8",
        python_packages=[
            # Add any additional packages required
        ],
        commands=["apt-get update && apt-get install -y wget git"],
    ),
    volumes=[Volume(name="models", mount_path="./models")],
    keep_warm_seconds=0,
    #on_start=download_models,
)
def run(**inputs):
    # This function is a placeholder, as the main task is performed in the on_start hook.
    files = inputs["files"]
    write_models(files)
    
    
    print("Models cloned successfully.")