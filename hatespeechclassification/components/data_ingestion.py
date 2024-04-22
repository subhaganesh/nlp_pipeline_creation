import os
import sys
from zipfile import ZipFile
from hatespeechclassification.logger import logging
from hatespeechclassification.exception import CustomException
from hatespeechclassification.configuration.mongodb import MongoDB
from hatespeechclassification.entity.config_entity import DataIngestionConfig
from hatespeechclassification.entity.artifact_entity import DataIngestionArtifacts


class DataIngestion:
    def __init__(self, data_ingestion_config : DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        self.MongoDB = MongoDB()


    def get_data_from_mongodb(self) -> None:
        try:
            logging.info("5-Entered the get_data_from mongodb method of Data ingestion class")
            os.makedirs(self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR, exist_ok=True)

            self.MongoDB.extract_zip_from_mongodb(self.data_ingestion_config.mongo_uri,
                                                  self.data_ingestion_config.db_name,
                                                  self.data_ingestion_config.ZIP_FILE_NAME,
                                                  self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR,
                                                 )
            
            logging.info("7-Exited the get_data_from mongodb method of Data ingestion class")

        
        except Exception as e:
            raise CustomException(e, sys) from e
        
    
    def unzip_and_clean(self):
        logging.info("9-Entered the unzip_and_clean method of Data ingestion class")
        try: 
            with ZipFile(self.data_ingestion_config.ZIP_FILE_PATH, 'r') as zip_ref:
                zip_ref.extractall(self.data_ingestion_config.ZIP_FILE_DIR)

            logging.info("10-Exited the unzip_and_clean method of Data ingestion class")

            return self.data_ingestion_config.DATA_ARTIFACTS_DIR, self.data_ingestion_config.NEW_DATA_ARTIFACTS_DIR

        except Exception as e:
            raise CustomException(e, sys) from e
        
    

    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        logging.info("4-Entered the initiate_data_ingestion method of Data ingestion class")

        try:
            self.get_data_from_mongodb()
            logging.info("8-Fetched the data from mongodb")
            imbalance_data_file_path, raw_data_file_path = self.unzip_and_clean()
            logging.info("11-Unzipped file and split into train and valid")

            data_ingestion_artifacts = DataIngestionArtifacts(
                imbalance_data_file_path= imbalance_data_file_path,
                raw_data_file_path = raw_data_file_path
            )

            logging.info("12-Exited the initiate_data_ingestion method of Data ingestion class")

            logging.info(f"13-Data ingestion artifact: {data_ingestion_artifacts}")

            return data_ingestion_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e