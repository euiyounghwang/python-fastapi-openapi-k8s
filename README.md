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


### Kubernetes
- Kubernetes is an open-source container orchestration system that automates the deployment, scaling, and management of containerized applications. It works by providing an API to manage clusters of virtual machines, scheduling containers, and automatically handling tasks like service discovery, load balancing, and self-healing to ensure applications remain available. 