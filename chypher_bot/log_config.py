import logging

def configure_logger():
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    
    file_handler = logging.FileHandler('logs.txt', encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Where What When
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    return logger