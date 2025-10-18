import pandas as pd
import numpy as np
from dataset import DatasetLoader

class CleanedData(DatasetLoader):
    def __init__(self, file_path):
        super().__init__(file_path)

    # Fill missing values with mean
    def fill_missing_values(self):
        try:
            data = self.get_data()
            data_cleaned = data.copy()

            for col in data_cleaned.select_dtypes(include=[np.number]).columns:
                mean = data_cleaned[col].mean()
                data_cleaned[col].fillna(mean, inplace=True)

        except Exception as e:
            print("Error filling missing values:", e)
        return data_cleaned

    # Remove outliers using IQR method
    def remove_outliers(self, data_cleaned, columns):
        try:
            data_outliers_removed = data_cleaned.copy()
            for column in columns:
                Q1 = data_outliers_removed[column].quantile(0.25)
                Q3 = data_outliers_removed[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                outliers = data_outliers_removed[(data_outliers_removed[column] < lower_bound) | (data_outliers_removed[column] > upper_bound)]
                data_outliers_removed.drop(outliers.index, inplace=True)

        except Exception as e:
            print("Error removing outliers:", e)
        return data_outliers_removed

if __name__ == "__main__":    
    read_file_path = 'c:/Users/2276038/Desktop/Learning/python/project/test_execution_analytics_linear/qa_regression_raw_dataset.csv'
    write_file_path = 'c:/Users/2276038/Desktop/Learning/python/project/test_execution_analytics_linear/qa_regression_cleaned_dataset.csv'
    cleaner = CleanedData(read_file_path)
    data = cleaner.get_data()
    print("Loaded data successfully.\n")

    cleaned_data = cleaner.fill_missing_values()
    print("Completed filling missing values.\n")

    columns = ['Test_Case_Count', 'Code_Churn', 'Execution_Time_Previous']
    cleaned_data = cleaner.remove_outliers(cleaned_data, columns)
    print("Completed removing outliers.\n")

    cleaner.set_data(cleaned_data, write_file_path)
    print("Cleaned data saved successfully.\n")