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

    # Filter Low Case Records
        # Exclude entries where confirmed cases are < 10.
    def filter_low_case_records(self):
        self.data = self.data[self.data['Confirmed'] >= 10]
        return self.data
    
    # Identify Region with Highest Confirmed Cases
    def region_with_highest_cases(self):
        region = self.data.groupby('WHO Region')['Confirmed'].sum().idxmax()
        return region

    # Sort data by Confirmed Cases and Save to CSV
    def save_sorted_data(self, output_filepath):
        sorted_data = self.data.sort_values(by='Confirmed', ascending=False)
        sorted_data.to_csv(output_filepath, index=False)
        return sorted_data

    # Top 5 Countries by Case Count
    def top_5_countries_by_case_count(self):
        return self.data.sort_values('Confirmed', ascending=False).head(5)[['Country/Region', 'Confirmed']]

    def region_with_lowest_death_count_cases(self):
        region = self.data.groupby('WHO Region')['Deaths'].sum().idxmin()
        return region
    
if __name__ == "__main__":
    report = CovidReport('c:/Users/2276038/Desktop/Learning/python/assignments/Assignment_week4/country_wise_latest.csv')
    print("COVID-19 Cases Summary by Region:")
    print(report.summarize_cases_by_region())

    print("\nFiltered Data (Confirmed Cases >= 10):")
    print(report.filter_low_case_records())

    print("\nRegion with Highest Confirmed Cases:")
    print(report.region_with_highest_cases())

    print("\nSaving sorted data to 'sorted_covid_data.csv'...")
    sorted_data = report.save_sorted_data('c:/Users/2276038/Desktop/Learning/python/assignments/Assignment_week4/sorted_covid_data.csv')
    print("sorted_data:\n", sorted_data)

    print("\nTop 5 Countries by Confirmed Cases:")
    print(report.top_5_countries_by_case_count().to_string(index=False))  # When printing to console    

    print("\nRegion with Lowest Death Count:")
    print(report.region_with_lowest_death_count_cases())