# python-fastapi-openapi-k8s
<i>python-fastapi-openapi-k8s


### Install Poerty
```
https://python-poetry.org/docs/?ref=dylancastillo.co#installing-with-the-official-installer
```


### Using Python Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate
```


### Using Poetry: Create the virtual environment in the same directory as the project and install the dependencies:
- Gunicorn is a Python WSGI HTTP Server that usually lives between a reverse proxy (e.g., Nginx) or load balancer (e.g., AWS ELB) and a web application such as Django or Flask.
- Better performance by optimizing Gunicorn config (https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7)
- The suggested number of workers is (2*CPU)+1.
- gunicorn --workers=5 --threads=2 --worker-class=gthread main:app, the maximum concurrent requests areworkers * threads 10 in our case.

```bash
poetry config virtualenvs.in-project true
poetry init
poetry add fastapi
poetry add gunicorn
poetry add uvicorn
poetry add pytz
poetry add httpx
poetry add pytest
poetry add pytest-cov
poetry add requests
poetry add python-dotenv
poetry add pyyaml
...

# start with gunicorn config
gunicorn.config.py

import multiprocessing
 
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
wsgi_app = "app.main:app"
timeout = 60
loglevel = "info"
bind = "0.0.0.0:8000"
max_requests = 1000
max_requests_jitter = 100

...
gunicorn -c app/gunicorn.config.py

gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8004 --workers 4

..
uvicorn app.main:app --reload for dev
```
or you can run this shell script `./create_virtual_env.sh` to make an environment. then go to virtual enviroment using `source .venv/bin/activate`


### Register Service
- sudo service k8s_es_api status/stop/start/restart
```bash
#-- /etc/systemd/system/k8s_es_api.service
[Unit]
Description=k8s ES Service

[Service]
User=devuser
Group=devuser
Type=simple
ExecStart=/bin/bash /home/devuser/k8s_interface_api/service-start.sh
ExecStop= /usr/bin/killall k8s_es_api

[Install]
WantedBy=default.target


# Service command
sudo systemctl daemon-reload 
sudo systemctl enable k8s_es_api.service
sudo systemctl start k8s_es_api.service 
sudo systemctl status k8s_es_api.service 
sudo systemctl stop k8s_es_api.service 

sudo service k8s_es_api status/stop/start
```


### Service
- Run this command `./start-start.sh` or `python -m uvicorn main:app --reload --host=0.0.0.0 --port=8888 --workers 4`
- Run Dockerfile: `CMD ["gunicorn", "-w", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8888", "-t", "30", "--pythonpath", "/app/FN-Basic-Services", "main:app"]`
- Service : http://localhost:8888/docs




### Pytest
- Go to virtual enviroment using `source .venv/bin/activate`
- Run this command manually: `poetry run py.test -v --junitxml=test-reports/junit/pytest.xml --cov-report html --cov tests/` or `./pytest.sh`
```bash
$ ./pytest.sh
tests\test_api.py::test_api [2025-10-23 15:26:04,750] [INFO] [main] [root] /hello
[2025-10-23 15:26:04,759] [INFO] [_client] [_send_single_request] HTTP Request: GET http://testserver/ "HTTP/1.1 200 OK"
PASSED

============================================================= tests coverage ============================================================== 
_____________________________________________ coverage: platform win32, python 3.11.7-final-0 _____________________________________________ 

Name                   Stmts   Miss  Cover   Missing
----------------------------------------------------
config\log_config.py      32      1    97%   42
injector.py                6      0   100%
main.py                   13      0   100%
tests\__init__.py          0      0   100%
tests\conftest.py          8      0   100%
tests\test_api.py          6      0   100%
----------------------------------------------------
TOTAL                     65      1    98%
============================================================ 1 passed in 0.23s ============================================================ 
(.venv) 
```



### Docker build
- Run the command using `./docker-compose.yml` or `./docker-build.sh` and `./docker-run.sh`
```bash
*  Executing task in folder python-fastapi-openapi-k8s: 'C:\Program Files\Docker\Docker\resources\bin\docker.EXE' compose -f 'docker-compose.yml' up -d --build 'fn-basic-docker-api' 'fn-basic-docker-api-test' 

[+] Building 7.5s (19/19) FINISHED
 => [internal] load local bake definitions                                                                                             0.0s
 => => reading from stdin 925B                                                                                                         0.0s
 => [fn-basic-docker-api-test internal] load build definition from Dockerfile                                                          0.0s
 => => transferring dockerfile: 2.39kB                                                                                                 0.0s
 => WARN: FromPlatformFlagConstDisallowed: FROM --platform flag should not use constant value "linux/amd64" (line 3)                   0.0s 
 => WARN: FromPlatformFlagConstDisallowed: FROM --platform flag should not use constant value "linux/amd64" (line 34)                  0.0s 
 => WARN: FromPlatformFlagConstDisallowed: FROM --platform flag should not use constant value "linux/amd64" (line 49)                  0.0s 
 => WARN: FromPlatformFlagConstDisallowed: FROM --platform flag should not use constant value "linux/amd64" (line 3)                   0.0s 
 => WARN: FromPlatformFlagConstDisallowed: FROM --platform flag should not use constant value "linux/amd64" (line 34)                  0.0s 
 => WARN: FromPlatformFlagConstDisallowed: FROM --platform flag should not use constant value "linux/amd64" (line 49)                  0.0s 
 => [fn-basic-docker-api internal] load metadata for docker.io/library/python:3.9-slim-buster                                          0.7s 
 => [fn-basic-docker-api internal] load .dockerignore                                                                                  0.0s
 => => transferring context: 74B                                                                                                       0.0s 
 => [fn-basic-docker-api-test environment 1/5] FROM docker.io/library/python:3.9-slim-buster@sha256:320a7a4250aba4249f458872adecf92ee  0.0s 
 => [fn-basic-docker-api-test internal] load build context                                                                             0.7s 
 => => transferring context: 226.34kB                                                                                                  0.7s 
 => CACHED [fn-basic-docker-api-test runtime 2/5] WORKDIR /app                                                                         0.0s
 => CACHED [fn-basic-docker-api-test environment 2/5] RUN python3 -m venv /app/poetry-venv  && /app/poetry-venv/bin/pip install -U pi  0.0s 
 => CACHED [fn-basic-docker-api-test environment 3/5] WORKDIR /app                                                                     0.0s
 => CACHED [fn-basic-docker-api-test environment 4/5] COPY poetry.lock pyproject.toml ./                                               0.0s 
 => CACHED [fn-basic-docker-api-test environment 5/5] RUN /bin/bash -c 'source $POETRY_VENV/bin/activate &&     poetry install --no-r  0.0s 
 => CACHED [fn-basic-docker-api-test runtime 3/5] COPY --from=environment /app .                                                       0.0s 
 => [fn-basic-docker-api runtime 4/5] COPY . FN-Basic-Services                                                                         1.4s
 => [fn-basic-docker-api-test test 5/5] RUN sed -i -e 's/\r$//' /app/FN-Basic-Services/*.sh                                            0.6s 
 => [fn-basic-docker-api runtime 5/5] RUN sed -i -e 's/\r$//' /app/FN-Basic-Services/*.sh                                              0.7s 
 => [fn-basic-docker-api-test] exporting to image                                                                                      1.0s 
 => => exporting layers                                                                                                                1.0s 
 => => writing image sha256:9efc497a918564a8c7d0de13bbd04f07e82df3e852a8ad87c6fdbf7fde2a5db5                                           0.0s 
 => => naming to docker.io/library/ffn-basic-docker-api:test                                                                           0.0s 
 => [fn-basic-docker-api] exporting to image                                                                                           1.0s 
 => => exporting layers                                                                                                                1.0s 
 => => writing image sha256:b4bfe71d730f3ace7f14eba1540487c482628029037648f59ffd31541df26df8                                           0.0s 
 => => naming to docker.io/library/fn-basic-docker-api:es                                                                              0.0s 
 => [fn-basic-docker-api] resolving provenance for metadata file                                                                       0.0s 
 => [fn-basic-docker-api-test] resolving provenance for metadata file                                                                  0.0s 
[+] Running 4/4
 ✔ fn-basic-docker-api                 Built                                                                                           0.0s 
 ✔ fn-basic-docker-api-test            Built                                                                                           0.0s 
 ✔ Container fn-basic-docker-api       Started                                                                                        12.9s 
 ✔ Container fn-basic-docker-api-test  Started                                                                                        12.9s 
 *  Terminal will be reused by tasks, press any key to close it. 
```


### Kubernetes
- Kubernetes is an open-source container orchestration system that automates the deployment, scaling, and management of containerized applications. It works by providing an API to manage clusters of virtual machines, scheduling containers, and automatically handling tasks like service discovery, load balancing, and self-healing to ensure applications remain available. 