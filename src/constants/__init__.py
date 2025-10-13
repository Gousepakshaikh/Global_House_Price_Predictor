import os

# MongoDB
DATABASE_NAME:str="House"
MONGODB_URL_KEY:str="MONGODB_URL"
COLLECTION_NAME:str="House-Data"

# Pipeline
PIPELINE_NAME:str=""
ARTIFACT_DIR:str="Artifact"

# dataset
FILE_NAME:str="data.csv"
TRAINING_FILE_NAME:str="train.csv"
TESTING_FILE_NAME:str="test.csv"
SCHEMA_FILE_PATH:str=os.path.join("config","schema.yaml")

# Data-Ingetion 
DATA_INGESTION_COLLECTION_NAME:str="House-Data"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str="feature-store"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.25

# Data-Validation
DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_REPORT_FILE_NAME:str="Report.yaml"

# Data-Transformation
DATA_TRANSFORMATION_DIR_NAME:str="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_OBJ_DIR:str="transformed_obj"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str="transformed_data"

# Model
PREPROCESSING_OBJ_FILE_NAME:str="preprocessing.pkl"
TARGET_COLUMN:str="price"

