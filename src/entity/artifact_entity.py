from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_file_path:str
    test_file_path:str 

@dataclass
class DataValidationArtifact:
    validation_status:bool
    message:str
    validation_report_file_path:str

@dataclass
class DataTransformationArtifact:
    transformed_obj_file_path:str 
    transformed_train_file_path:str
    transformed_test_file_path:str

@dataclass
class RegressionMetricsArtifact:
    MAE:float
    MSE:float
    R2_SCORE:float
    MAPE:float

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path:str
    metrics_artifact:RegressionMetricsArtifact

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    changed_r2_score:float
    s3_model_path:str
    trained_model_path:str






    