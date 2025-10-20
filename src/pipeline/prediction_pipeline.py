
from src.exception import MyException
import sys
from pandas import DataFrame
from src.logger import logging
from src.entity.config_entity import HousePredictorConfig
from src.entity.s3_estimator import HousePriceEstimator

class HouseData:
    def __init__(self,
                 country,
                 property_type,
                 furnishing_status,
                 property_size_sqft,
                 previous_owners,
                 rooms,
                 bathrooms,
                 garden,
                 monthly_expenses,
                 neighbourhood_rating):
        try:
            self.country=country
            self.property_type=property_type
            self.furnishing_status=furnishing_status
            self.property_size_sqft=property_size_sqft
            self.previous_owners=previous_owners
            self.rooms=rooms
            self.bathrooms=bathrooms
            self.garden=garden
            self.monthly_expenses=monthly_expenses
            self.neighbourhood_rating=neighbourhood_rating

        except Exception as e:
            raise MyException(e,sys)
        
    
    def get_house_data_as_dict(self):

        try:
            input_data = {
                "country": [self.country],
                "property_type": [self.property_type],
                "furnishing_status": [self.furnishing_status],
                "property_size_sqft": [self.property_size_sqft],
                "previous_owners": [self.previous_owners],
                "rooms": [self.rooms],
                "bathrooms": [self.bathrooms],
                "garden": [self.garden],
                "monthly_expenses": [self.monthly_expenses],
                "neighbourhood_rating": [self.neighbourhood_rating]
            }

            logging.info("created house data as dict")
            
            return input_data
        
        except Exception as e:
            raise MyException(e, sys)
        
    def get_house_input_data_frame(self)->DataFrame:
        """
        This function returns a DataFrame from housedata class input
        """
        try:
            house_input_dict=self.get_house_data_as_dict()
            return DataFrame(house_input_dict)
        
        except Exception as e:
            raise MyException(e, sys)
        
class HousePricePredictor:
    def __init__(self,prediction_pipeline_config:HousePredictorConfig=HousePredictorConfig(),)->None:

        try:
            self.prediction_pipeline_config=prediction_pipeline_config
        
        except Exception as e:
            raise MyException(e, sys)
        

    def predict(self,dataframe:DataFrame):
        """
        This is the method of HousePricePredictor
        Returns: Prediction 
        """
        try:
            logging.info("Entered predict method of HousePricePredict class")  

            model=HousePriceEstimator(bucket_name=self.prediction_pipeline_config.model_bucket_name,
                                      model_path=self.prediction_pipeline_config.model_file_path)
            
            result=model.predict(dataframe=dataframe)
            return result
        
        except Exception as e:
            raise MyException(e, sys)
        
        
        



    
        