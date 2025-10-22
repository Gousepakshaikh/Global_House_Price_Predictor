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
MODEL_FILE_NAME="model.pkl"

# Model_Trainer
MODEL_TRAINER_DIR_NAME:str="model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str="trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str="model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float=0.6
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH:str=os.path.join("config","model.yaml")
MODEL_TRAINER_MODEL_CONFIG_REPLACE:bool=True

# Blackblaze
S3_ACCESS_KEY_ID_ENV_KEY:str="S3_ACCESS_KEY_ID"
S3_SECRET_ACCESS_KEY_ENV_KEY:str="S3_SECRET_ACCESS_KEY"
ENDPOINT_URL="https://s3.us-east-005.backblazeb2.com"

# Model Evaluation
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE:float=0.02
MODEL_BUCKET_NAME:str="House-Bucket"
MODEL_PUSHER_S3_KEY:str="model_registry"

# app
APP_HOST="0.0.0.0"
APP_PORT = int(os.environ.get("PORT", 5000))





