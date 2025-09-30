import pandas as pd

class Dataset:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_data(self):
        self.data = pd.read_csv(self.filepath)
        return self.data
    
class CovidReport(Dataset):
    def __init__(self, filepath):
        super().__init__(filepath)
        self.data = self.load_data()

    # Summarize Case Counts by Region
        # Display total confirmed, death, and recovered cases for each region.
    def summarize_cases_by_region(self):
        summary = self.data.groupby('WHO Region').agg({
            'Confirmed': 'sum',
            'Deaths': 'sum',
            'Recovered': 'sum',
            'Active': 'sum'
        }).reset_index()
        return summary

    # 2. Filter Low Case Records
    # Exclude entries where confirmed cases are < 10.
    def filter_low_case_records(self):
        self.data = self.data[self.data['Confirmed'] >= 10]
        return self.data
    
    # Identify Region with Highest Confirmed Cases
    def region_with_highest_cases(self):
        region = self.data.groupby('WHO Region')['Confirmed'].sum().idxmax()
        return region
    
if __name__ == "__main__":
    report = CovidReport('c:/Users/2276038/Desktop/Learning/python/assignments/Assignment_week4/country_wise_latest.csv')
    print("COVID-19 Cases Summary by Region:")
    print(report.summarize_cases_by_region())

    print("\nFiltered Data (Confirmed Cases >= 10):")
    print(report.filter_low_case_records())

    print("\nRegion with Highest Confirmed Cases:")
    print(report.region_with_highest_cases())