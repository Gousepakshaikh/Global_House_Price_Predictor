import sys
from src.logger import logging
from src.exception import MyException

from src.components.data_ingestion import DataIngestion



from src.entity.config_entity import DataIngestionConfig



from src.entity.artifact_entity import DataIngestionArtifact




class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()

    
    def start_data_ingetion(self):
        """
        this method is responsible for starting data ingestion component of training pipeline
        """
        try:
            logging.info('starting data ingestion in training pipeline')
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info('start data ingestion completed successfully')
            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e,sys)
        
    
    def run_pipeline(self):
        """
        this method is responsible for running all pipeline components 
        """
        try:
            data_ingestion_artifact=self.start_data_ingetion()


        except Exception as e:
            raise MyException(e, sys)
    


        