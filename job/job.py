
from threading import Thread
import time
from injector import logger

def thread_background():
    while True:
        try:
            logger.info('--thread_background--')
        except Exception as e:
            pass
        time.sleep(60)  # TODO poll other things
        
def create_job():        
    # Create thread as background
    Thread(target=thread_background, daemon=True).start()