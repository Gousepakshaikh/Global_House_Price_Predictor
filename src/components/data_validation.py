from src.entity.artifact_entity import DataIngestionArtifact
from src.entity.config_entity import DataValidationConfig
from src.utils.main_utils import read_yaml_file
from src.constants import SCHEMA_FILE_PATH
from src.exception import MyException
import sys
from pandas import DataFrame
import pandas as pd
from src.logger import logging
from src.entity.artifact_entity import DataValidationArtifact
import os
import json

class DataValidation: 
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_config=read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyException(e,sys)
        
    def validate_number_of_columns(self,dataframe:DataFrame)->bool:
        
        try:
            logging.info("validating number of columns...")

            status=len(self.schema_config['columns'])==len(dataframe.columns)
            logging.info(f"Validation of number of columns status:{status}")
            return status
        except Exception as e:
            raise MyException(e,sys)
        
    def is_column_exist(self,dataframe:DataFrame)->bool:
        try:
            dataframe_columns=dataframe.columns
            missing_numerical_columns=[]
            missing_categorical_columns=[]

            for column in self.schema_config['numerical_columns']:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)

            if len(missing_numerical_columns)>0:
                logging.info(f"missing numerical columns: {missing_numerical_columns}")

            for column in self.schema_config['categorical_columns']:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)

            if len(missing_categorical_columns)>0:
                logging.info(f"missing categorical columns: {missing_categorical_columns}")

            return False if len(missing_categorical_columns)>0 or len(missing_numerical_columns)>0 else True
        
        except Exception as e:
            raise MyException(e,sys)
        
    @staticmethod
    def read_data(file_path:str)->DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e,sys)
    
    def initiate_data_validation(self)->DataValidationArtifact:
        """
        Intiates data validation component for the pipeline
        """

        try:
            logging.info("Starting data validation process... Checking missing columns, and data consistency.")

            validation_error_message=""
            train_df,test_df=(DataValidation.read_data(file_path=self.data_ingestion_artifact.train_file_path),
                              DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))
            

            status=self.validate_number_of_columns(dataframe=train_df)
            if not status:
                validation_error_message+="columns are missing in training dataframe"
            
            else:
                logging.info(f"The len status for training data is: {status}")

            status=self.validate_number_of_columns(dataframe=test_df)
            if not status:
                validation_error_message+="columns are missing in testing data"

            else:
                logging.info(f'the len status of the test_data: {status}')

            
            status=self.is_column_exist(dataframe=train_df)
            if not status:
                validation_error_message+=f"columns are missing in train data status:{status}"

            else:
                logging.info("All columns exist in train data")

            status=self.is_column_exist(dataframe=test_df)
            if not status:
                validation_error_message+="Columns are missing in test_data"

            else:
                logging.info("All columns exist in test data")

            
            validation_status=len(validation_error_message)==0

            data_validation_artifact=DataValidationArtifact(validation_status=validation_status,
                                                            message=validation_error_message,
                                                            validation_report_file_path=self.data_validation_config.validation_report_file_path)
            
            report_dir=os.path.dirname(self.data_validation_config.validation_report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            validation_report={
                "validation_status":validation_status,
                "message":validation_error_message.strip()
            }

            with open(self.data_validation_config.validation_report_file_path,'w') as file:
                json.dump(validation_report,file,indent=4)

            
            logging.info("Data validation artifact created and saved to JSON file.")
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            
            return data_validation_artifact
        except Exception as e:
            raise MyException(e, sys) from e


        




