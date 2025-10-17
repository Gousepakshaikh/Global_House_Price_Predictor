from src.cloud_storage.s3_storage import SimpleStorageService
from src.exception import MyException
from src.entity.estimator import MyModel
import sys
from pandas import DataFrame


class HousePriceEstimator:
    """
    This class is used to save and retrieve our model from Backblaze bucket and to do prediction
    """
    def __init__(self,bucket_name:str,model_path):
        """
        :param bucket_name: Name of your Backblaze model bucket
        :param model_path: Location of your model in bucket
        """
        self.bucket_name=bucket_name
        self.s3=SimpleStorageService()
        self.model_path=model_path
        self.loaded_model:MyModel=None


    def is_model_present(self,model_path):
        """
        Check if a model exists in the Backblaze bucket.
        """

        try:
            self.s3.s3_key_path_available(bucket_name=self.bucket_name,s3_key=model_path)
        except Exception as e:
            print(e)
            return False
    
    def load_model(self)->MyModel:

        """
        loads the model from backblaze
        """
        return self.s3.load_model(model_name=self.model_path,bucket_name=self.bucket_name)
    
    def save_model(self,from_file,remove:bool=False)->None:
        """
        Save the model to the Backblaze bucket.
        :param from_file: Path to the model file locally
        :param remove: If True, remove the local copy after upload
        """

        try:
            self.s3.upload_file(from_filename=from_file,to_filename=self.model_path,bucket_name=self.bucket_name,remove=remove)
        except Exception as e:
            raise MyException(e,sys)
        
    def predict(self,dataframe:DataFrame):
        """
        Make predictions using the loaded model.
        """
        try:
            if self.loaded_model is None:
                self.loaded_model=self.load_model()
            return self.loaded_model.predict(dataframe=dataframe)
        except Exception as e:
            raise MyException(e,sys)
         



