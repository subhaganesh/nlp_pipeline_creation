import os 
import sys
import pickle
import pandas as pd
from hatespeechclassification.logger import logging
from hatespeechclassification.constants import *
from hatespeechclassification.exception import CustomException
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from hatespeechclassification.entity.config_entity import ModelTrainerConfig
from hatespeechclassification.entity.artifact_entity import ModelTrainerArtifacts,DataTransformationArtifacts
from hatespeechclassification.ml.model import ModelArchitecture



class ModelTrainer:
    def __init__(self,data_transformation_artifacts: DataTransformationArtifacts,
                model_trainer_config: ModelTrainerConfig):

        self.data_transformation_artifacts = data_transformation_artifacts
        self.model_trainer_config = model_trainer_config

    
    def spliting_data(self,csv_path):
        try:
            logging.info("31-Entered the spliting_data function")
            logging.info("32-Reading the data")
            df = pd.read_csv(csv_path, index_col=False)
            logging.info("33-Splitting the data into x and y")
            x = df[TWEET]
            y = df[LABEL]

            logging.info("34-Applying train_test_split on the data")
            x_train,x_test,y_train,y_test = train_test_split(x,y, test_size=0.3,random_state = 42)
            print(len(x_train),len(y_train))
            print(len(x_test),len(y_test))
            print(type(x_train),type(y_train))
            logging.info("35-Exited the spliting the data function")
            return x_train,x_test,y_train,y_test

        except Exception as e:
            raise CustomException(e, sys) from e
        

    
    def tokenizing(self,x_train):
        try:
            logging.info("38-Applying tokenization on the data")
            tokenizer = Tokenizer(num_words=self.model_trainer_config.MAX_WORDS)
            tokenizer.fit_on_texts(x_train)
            sequences = tokenizer.texts_to_sequences(x_train)
            print(f"converting text to sequences: {sequences}")
            logging.info("39-converting text to sequences")
            sequences_matrix = pad_sequences(sequences,maxlen=self.model_trainer_config.MAX_LEN)
            print(f"40- The pad_sequence matrix is: {sequences_matrix}")
            logging.info("40- The sequence matrix is added with padding")
            return sequences_matrix,tokenizer
        except Exception as e:
            raise CustomException(e, sys) from e
        

    

    def initiate_model_trainer(self,) -> ModelTrainerArtifacts:
        logging.info("29-Entered initiate_model_trainer method of ModelTrainer class")

        """
        Method Name :   initiate_model_trainer
        Description :   This function initiates a model trainer steps
        
        Output      :   Returns model trainer artifact
        On Failure  :   Write an exception log and then raise an exception
        """

        try:
            logging.info("30-Entered the initiate_model_trainer function ")
            x_train,x_test,y_train,y_test = self.spliting_data(csv_path=self.data_transformation_artifacts.transformed_data_path)
            model_architecture = ModelArchitecture()   

            model = model_architecture.get_model()



            logging.info(f"36-Xtrain size is : {x_train.shape}")

            logging.info(f"37-Xtest size is : {x_test.shape}")

            sequences_matrix,tokenizer =self.tokenizing(x_train)


            logging.info("41-Entered into model training")
            model.fit(sequences_matrix, y_train, 
                        batch_size=self.model_trainer_config.BATCH_SIZE, 
                        epochs = self.model_trainer_config.EPOCH, 
                        validation_split=self.model_trainer_config.VALIDATION_SPLIT, 
                        )
            logging.info("42-Model training finished")

            
            with open('tokenizer.pickle', 'wb') as handle:
                pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
            os.makedirs(self.model_trainer_config.TRAINED_MODEL_DIR,exist_ok=True)



            logging.info("43-saving the model")
            model.save(self.model_trainer_config.TRAINED_MODEL_PATH)
            x_test.to_csv(self.model_trainer_config.X_TEST_DATA_PATH)
            y_test.to_csv(self.model_trainer_config.Y_TEST_DATA_PATH)

            x_train.to_csv(self.model_trainer_config.X_TRAIN_DATA_PATH)

            model_trainer_artifacts = ModelTrainerArtifacts(
                trained_model_path = self.model_trainer_config.TRAINED_MODEL_PATH,
                x_test_path = self.model_trainer_config.X_TEST_DATA_PATH,
                y_test_path = self.model_trainer_config.Y_TEST_DATA_PATH)
            logging.info("44-Returning the ModelTrainerArtifacts")
            return model_trainer_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e