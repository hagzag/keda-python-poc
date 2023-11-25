from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint

import yaml
import os

app = FastAPI()

# Global variable to store the current scale
current_scale = 3

class ScaleResponse(BaseModel):
    desiredReplicas: int

class ScaleRequest(BaseModel):
    desiredReplicas: conint(ge=0, le=9)  # Constrained int between 0 and 9

@app.get("/scale", response_model=ScaleResponse)
def get_scale():
    return ScaleResponse(desiredReplicas=current_scale)

@app.post("/scale", response_model=ScaleResponse)
def set_scale(scale_request: ScaleRequest):
    global current_scale
    current_scale = scale_request.desiredReplicas
    return ScaleResponse(desiredReplicas=current_scale)


def load_config():
    # Default configuration
    config_data = {"app": {"listen_port": 5000}}

    # File paths
    config_paths = ["config.yaml", "config.yml"]

    # Try loading configuration from each file
    for path in config_paths:
        try:
            with open(path, "r") as file:
                config_from_file = yaml.safe_load(file)
                config_data.update(config_from_file)
                print(f"Configuration loaded from {path}")
                break
        except FileNotFoundError:
            continue
    else:
        print("No YAML configuration file found, using default or .env settings")

    # Override with .env settings if available
    config_data['app'] = {
        'listen_port': config('APP_LISTEN_PORT', default=config_data.get('app', {}).get('listen_port', 9000), cast=int)
    }

    return config_data

if __name__ == "__main__":
    import uvicorn

    # Load configuration
    config = load_config()

    uvicorn.run(app, host="0.0.0.0", port=config['app']['listen_port'])
