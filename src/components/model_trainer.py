from src.entity.artifact_entity import DataTransformationArtifact,RegressionMetricsArtifact,ModelTrainerArtifact
from src.entity.config_entity import ModelTrainerConfig
from src.exception import MyException
import sys
import numpy as np
from typing import Tuple
from src.logger import logging
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error,mean_absolute_percentage_error
from src.utils.main_utils import load_numpy_array_data,load_object,save_object
from src.entity.estimator import MyModel


class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,model_trainer_config:ModelTrainerConfig):
        try:
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_config=model_trainer_config

        except Exception as e:
            raise MyException(e,sys)
        
    def get_model_object_and_report(self,train:np.array,test:np.array)->Tuple[object,object]:


        try:
            logging.info("Training DecisionTreeRegressor starts here.")
            x_train,y_train,x_test,y_test=train[:,:-1],train[:,-1],test[:,:-1],test[:,-1]
            logging.info("train_test_split done.")

            #initialize DecisionTreeRegressor
            model=DecisionTreeRegressor()

            #Fit the model
            logging.info('Model Fitting going on.')
            model.fit(x_train,y_train)
            logging.info("model fitting done...")

            #predictions and evaluation metrics
            y_pred=model.predict(x_test)
            MAE=mean_absolute_error(y_test,y_pred)
            RMSE=np.sqrt(mean_squared_error(y_test,y_pred))
            R2_SCORE=r2_score(y_test,y_pred)
            MAPE=mean_absolute_percentage_error(y_test,y_pred)

            #creating metric artifact
            metrics_artifact=RegressionMetricsArtifact(MAE=MAE,
                                                       RMSE=RMSE,
                                                       R2_SCORE=R2_SCORE,
                                                       MAPE=MAPE)


            return model,metrics_artifact
        except Exception as e:
            raise MyException(e,sys) from e
        
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        logging.info("Entered initiate model trainer method of model_trainer class")

        try:
            logging.info("Starting Model-trainer component")
            train_arr=load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)
            test_arr=load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)
            logging.info("train and test_data loaded")

            trained_model,metrics_artifact=self.get_model_object_and_report(train=train_arr,test=test_arr)
            logging.info("trained_model and metrics artifact loaded")

            # load_preprocessing object 
            preprocessing_object=load_object(self.data_transformation_artifact.transformed_obj_file_path)

            # check model r2_score meets expected_threshold
            if r2_score(train_arr[:,-1],trained_model.predict(train_arr[:,:-1]))<self.model_trainer_config.model_trainer_expected_score:
                logging.info('no model found with score above base score')
                raise Exception("No model found with score above base score")
            
            # Save the final model object that includes both preprocessing and the trained model
            logging.info("saving the model as performance is better than previous one")
            my_model=MyModel(preprocessing_object=preprocessing_object,trained_model_object=trained_model)
            save_object(self.model_trainer_config.trained_model_file_path,my_model)
            logging.info("Saved final model object that includes both preprocessing and the trained model")

            model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                                        metrics_artifact=metrics_artifact)
            logging.info("Saved final model object that includes both preprocessing and the trained model")

            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            logging.info("Model Trainer component in training pipeline completed.")
            return model_trainer_artifact
        
        except Exception as e:
            raise MyException(e, sys) from e


        






