import numpy as np
from dataset_rw import DatasetLoader

class CleanedData(DatasetLoader):
    def __init__(self, file_path):
        super().__init__(file_path)
        

    # Fill missing values with mean
    def fill_missing_values(self):
        try:
            data = self.get_data()
            data_cleaned = data.copy()
            numeric_columns = data_cleaned.select_dtypes(include=[np.number]).columns
            for col in numeric_columns:
                mean = data_cleaned[col].mean()
                data_cleaned[col] = data_cleaned[col].fillna(mean)

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