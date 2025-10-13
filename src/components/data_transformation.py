from src.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from src.entity.config_entity import DataTransformationConfig
from src.constants import SCHEMA_FILE_PATH,TARGET_COLUMN
from src.utils.main_utils import read_yaml_file,save_object,save_numpy_array_data
from src.exception import MyException
import sys
from pandas import DataFrame
import pandas as pd
from sklearn.pipeline import Pipeline
from src.logger import logging
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import numpy as np

class DataTransformation:

    """
    Responsible for transforming raw data into feature-engineered numerical arrays
    and saving preprocessing artifacts for training and inference.
    """
    
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_transformation_config:DataTransformationConfig,
                 data_validation_artifact:DataValidationArtifact):
        
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
            self.schema_config=read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyException(e,sys)
        
    @staticmethod
    def read_data(file_path)->DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e,sys)
        
    def get_data_transformer_object(self)->Pipeline:
        
        try:
            logging.info("Entered get_data_transformer_object method of DataTransformation class")
            logging.info("Initializing-Transformeres")
            One_Hot_Encoder=OneHotEncoder(drop='first',handle_unknown="ignore")
            logging.info("transformer initialized:OneHotEncoder")

            logging.info('loading columns for one hot incoding')
            ohe_features=self.schema_config["ohe_features"]
            logging.info(f"Ohe-features are:[{ohe_features}]")

            # creating preprocessor pipeline 
            preprocessor=ColumnTransformer(
                transformers=[
                    ("ohe",One_Hot_Encoder,ohe_features)
                ],remainder='passthrough'
            )

            logging.info('wrapping everything in single pipeline')
            final_pipeline=Pipeline(steps=[('preprocessor',preprocessor)])
            logging.info('final pipeline ready')
            return final_pipeline
        except Exception as e:
            raise MyException(e,sys)
        
    def drop_columns(self,df):

        """
        Loads unimportant columns from schema config and drops them safely.
        """

        try:
            logging.info("Dropping useless columns as per schema configuration...")
            drop_cols=self.schema_config.get('drop_columns',[])

            # only that columns exist in df 
            valid_drop_cols=[col for col in drop_cols if col in df.columns]

            if valid_drop_cols:
                logging.info(f"dropping columns: {valid_drop_cols}")
                df=df.drop(columns=valid_drop_cols,axis=1)
            
            else:
                logging.info("no matching column found to drop")

            return df
        
        except Exception as e:
            logging.error("error occurred while dropping columns")
            raise MyException(e,sys)
        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        """
        Initiates the data transformation component for the pipeline.
        """
        try:
            logging.info("Feature Transformation Starts here")
            if not self.data_validation_artifact.validation_status:
                raise Exception(self.data_validation_artifact.message)
            
            #load train and test data
            train_df=self.read_data(self.data_ingestion_artifact.train_file_path)
            test_df=self.read_data(self.data_ingestion_artifact.test_file_path)
            logging.info('Data loaded Successfully')

            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]

            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            logging.info("input_features and target features are  defined")

            input_feature_train_df=self.drop_columns(input_feature_train_df)
            input_feature_test_df=self.drop_columns(input_feature_test_df)

            logging.info("OneHotEncoding is started....")
            preprocessor=self.get_data_transformer_object()
            input_feature_train_arr=preprocessor.fit_transform(input_feature_train_df)
            logging.info("input_feature_train_df encoding is completed")
            input_feature_test_arr=preprocessor.transform(input_feature_test_df)
            logging.info("input_feature_test_df encoding is completed")

            train_arr=np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr=np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            logging.info("saving of obj and transformed-data starts here")
            save_object(self.data_transformation_config.transformed_obj_file_path,preprocessor)
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)

            logging.info("Saving of obj and tranformed train_test data saved")
            logging.info("Data-transformation completed successfully...")
            return DataTransformationArtifact(
                transformed_obj_file_path=self.data_transformation_config.transformed_obj_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            
        except Exception as e:
            raise MyException(e, sys) from e
            








         
    

        

        
        
            








    