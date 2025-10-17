from dataclasses import dataclass
from src.entity.config_entity import ModelEvaluationConfig
from src.entity.artifact_entity import ModelTrainerArtifact,DataIngestionArtifact,ModelEvaluationArtifact
from src.exception import MyException
import sys
from typing import Optional
from src.entity.s3_estimator import HousePriceEstimator
from src.logger import logging
from src.constants import SCHEMA_FILE_PATH
from src.utils.main_utils import read_yaml_file,load_object
import pandas as pd
from src.constants import TARGET_COLUMN
from sklearn.metrics import r2_score




@dataclass
class EvaluationModelResponse:
    trained_model_r2_score:float
    best_model_r2_score:float
    is_model_accepted:bool
    difference:float


class ModelEvaluation:
    def __init__(self,model_eval_config:ModelEvaluationConfig,model_trainer_artifact:ModelTrainerArtifact,
                 data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.model_eval_config=model_eval_config
            self.model_trainer_artifact=model_trainer_artifact
            self.data_ingestion_artifact=data_ingestion_artifact

        except Exception as e:
            raise MyException(e,sys)
        
    def get_best_model(self)->Optional[HousePriceEstimator]:
        try:
            bucket_name=self.model_eval_config.bucket_name
            model_path=self.model_eval_config.s3_model_key_path
            house_price_estimator=HousePriceEstimator(bucket_name=bucket_name,model_path=model_path)

            if house_price_estimator.is_model_present(model_path=model_path):
                return house_price_estimator
            return None
        except Exception as e:
            raise MyException(e, sys) from e
        
    def drop_id_column(self,df):
        logging.info("Dropping _id column")

        if "_id" in df.columns:
            df=df.drop(columns=['_id'],axis=1)
            logging.info("_df column dropped")
        return df
    
    def drop_columns(self,df):
        
        file=read_yaml_file(SCHEMA_FILE_PATH)
        drop_columns=file['drop_columns']

        df=df.drop(columns=drop_columns,axis=1)
        return df
    
    def evaluate_model(self)->EvaluationModelResponse:

        try:
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)

            x,y=test_df.drop(columns=[TARGET_COLUMN],axis=1),test_df[TARGET_COLUMN]
            logging.info("test data loaded now transforming for prediction")
            x=self.drop_id_column(x)
            x=self.drop_columns(x)

            trained_model=load_object(self.model_trainer_artifact.trained_model_file_path)
            logging.info("Trained_model loaded successfully")
            trained_model_preds=trained_model.predict(x)
            trained_model_r2_score=r2_score(y,trained_model_preds)
            logging.info(f'Trained model r2_score is: {trained_model_r2_score}')


            best_model_r2_score=None
            best_model=self.get_best_model()

            if best_model is not None:
                best_model_preds=best_model.predict(x)
                logging.info(f"Computing r2_Score for production model..")
                best_model_r2_score=r2_score(y,best_model_preds)

                logging.info(f"r2_Score-Production Model: {best_model_r2_score}, r2_Score-New Trained Model: {trained_model_r2_score}")

            tmp_best_model_score=0 if best_model_r2_score is None else best_model_r2_score
            result=EvaluationModelResponse(
                trained_model_r2_score=trained_model_r2_score,
                best_model_r2_score=best_model_r2_score,
                is_model_accepted=trained_model_r2_score>tmp_best_model_score,
                difference=trained_model_r2_score-tmp_best_model_score,
            )

            logging.info(f"Result: {result}")
            return result

        except Exception as e:
            raise MyException(e, sys)
        
    def initiate_model_evaluation(self)->ModelEvaluationArtifact:

        try:
            logging.info("Model evaluation starts here...")
            evaluate_model_response=self.evaluate_model()
            s3_model_path=self.model_eval_config.s3_model_key_path

            model_evaluation_artifact=ModelEvaluationArtifact(
                is_model_accepted=evaluate_model_response.is_model_accepted,
                s3_model_path=s3_model_path,
                changed_r2_score=evaluate_model_response.difference,
                trained_model_path=self.model_trainer_artifact.trained_model_file_path
            )

            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            logging.info(f'Model evaluation completed...')
            return model_evaluation_artifact
        except Exception as e:
            raise MyException(e, sys) from e
        




            

            


            




    
    
    

    


        
