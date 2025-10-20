import os
from dotenv import load_dotenv
from dataset_cleaning import CleanedData
from sklearn.preprocessing import StandardScaler

# Load environment variables
load_dotenv()

class DataScaler(CleanedData):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.scaler = StandardScaler()

    def scale_data(self, data):
       try:
           data_scaled = data.copy()
           columns = data_scaled.select_dtypes(include=['float64', 'int64']).columns
           data_scaled[columns] = self.scaler.fit_transform(data_scaled[columns])
       except Exception as e:
           print("Error scaling data:", e)

       return data_scaled
    
if __name__ == "__main__":
    raw_data_path = os.getenv('RAW_DATASET_PATH')
    cleaned_data_path = os.getenv('CLEANED_DATASET_PATH')
    scaled_data_path = os.getenv('SCALED_DATASET_PATH')

    if not raw_data_path or not cleaned_data_path or not scaled_data_path:
        print("Environment variables RAW_DATASET_PATH, CLEANED_DATASET_PATH, and SCALED_DATASET_PATH must be set")

    data_scaler = DataScaler(raw_data_path)
    print("Loaded raw data successfully.\n")

    cleaned_data_without_blanks = data_scaler.fill_missing_values()
    print("Completed filling missing values.\n")

    columns = ['Test_Case_Count', 'Code_Churn', 'Execution_Time_Previous']
    cleaned_data_without_outliers = data_scaler.remove_outliers(cleaned_data_without_blanks, columns)
    print("Completed removing outliers.\n")

    data_scaler.set_data(cleaned_data_without_outliers, cleaned_data_path)
    print("Cleaned data saved successfully.\n")

    scaled_data = data_scaler.scale_data(cleaned_data_without_outliers)
    print("Completed scaling data.\n")

    data_scaler.set_data(scaled_data, scaled_data_path)
    print("Scaled data saved successfully.\n")
