import sys
from hatespeechclassification.logger import logging
from hatespeechclassification.exception import CustomException
from hatespeechclassification.components.data_ingestion import DataIngestion
from hatespeechclassification.components.data_transforamation import DataTransformation
from hatespeechclassification.components.model_trainer import ModelTrainer
from hatespeechclassification.components.model_evaluation import ModelEvaluation




from hatespeechclassification.entity.config_entity import (DataIngestionConfig,
                                                           DataTransformationConfig,
                                                           ModelTrainerConfig,
                                                           ModelEvaluationConfig,
                                                           ) 




from hatespeechclassification.entity.artifact_entity import (DataIngestionArtifacts,
                                                             DataTransformationArtifacts,
                                                             ModelTrainerArtifacts,
                                                             ModelEvaluationArtifacts,
                                                             )






class TrainPipeline:
    def __init__(self, mongo_uri, db_name):
                self.data_ingestion_config = DataIngestionConfig(mongo_uri, db_name)
                self.data_transformation_config = DataTransformationConfig()
                self.model_trainer_config = ModelTrainerConfig()
                self.model_evaluation_config =ModelEvaluationConfig(mongo_uri, db_name)
        


    

    def start_data_ingestion(self) -> DataIngestionArtifacts:
        logging.info("2-Entered the start_data_ingestion method of TrainPipeline class")
        try:
            logging.info("3-Getting the data from mongodb Storage ")
            data_ingestion = DataIngestion(data_ingestion_config = self.data_ingestion_config)

            data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
            logging.info("14-Got the train and valid from mongodb Storage")
            logging.info("15-Exited the start_data_ingestion method of TrainPipeline class")
            return data_ingestion_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e
        



    def start_data_transformation(self, data_ingestion_artifacts = DataIngestionArtifacts) -> DataTransformationArtifacts:
        logging.info("16-Entered the start_data_transformation method of TrainPipeline class")
        try:
            data_transformation = DataTransformation(
                data_ingestion_artifacts = data_ingestion_artifacts,
                data_transformation_config=self.data_transformation_config
            )

            data_transformation_artifacts = data_transformation.initiate_data_transformation()
            
            logging.info("27-Exited the start_data_transformation method of TrainPipeline class")
            return data_transformation_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e
        

    
    def start_model_trainer(self, data_transformation_artifacts: DataTransformationArtifacts) -> ModelTrainerArtifacts:
        logging.info("28-Entered the start_model_trainer method of TrainPipeline class")
        try:
            model_trainer = ModelTrainer(data_transformation_artifacts=data_transformation_artifacts,
                                        model_trainer_config=self.model_trainer_config
                                        )
            model_trainer_artifacts = model_trainer.initiate_model_trainer()
            logging.info("45-Exited the start_model_trainer method of TrainPipeline class")
            return model_trainer_artifacts

        except Exception as e:
            raise CustomException(e, sys)
        
    def start_model_evaluation(self, model_trainer_artifacts: ModelTrainerArtifacts, data_transformation_artifacts: DataTransformationArtifacts) -> ModelEvaluationArtifacts:
        logging.info("Entered the start_model_evaluation method of TrainPipeline class")
        try:
            model_evaluation = ModelEvaluation(data_transformation_artifacts = data_transformation_artifacts,
                                                model_evaluation_config=self.model_evaluation_config,
                                                model_trainer_artifacts=model_trainer_artifacts)

            model_evaluation_artifacts = model_evaluation.initiate_model_evaluation()
            logging.info("Exited the start_model_evaluation method of TrainPipeline class")
            return model_evaluation_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e  




    def run_pipeline(self):
        logging.info("1-Entered the run_pipeline method of TrainPipeline class")
        try:
            data_ingestion_artifacts = self.start_data_ingestion()

            data_transformation_artifacts = self.start_data_transformation(
                data_ingestion_artifacts=data_ingestion_artifacts
            )

            model_trainer_artifacts = self.start_model_trainer(
                data_transformation_artifacts=data_transformation_artifacts
            )

            model_evaluation_artifacts = self.start_model_evaluation(model_trainer_artifacts=model_trainer_artifacts,
                                                                    data_transformation_artifacts=data_transformation_artifacts
            ) 

            
            logging.info("46-Exited the run_pipeline method of TrainPipeline class") 
                                     
        except Exception as e:
            raise CustomException(e, sys) from e
        

    