import pandas as pd
from sklearn.preprocessing import StandardScaler

class CovidEDA:
    def __init__(self, file_path):
        self.file_path = file_path

    def _load_data(self):
        data = pd.read_csv(self.file_path)
        data = data[['Confirmed', 'New cases']]
        print("Data loaded successfully.\n", data)
        return data

    # Compute Statistical Measures
        # Calculate and print:
        # Mean
        # Median
        # Variance
        # Standard Deviation
        # Correlation Matrix (between Confirmed and New cases)

    def compute_statistical_measures(self, data):
        print("Statistical Measures:\n")
        print("Mean:\n", data.mean())
        print("\nMedian:\n", data.median()) 
        print("\nVariance:\n", data.var())
        print("\nStandard Deviation:\n", data.std())
        print("\nCorrelation:\n", data.corr())

        # IQR Method for Outlier Detection
        # Calculate Q1 (25th percentile) and Q3 (75th percentile)
        # Calculate IQR (Interquartile Range)
        # Determine lower and upper bounds for outliers
        # Identify outliers
        # Remove outliers and create a cleaned dataset

        # Q1 = data['Total Amount'].quantile(0.25)
        # Q3 = data['Total Amount'].quantile(0.75)
        # IQR = Q3 - Q1

        # lower_bound = Q1 - 1.5 * IQR
        # upper_bound = Q3 + 1.5 * IQR

    def outlier_detection(self, data):
        confirmed_q1 = data['Confirmed'].quantile(0.25)
        confirmed_q3 = data['Confirmed'].quantile(0.75)
        confirmed_iqr = confirmed_q3 - confirmed_q1

        new_cases_q1 = data['New cases'].quantile(0.25)
        new_cases_q3 = data['New cases'].quantile(0.75)
        new_cases_iqr = new_cases_q3 - new_cases_q1

        confirmed_iqr_lower_bound = confirmed_q1 - 1.5 * confirmed_iqr
        confirmed_iqr_upper_bound = confirmed_q3 + 1.5 * confirmed_iqr

        new_cases_iqr_lower_bound = new_cases_q1 - 1.5 * new_cases_iqr
        new_cases_iqr_upper_bound = new_cases_q3 + 1.5 * new_cases_iqr

        print("Outlier Detection Results:")
        print("\nConfirmed Cases:")
        print("Lower Bound:", confirmed_iqr_lower_bound)
        print("Upper Bound:", confirmed_iqr_upper_bound)

        print("\nNew Cases:")
        print("Lower Bound:", new_cases_iqr_lower_bound)
        print("Upper Bound:", new_cases_iqr_upper_bound)

        cleaned_data = data[(data['Confirmed'] >= confirmed_iqr_lower_bound) & (data['Confirmed'] <= confirmed_iqr_upper_bound) &
                            (data['New cases'] >= new_cases_iqr_lower_bound) & (data['New cases'] <= new_cases_iqr_upper_bound)]
        
        print("\nCleaned Data for Confirmed and New Cases:")
        print(cleaned_data)
        cleaned_data.to_csv('c:/Users/2276038/Desktop/Learning/python/assignments/Assignment_week6/Cleaned_CovidDataset.csv', index=False)

        # Normalization using Standard Scaler
            # Apply StandardScaler from sklearn.preprocessing to normalize the
            # Confirmed and New Cases.
            # Display the scaled (normalized) output as a new DataFrame.
    def normalization_scalar_standardization(self, data):
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data)
        scaled_df = pd.DataFrame(scaled_data, columns=data.columns) 
        print("\nScaled Data:\n", scaled_df)
        

report = CovidEDA('c:/Users/2276038/Desktop/Learning/python/assignments/Assignment_week6/country_wise_latest.csv')
data = report._load_data()
report.compute_statistical_measures(data)
report.outlier_detection(data)
report.normalization_scalar_standardization(data)