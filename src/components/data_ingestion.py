from src.entity.config_entity import DataIngestionConfig
from src.exception import MyException
import sys
from pandas import DataFrame
from src.logger import logging
from src.data_access.house_data import HouseData
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from src.entity.artifact_entity import DataIngestionArtifact

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        """
        Initializes the DataIngestion class.

        Args:
            data_ingestion_config (DataIngestionConfig): Configuration for data ingestion.
        """

        try:
            self.data_ingestion_config=data_ingestion_config
        
        except Exception as e:
            raise MyException(e,sys)
        
    def export_data_into_feature_store(self)->DataFrame:
        """
        Exports data from MongoDB to a CSV file and returns it as a pandas DataFrame
        """
        
        try:
            logging.info('Exporting Data From MongoDB')
            my_data=HouseData()
            dataframe=my_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)

            logging.info(f"Shape of dataframe: {dataframe.shape}")
            dir_path=os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"saving exported dataframe into feature store")
            dataframe.to_csv(self.data_ingestion_config.feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise MyException(e,sys)
        
    def split_data_as_train_test(self,dataframe:DataFrame)->None:
        """
        Splits the dataframe in training and testing data
        """
        try:
            logging.info('Splitting of Dataframe starts...')
            train_data,test_data=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info('Splitting of dataframe completed')

            logging.info('Saving of train and test file in ingested dir starts')
            dir_path=os.path.dirname(self.data_ingestion_config.testing_file_path)

            os.makedirs(dir_path,exist_ok=True)
            train_data.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_data.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)

            logging.info('Saving of training and testing data completed')
        except Exception as e:
            raise MyException(e,sys)
        
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        """
        This is the Main function which return DataIngestionArtifact to use in next pipeline component
        """
        try:
            logging.info('Data Ingestion starts...')
            df=self.export_data_into_feature_store()
            logging.info('got the data from mongodb')
            self.split_data_as_train_test(df)

            data_ingestion_artifact=DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            logging.info(f'data_ingestion_artifact: {data_ingestion_artifact}')
            logging.info("Data-Ingestion completed successfully")

            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e,sys)
        
        













        



         
