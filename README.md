# keda-python-poc



## starting local demo

1. git clone this repo
2. poetry install
3. poetry run uvicorn api:app --reload

[see also this section below](#run-localy)

## get scale - discover default values

```sh
curl -X GET localhost:8000/scale
```

yiedls: `{"desiredReplicas":3}`

## Configure "workers" scale

```sh
curl -X POST http://localhost:8000/scale -H "Content-Type: application/json" -d '{"desiredReplicas": 9}'
```

## Get new scale

```sh
curl -X GET localhost:8000/scale
```

yiedls: `{"desiredReplicas":9}`

## Run localy

run `task run-api-local` which will run the following commands for you:

- poetry install --no-root
- poetry env info
- poetry run uvicorn api:app --reload 

run `task run-worker-local` which will run the following commands for you:

- poetry install --no-root
- poetry env info
- poetry run uvicorn worker:app --reload 

## Build a container

run `task docker-build` which will run the following commands: 

- `docker build -t 'your-repo/keda-poc:0.0.1'`

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
