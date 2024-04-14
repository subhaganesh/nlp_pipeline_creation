import sys
from hatespeechclassification.logger import logging
from hatespeechclassification.exception import CustomException
from hatespeechclassification.components.data_ingestion import DataIngestion
from hatespeechclassification.entity.config_entity import (DataIngestionConfig)
from hatespeechclassification.entity.artifact_entity import (DataIngestionArtifacts)






class TrainPipeline:
    def __init__(self, mongo_uri, db_name):
        self.data_ingestion_config = DataIngestionConfig(mongo_uri, db_name)
        


    

    def start_data_ingestion(self) -> DataIngestionArtifacts:
        logging.info("Entered the start_data_ingestion method of TrainPipeline class")
        try:
            logging.info("Getting the data from mongodb Storage ")
            data_ingestion = DataIngestion(data_ingestion_config = self.data_ingestion_config)

            data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
            logging.info("Got the train and valid from mongodb Storage")
            logging.info("Exited the start_data_ingestion method of TrainPipeline class")
            return data_ingestion_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e
        


    def run_pipeline(self):
        logging.info("Entered the run_pipeline method of TrainPipeline class")
        try:
            data_ingestion_artifacts = self.start_data_ingestion()
        
        except Exception as e:
            raise CustomException(e, sys) from e
        