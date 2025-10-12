from datetime import datetime
from dataclasses import dataclass
import os
from src.constants import *

time_stamp:str=datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

@dataclass
class TrainingPipelineConfig:
    pipeline_name:str=PIPELINE_NAME
    artifact_dir:str=os.path.join(ARTIFACT_DIR,time_stamp)
    timestamp=time_stamp 

training_pipeline_config:TrainingPipelineConfig=TrainingPipelineConfig()

@dataclass
class DataIngestionConfig:
    data_ingestion_dir:str=os.path.join(training_pipeline_config.artifact_dir,DATA_INGESTION_DIR_NAME)
    feature_store_file_path:str=os.path.join(data_ingestion_dir,DATA_INGESTION_FEATURE_STORE_DIR,FILE_NAME)
    training_file_path:str=os.path.join(data_ingestion_dir,DATA_INGESTION_INGESTED_DIR,TRAINING_FILE_NAME)
    testing_file_path:str=os.path.join(data_ingestion_dir,DATA_INGESTION_INGESTED_DIR,TESTING_FILE_NAME)
    train_test_split_ratio:float=DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    collection_name:str=DATA_INGESTION_COLLECTION_NAME

@dataclass
class DataValidationConfig:
    data_validation_dir:str=os.path.join(training_pipeline_config.artifact_dir,DATA_VALIDATION_DIR_NAME)
    validation_report_file_path:str=os.path.join(data_validation_dir,DATA_VALIDATION_REPORT_FILE_NAME)

    



