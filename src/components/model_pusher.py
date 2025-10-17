from src.entity.config_entity import ModelEvaluationConfig,ModelPusherConfig
from src.entity.artifact_entity import ModelEvaluationArtifact,ModelPusherArtifact
from src.cloud_storage.s3_storage import SimpleStorageService
from src.entity.s3_estimator import HousePriceEstimator
from src.logger import logging
from src.exception import MyException
import sys



class ModelPusher:
    def __init__(self,model_evaluation_artifact:ModelEvaluationArtifact,model_pusher_config:ModelPusherConfig):
        self.s3=SimpleStorageService()
        self.model_evaluation_artifact=model_evaluation_artifact
        self.model_pusher_config=model_pusher_config

        self.houseprice_estimator=HousePriceEstimator(bucket_name=self.model_pusher_config.bucket_name,
                                                      model_path=self.model_pusher_config.s3_model_key_path)
        
    
    def initiate_model_pusher(self)->ModelPusherArtifact:
        logging.info("model_pusher component starts here...")

        try:
            logging.info("Uploading a new model to Blackblaze bucket")
            self.houseprice_estimator.save_model(from_file=self.model_evaluation_artifact.trained_model_path)

            model_pusher_artifact = ModelPusherArtifact(
                bucket_name=self.model_pusher_config.bucket_name,
                s3_model_path=self.model_pusher_config.s3_model_key_path
            )

            logging.info("Uploaded model successfully to Backblaze bucket")
            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            logging.info("Exited initiate_model_pusher method of ModelPusher class")
            
            return model_pusher_artifact
        except Exception as e:
            raise MyException(e, sys) from e
