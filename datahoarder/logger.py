import logging

logger = logging.getLogger(__name__)

c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')
c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.ERROR)

logger.addHandler(c_handler)
logger.addHandler(f_handler)