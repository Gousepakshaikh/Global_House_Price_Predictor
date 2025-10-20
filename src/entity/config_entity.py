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

@dataclass
class DataTransformationConfig:
    data_transformation_dir:str=os.path.join(training_pipeline_config.artifact_dir,DATA_TRANSFORMATION_DIR_NAME)
    transformed_obj_file_path:str=os.path.join(data_transformation_dir,DATA_TRANSFORMATION_TRANSFORMED_OBJ_DIR,PREPROCESSING_OBJ_FILE_NAME)
    transformed_train_file_path:str=os.path.join(data_transformation_dir,DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,TRAINING_FILE_NAME.replace('csv','npy'))
    transformed_test_file_path:str=os.path.join(data_transformation_dir,DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,TESTING_FILE_NAME.replace('csv','npy'))

@dataclass
class ModelTrainerConfig:
    model_trainer_dir:str=os.path.join(training_pipeline_config.artifact_dir,MODEL_TRAINER_DIR_NAME)
    trained_model_file_path:str=os.path.join(model_trainer_dir,MODEL_TRAINER_TRAINED_MODEL_DIR,MODEL_TRAINER_TRAINED_MODEL_NAME)
    model_trainer_expected_score:float=0.6
    model_config_file_path:str=MODEL_TRAINER_MODEL_CONFIG_FILE_PATH
    model_config_replace:bool=MODEL_TRAINER_MODEL_CONFIG_REPLACE

@dataclass
class ModelEvaluationConfig:
    changed_threshold_score:float=MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE
    bucket_name:str=MODEL_BUCKET_NAME
    s3_model_key_path:str=MODEL_FILE_NAME

@dataclass
class ModelPusherConfig:
    bucket_name:str=MODEL_BUCKET_NAME
    s3_model_key_path:str=MODEL_FILE_NAME

@dataclass 
class HousePredictorConfig:
    model_file_path:str=MODEL_FILE_NAME
    model_bucket_name:str=MODEL_BUCKET_NAME

    

