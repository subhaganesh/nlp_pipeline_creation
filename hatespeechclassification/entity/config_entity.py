from dataclasses import dataclass
from hatespeechclassification.constants import *
import os

@dataclass
class DataIngestionConfig:
    def __init__(self, mongo_uri, db_name):
        self.COLLECTION_NAME = COLLECTION_NAME
        self.ZIP_FILE_NAME = ZIP_FILE_NAME
        self.mongo_uri= mongo_uri
        self.db_name= db_name
        self.DATA_INGESTION_ARTIFACTS_DIR: str = os.path.join(os.getcwd(),ARTIFACTS_DIR,DATA_INGESTION_ARTIFACTS_DIR)
        self.DATA_ARTIFACTS_DIR: str = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR,DATA_INGESTION_IMBALANCE_DATA_DIR)
        self.NEW_DATA_ARTIFACTS_DIR: str = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR,DATA_INGESTION_RAW_DATA_DIR)
        self.ZIP_FILE_DIR = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR)
        self.ZIP_FILE_PATH = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR,self.ZIP_FILE_NAME)