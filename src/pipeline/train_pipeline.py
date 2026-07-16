import sys

from src.logger import logging
from src.exception import CustomException

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

class TrainPipeline:
    def __init__(self):
        pass
    
    def run_pipeline(self):
        try:
            logging.info("The training pipeline has been initiated")

            data_ingestion = DataIngestion()
            train_data, test_data = data_ingestion.initiate_data_ingestion()
            
            data_transformation = DataTransformation()
            train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data)
            
            model_trainer = ModelTrainer()
            r2_square = model_trainer.initiate_model_trainer(train_arr, test_arr)
            
            logging.info(f"Training pipeline completed. Best R2 score: {r2_square}")
            return r2_square

        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == "__main__":
    pipeline = TrainPipeline()
    score = pipeline.run_pipeline()
    print(f"Training complete. Test R2 score: {score:.4f}")