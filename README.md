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
- Service : http://VM_Node_#1:8888/docs




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

### Spark Cluster
- An Apache Spark cluster is a distributed computing system designed for processing large datasets in parallel. It consists of a master node and multiple worker nodes. 
    - Master Nodes: This node hosts the driver program, which is responsible for coordinating and managing the execution of Spark applications. It tracks the status of worker nodes and allocates tasks to them.
    - Worker Nodes: These nodes, also known as data nodes, are responsible for storing data and executing the actual data processing tasks. They run Spark executor processes that perform computations on data partitions assigned by the master
- Download : https://spark.apache.org/downloads.html
- Spark Run Mode : Cluster, Standalone(Sparck cluster with Master/Worker nodes in local env - `spark-submit with master address`, `start-master.sh`, `start-worker.sh <master_url>`), Local Mode(without cluster), Reference (https://wooono.tistory.com/140)
  - Spark Local Mode (https://bluehorn07.github.io/2024/08/18/run-spark-on-local-1/): 
    - python3 -m venv venv
    - source venv/bin/activate
    - pip3 install pyspark==3.5.2
    - pyspark
    - spark-submit --master "local[2]" ~/ES/spark/utils/hello-spark.py

- SSH into Local VM_#1, #2
### Commands to create Spark Cluster
- __Installation Commands__
  - lsb_release -a
  - sudo apt update
  - sudo apt install openjdk-17-jdk -y
  - wget https://dlcdn.apache.org/spark/spark-4.0.1/spark-4.0.1-bin-hadoop3.tgz
  - tar -xvf ./spark-4.0.1-bin-hadoop3.tgz
  - pwd
  - /home/devuser/ES/spark
  - ln -s ./spark-4.0.1-bin-hadoop3 latest
  - sudo dpkg --configure -a
  - sudo apt install python3.9
  - export SPARK_HOME=/home/devuser/ES/spark/latest
  - export PYSPARK_PYTHON=/usr/bin/python3.9
  - export PATH=$SPARK_HOME/bin:$PATH
  - echo 'export SPARK_HOME=/home/devuser/ES/spark/latest' >> ~/.bashrc
  - echo 'export PATH=$SPARK_HOME/bin:$PATH' >> ~/.bashrc
  - echo 'export PATH=$PYSPARK_PYTHON:$PATH' >> ~/.bashrc
  - source ~/.bashrc
  - `spark-shell` or `pyspark`
  ```bash
  WARNING: Using incubator modules: jdk.incubator.vector
  Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
  25/10/24 15:36:41 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
  Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
  Setting default log level to "WARN".
  To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
  Welcome to
        ____              __
      / __/__  ___ _____/ /__
      _\ \/ _ \/ _ `/ __/  '_/
    /___/ .__/\_,_/_/ /_/\_\   version 4.0.1
        /_/

  Using Scala version 2.13.16 (OpenJDK 64-Bit Server VM, Java 17.0.9)
  Type in expressions to have them evaluated.
  Type :help for more information.
  25/10/24 15:36:44 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
  Spark context Web UI available at http://VM_Node_#1:4040
  Spark context available as 'sc' (master = local[*], app id = local-1761338204619).
  Spark session available as 'spark'.

  >>> myRange = spark.range(1000).toDF("number")
  >>> divisBy2 = myRange.where("number % 2 = 0")
  >>> divisBy2.count()
  500
  scala> exit()
  ```
  - Setup Spark Cluster: Run the Master Node `spark-class org.apache.spark.deploy.master.Master -h VM_Node_#1` on VM_Node_#1, http://VM_Node_#1:8080, Reference (https://bluehorn07.github.io/topic/development#apache-spark)
    - If there is no JAVA_HOME Path: Modify `spark-env.sh`
    - cp conf/spark-env.sh.template conf/spark-env.sh
    ```bash
    #!/usr/bin/env bash

    export JAVA_HOME=/apps/monitoring_script/spark/java/latest
    spark-class org.apache.spark.deploy.master.Master -h localhost

    ```

    - `./spark-env.sh`
  ```bash
  WARNING: Using incubator modules: jdk.incubator.vector
  Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
  25/10/27 15:31:43 WARN Utils: Your hostname, ubuntu-node-1, resolves to a loopback address: 127.0.1.1; using VM_Node_#1 instead (on interface enp0s1)
  25/10/27 15:31:43 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
  25/10/27 15:31:44 INFO Master: Started daemon with process name: 2849@ubuntu-node-1
  25/10/27 15:31:44 INFO SignalUtils: Registering signal handler for TERM
  25/10/27 15:31:44 INFO SignalUtils: Registering signal handler for HUP
  25/10/27 15:31:44 INFO SignalUtils: Registering signal handler for INT
  25/10/27 15:31:44 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
  Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
  25/10/27 15:31:44 INFO SecurityManager: Changing view acls to: devuser
  25/10/27 15:31:44 INFO SecurityManager: Changing modify acls to: devuser
  25/10/27 15:31:44 INFO SecurityManager: Changing view acls groups to: devuser
  25/10/27 15:31:44 INFO SecurityManager: Changing modify acls groups to: devuser
  25/10/27 15:31:44 INFO SecurityManager: SecurityManager: authentication disabled; ui acls disabled; users with view permissions: devuser groups with view permissions: EMPTY; users with modify permissions: devuser; groups with modify permissions: EMPTY; RPC SSL disabled
  25/10/27 15:31:44 INFO Utils: Successfully started service 'sparkMaster' on port 7077.
  25/10/27 15:31:44 INFO Master: Starting Spark master at spark://VM_Node_#1:7077
  25/10/27 15:31:44 INFO Master: Running Spark version 4.0.1
  25/10/27 15:31:44 INFO JettyUtils: Start Jetty 0.0.0.0:8080 for MasterUI
  25/10/27 15:31:44 INFO Utils: Successfully started service 'MasterUI' on port 8080.
  25/10/27 15:31:44 INFO MasterWebUI: Bound MasterWebUI to 0.0.0.0, and started at http://VM_Node_#1:8080
  25/10/27 15:31:44 INFO Master: I have been elected leader! New state: ALIVE
  ```
  - Run spark application on Master node : `spark-submit --master spark://VM_Node_#1:7077 ~/ES/spark/utils/hello-spark.py` (Need to join the Worker node into Spark Cluster), `WARN TaskSchedulerImpl: Initial job has not accepted any resources; check your cluster UI to ensure that workers are registered and have sufficient resources`
  ```bash
  25/10/27 15:45:23 INFO DAGScheduler: Submitting 2 missing tasks from ResultStage 0 (PythonRDD[1] at count at /home/devuser/ES/spark/utils/hello-spark.py:10) (first 15 tasks are for partitions Vector(0, 1))
  25/10/27 15:45:23 INFO TaskSchedulerImpl: Adding task set 0.0 with 2 tasks resource profile 0
  25/10/27 15:45:38 WARN TaskSchedulerImpl: Initial job has not accepted any resources; check your cluster UI to ensure that workers are registered and have sufficient resources
  ```
  - Setup Spark Cluster: Run the Worker Node `spark-class org.apache.spark.deploy.worker.Worker spark://VM_Node_#1:7077` on VM_Node_#2
  - Run the spark application on Master node (VM_Node_#1): `spark-submit --master spark://VM_Node_#1:7077 --total-executor-cores 1 --executor-memory 512m ~/ES/spark/utils/hello-spark.py`


### Kubernetes
- Kubernetes is an open-source container orchestration system that automates the deployment, scaling, and management of containerized applications. It works by providing an API to manage clusters of virtual machines, scheduling containers, and automatically handling tasks like service discovery, load balancing, and self-healing to ensure applications remain available. 
### Commands to create K8s Cluster
- __Installation Commands__
  - lsb_release -a
  - pwd
  - /home/devuser/ES/k8s


### Search Engine
- Meilisearch(https://github.com/meilisearch/meilisearch) : Meilisearch is an open-source, lightning-fast search engine designed to provide a highly relevant and intuitive search experience for applications and websites
```bash
curl \
  -X POST 'http://localhost:7700/indexes/movies/documents' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer CMJuRd2KKqt1UmxntJZCelvlDuxrbiUzzQ9AW9B7lnQ' \
  --data-binary @movies.json
```
- Zincsearch (https://github.com/zincsearch/zincsearch): ZincSearch is a search engine that does full text indexing. It is a lightweight alternative to Elasticsearch and runs using a fraction of the resources. 
- Docs : https://zincsearch-docs.zinc.dev/quickstart/, Swagger : http://localhost:4080/swagger/
- Run : `./zincsearch ZINC_PROMETHEUS_ENABLE=true`
- Bulk Sample : $ curl http://localhost:4080/api/_bulk -i -u test:test --data-binary "@./Search_Engine/olympics.json"
```bash
ZINC_FIRST_ADMIN_USER=test
ZINC_FIRST_ADMIN_PASSWORD=test
```
- Search
```bash
curl \
  -X POST 'http://localhost:4080/api/olympics/_search' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Basic test:test' \
  -d'
     {
       "query": {
         "match_all": {}
       }
  }'
```