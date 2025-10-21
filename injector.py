from config.log_config import create_log
from dotenv import load_dotenv
# import yaml
import json
import os
# from service.db_service import DBHandler

load_dotenv()
    
# Initialize & Inject with only one instance
logger = create_log()


# DBHandlerInject = DBHandler(logger)