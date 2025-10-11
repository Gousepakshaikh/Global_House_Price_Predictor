import certifi
from src.constants import DATABASE_NAME,MONGODB_URL_KEY
import pymongo
import os
from src.logger import logging
from src.exception import MyException
import sys



# load the cirtificate authority file to avoid timeout errors when connecting to mongodb
ca=certifi.where()

class MongoDBClient:
    """
    MongoDBClient establishes connection with MongoDB dataset
    """

    client=None
    def __init__(self,database_name:str=DATABASE_NAME):
        """
        Initializes a connection to the mongodb Database if no existing connection is found
        """
        try:
            if MongoDBClient.client is None:
                mongodb_url=os.getenv(MONGODB_URL_KEY)
                if mongodb_url is None:
                    raise Exception(f"Environment variable named: {MONGODB_URL_KEY} is not set")
                MongoDBClient.client=pymongo.MongoClient(mongodb_url,tlsCAFile=ca)
            self.client=MongoDBClient.client
            self.database=self.client[database_name]
            self.database_name=database_name
            logging.info('MongoDB connection Successful')

        except Exception as e:
            raise MyException(e,sys)

            


    