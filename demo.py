from hatespeechclassification.logger import logging
from hatespeechclassification.exception import CustomException
import sys

#logging.info('demo logs')

try:
    x=7/'0'
except Exception as e:
    raise  CustomException(e , sys) from e



