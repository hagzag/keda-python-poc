# keda-python-poc


## starting local demo

1. git clone this repo
2. task run-api-local
2. task run-grpc-local

[see also this section below](#run-localy)

## get scale - discover default values

```sh
curl -X GET localhost:9090/scale
```

yiedls: `{"desiredReplicas":3}`

## Configure "workers" scale

```sh
curl -X POST http://localhost:9090/scale -H "Content-Type: application/json" -d '{"desiredReplicas": 9}'
```

## Get new scale

```sh
curl -X GET localhost:9090/scale
```

yiedls: `{"desiredReplicas":9}`

## Run localy

run `task run-api-local` which will run the following commands for you:

- poetry install --no-root
- poetry run uvicorn src.api.main:app --port 9090 --reload 

run `task run-grpc-local` which will run the following commands for you:

- poetry run python src/custom_scaler/grpc_server.py

run `task run-worker-local` which will run the following commands for you:

- poetry install --no-root
- poetry run uvicorn src.worker.main:app --port 8080 --reload 

## Build a container

run `task docker-build` which will run the following commands: 

- `docker build -t 'your-repo/keda-poc:0.0.1'`

## Run via docker

TBC

## add keda scaling object

1. access to a given cluster - use a "Palygrond" cluster
1. install keda in keda namespace - `task deploy_keda`
1. deploy app in keda-poc namespace `task deploy_demo_app`

1. create scaling object
1. trigger a scale up event
1. trigger a scale down event

## our app:

- ./apy.py  `task run-api-local`
- ./worker.py `task run-worker-local`
