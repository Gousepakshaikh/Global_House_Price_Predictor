import yaml
from src.exception import MyException
import sys
import os
import dill
import numpy as np


def read_yaml_file(file_path:str)->dict:
    try:
            
        with open(file_path,'rb') as file:
            return yaml.safe_load(file)
    
    except Exception as e:
        raise MyException(e,sys)
    

def write_yaml_file(file_path:str,content:object,replace:bool=False)->None:

    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)

        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as file:
            yaml.dump(content,file)
    
    except Exception as e:
        raise MyException(e,sys)
    
def load_object(file_path:str)->object:
    try:
        with open(file_path,'rb') as file:
            obj=dill.load(file)
        return obj
    
    except Exception as e:
        raise MyException(e,sys)
    
def save_numpy_array_data(file_path:str,array:np.array)->None:
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file:
            np.save(file,array)
    except Exception as e:
        raise MyException(e,sys)
    
def load_numpy_array_data(file_path:str)->np.array:
    try:
        with open(file_path,'rb') as file:
            return np.load(file)
    except Exception as e:
        raise MyException(e,sys)
    
def save_object(file_path:str,object:object)->None:
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,'wb') as file:
            dill.dump(object,file)

    except Exception as e:
        raise MyException(e,sys)
    







