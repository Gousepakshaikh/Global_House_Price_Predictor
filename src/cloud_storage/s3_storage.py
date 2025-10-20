from src.configuration.backblaze_connection import S3Client
from src.exception import MyException
import sys
from src.logger import logging
from typing import Union,List
from io import StringIO
import pickle
from botocore.exceptions import ClientError
import os
from pandas import DataFrame,read_csv

class SimpleStorageService:

    def __init__(self):
        try:

            s3_client=S3Client()
            self.s3_resource=s3_client.s3_resource
            self.s3_client=s3_client.s3_client
        except Exception as e:
            raise MyException(e,sys)
    def get_bucket(self,bucket_name:str):
        """
        Retrieves the bucket object based on the provided bucket name.
        """
        logging.info("Entered get_bucket method")
        try:
            bucket=self.s3_resource.Bucket(bucket_name)
            return bucket
        except Exception as e:
            raise MyException(e,sys)
        
    def s3_key_path_available(self,bucket_name:str,s3_key:str)->bool:
        """
        Checks if a specified key path (file path) exists in the bucket.
        """

        try: 
            bucket=self.get_bucket(bucket_name)
            file_objects=[file_object for file_object in bucket.objects.filter(Prefix=s3_key)]
            return len(file_objects)>0
        except Exception as e:
            raise MyException(e,sys)
        
    @staticmethod
    def read_object(object_name:str,decode:bool=True,make_readable:bool=False)->Union[StringIO,str]:
        """
        Reads the specified object with optional decoding and conversion to StringIO.
        """
        try:
            func=(
                lambda:object_name.get()["Body"].read().decode() if decode else object_name.get()["Body"].read()
            )
            conv_func=(
                lambda:StringIO(func()) if make_readable else func()
            )

            return conv_func()
        except Exception as e:
            raise MyException(e,sys)
        
    def get_file_object(self,filename:str,bucket_name:str)->Union[list[object],object]:
        """
        Retrieves the file object(s) from the specified bucket.
        """
        logging.info("Entered the get file obj method")

        try:
            bucket=self.get_bucket(bucket_name=bucket_name)
            file_objects=[file_object for file_object in bucket.objects.filter(Prefix=filename)]
            return file_objects[0] if len(file_objects)==1 else file_objects
        except Exception as e:
            raise MyException(e,sys)
        
        
    def load_model(self,model_name:str,bucket_name:str,model_dir:str=None)->object:
        """
        Loads a serialized model from the specified bucket.
        """

        try:
            model_file=f"{model_dir}/{model_name}" if model_dir else model_name
            file_object=self.get_file_object(filename=model_file,bucket_name=bucket_name)
            model_obj=self.read_object(object_name=file_object,decode=False)
            model=pickle.loads(model_obj)
            logging.info("Production model loaded from bucket.")
            return model
        except Exception as e:
            raise MyException(e, sys) from e
        
    def create_folder(self,folder_name:str,bucket_name:str)->None:
        """
        Creates a folder in the specified bucket.
        """
        logging.info("Entered create_folder method")
        try:
            self.s3_resource.Object(bucket_name,folder_name).load()
        
        except ClientError as e:
            if e.response["Error"]["Code"]=="404":
                folder_obj=folder_name+"/"
                self.s3_client.put_object(Bucket=bucket_name,Key=folder_obj)
        logging.info("Exited create_folder method")

    def upload_file(self, from_filename: str, to_filename: str, bucket_name: str, remove: bool = True) -> None:
        """
        Uploads a local file to the bucket with optional local file deletion.
        """
        try:
            self.s3_resource.meta.client.upload_file(from_filename, bucket_name, to_filename)
            logging.info(f"Uploaded {from_filename} to bucket {bucket_name} as {to_filename}")
            if remove:
                os.remove(from_filename)
                logging.info(f"Local file {from_filename} removed after upload")
        except Exception as e:
            raise MyException(e, sys) from e
        
    def upload_df_as_csv(self, data_frame: DataFrame, local_filename: str, bucket_filename: str, bucket_name: str) -> None:
        """
        Uploads a DataFrame as a CSV file to the bucket.
        """
        logging.info("Entered upload_df_as_csv method")
        try:
            data_frame.to_csv(local_filename, index=None, header=True)
            self.upload_file(local_filename, bucket_filename, bucket_name)
        except Exception as e:
            raise MyException(e, sys) from e

    def get_df_from_object(self, object_: object) -> DataFrame:
        """
        Converts a bucket object to a DataFrame.
        """
        logging.info("Entered get_df_from_object method")
        try:
            content = self.read_object(object_, make_readable=True)
            df = read_csv(content, na_values="na")
            return df
        except Exception as e:
            raise MyException(e, sys) from e

    def read_csv(self, filename: str, bucket_name: str) -> DataFrame:
        """
        Reads a CSV file from the bucket and converts it to a DataFrame.
        """
        logging.info("Entered read_csv method")
        try:
            csv_obj = self.get_file_object(filename, bucket_name)
            df = self.get_df_from_object(csv_obj)
            return df
        except Exception as e:
            raise MyException(e, sys) from e




        

        