from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import DATABASE_NAME
from src.exception import MyException
import sys
from typing import Optional
import pandas as pd
from src.logger import logging
import numpy as np


class HouseData:
    """
    HouseData class fetches records from MongoDB and returns them as a pandas DataFrame.
    """

    def __init__(self):
        """
        Initializes the mongodb client connection
        """
        try:
            self.mongo_client=MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise MyException(e,sys)
        
    def export_collection_as_dataframe(self,collection_name:str,database_name:Optional[str]=None)->pd.DataFrame:
        try:
            if database_name is None:
                collection=self.mongo_client.database[collection_name]
            else:
                collection=self.mongo_client[database_name][collection_name]

            logging.info("Featching data from mongodb...")

            # convert collection to dataframe
            df=pd.DataFrame(list(collection.find()))
            logging.info(f"Data fetched with len: {len(df)}")

            if "_id" in df.columns.to_list():
                df=df.drop(columns=['_id'],axis=1)
            df.replace({'na':np.nan,'NA':np.nan},inplace=True)

            return df
        except Exception as e:
            raise MyException(e,sys)



