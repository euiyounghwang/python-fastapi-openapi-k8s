from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
# from controller import db_controller
# from config.log_config import create_log
import yaml
from injector import logger
from job.job import create_job
import asyncio
from contextlib import asynccontextmanager

# logger = create_log()

# DB 연결 객체와 세션 관리 변수
database_engine = None
db_session = None


async def create_task():
    logger.info("-- create_task.. --")


async def initialize_database():
    global database_engine, db_session

    print("Database initialized.")
    # database_url = "sqlite:///./database.db" # SQLite 예시
    # database_engine = create_engine(database_url)
    # SQLModel.metadata.create_all(database_engine) # 테이블 생성 (필요시)

    # DB 세션 생성 (예시)
    # db_session = Session(database_engine)

async def initialize_scheduler():
    print("Scheduler initialized.")
    
    # 이하 어플리케이션 시작 시 처리할 로직
    task0 = asyncio.create_task(create_task())
    await task0

    # --
    # Create task as background
    create_job()
    # --

async def clean_up_database():
    print("Database connection closed.")

async def clean_up_scheduler():
    print("Scheduler stopped.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    await initialize_database()
    await initialize_scheduler()
    print("All startup tasks completed.")
    yield
    # Shutdown tasks
    await clean_up_database()
    await clean_up_scheduler()
    print("All shutdown tasks completed.")


app = FastAPI(
    lifespan=lifespan,
    title="FastAPI Basic Docker with k8s Service",
    description="FastAPI Basic Docker with k8s Service",
    version="0.0.1",
    # terms_of_service="http://example.com/terms/",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



"""
loop = asyncio.get_event_loop()

if loop.is_running():
    # Multiple topics from config.yml or docker arguments
    # for topic in global_settings.get_Kafka_topic():
    #     asyncio.create_task(kafka_event(topic))
    print('Tasks..')
    asyncio.create_task(event_register())

"""

"""
# Load an external OpenAPI YAML file
with open("./api/openapi.yml", "r") as f:
    external_openapi_spec = yaml.safe_load(f)

def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        for _, method_item in app.openapi_schema.get('paths').items():
            for _, param in method_item.items():
                responses = param.get('responses')
                # remove 422 response, also can remove other status code
                if '422' in responses:
                    del responses['422']
    return app.openapi_schema
    # return external_openapi_spec

app.openapi = custom_openapi
"""

@app.get("/", tags=['API'],  
         status_code=200,
         responses={
            200: {"description" : "OK"},
            500 :{"description" : "Unexpected error"}
         },
         description="Default GET API", 
         summary="Return Default Json")
async def root():
    logger.info("/hello")
    return {"message": "python-fastapi-openapi.yml k8s"}

'''
@app.get("/test", tags=['API'],  
         status_code=200,
         description="Default GET Param API", 
         summary="Return GET Param Json")
async def root_with_arg(id):
    logger.info('root_with_arg - {}'.format(id))
    return {"message": "Hello World [{}]".format(id)}
'''

@app.get("/test/{id}", tags=['API'],  
         status_code=200,
         responses={
            200: {"description" : "OK"},
            500 :{"description" : "Unexpected error"}
         },
         description="Default GET with Body API", 
         summary="Return GET with Body Json")
async def test_api(id: int):
    logger.info('test_api - {}'.format(id))
    return {"message": "Hello World [{}]".format(id)}


# router
# app.include_router(db_controller.app, tags=["DB API"], )
