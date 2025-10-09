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

    # Region with Lowest Death Count
    def region_with_lowest_death_count_cases(self):
        region = self.data.groupby('WHO Region')['Deaths'].sum().idxmin()
        return region
    
    # India Case Summary
    def india_case_summary(self):
        return self.data[self.data['Country/Region'] == 'India'].to_string(index=False)
    
    # Mortality Rate by Region
    def mortality_rate_by_region(self):
        region = self.data.groupby('WHO Region')['Deaths'].sum() / self.data.groupby('WHO Region')['Confirmed'].sum() * 100
        return region
    
    # Recovery Rate by Region
    def compare_recovery_rates(self):
        region = self.data.groupby('WHO Region')['Recovered'].sum() / self.data.groupby('WHO Region')['Confirmed'].sum() * 100
        return region

    # Detect Outliers in Case Counts
    def detect_outliers(self):
        mean = self.data['Confirmed'].mean()
        std_dev = self.data['Confirmed'].std()

        threshold_upper = mean + 2 * std_dev
        threshold_lower = mean - 2 * std_dev

        outliers = self.data[(self.data['Confirmed'] > threshold_upper) | (self.data['Confirmed'] < threshold_lower)]
        return outliers
    
    # Group by Country Counts
    def group_by_country(self):
        return self.data.groupby('Country/Region').size().reset_index(name='Counts')
    
    # Countries with Zero Recovered Cases
    def country_with_zero_recovered_cases(self):
        return self.data[self.data['Recovered'] == 0]['Country/Region']

if __name__ == "__main__":
    report = CovidReport('c:/Users/2276038/Desktop/Learning/python/assignments/Assignment_week5/country_wise_latest.csv')
    print("COVID-19 Cases Summary by Region:")
    print(report.summarize_cases_by_region())

    print("\nFiltered Data (Confirmed Cases >= 10):")
    print(report.filter_low_case_records())

    print("\nRegion with Highest Confirmed Cases:")
    print(report.region_with_highest_cases())

    print("\nSaving sorted data to 'sorted_covid_data.csv'...")
    sorted_data = report.save_sorted_data('c:/Users/2276038/Desktop/Learning/python/assignments/Assignment_week5/sorted_covid_data.csv')
    print("sorted_data:\n", sorted_data)

    print("\nTop 5 Countries by Confirmed Cases:")
    print(report.top_5_countries_by_case_count().to_string(index=False))  # When printing to console    

    print("\nRegion with Lowest Death Count:")
    print(report.region_with_lowest_death_count_cases())

    print("\nIndia Case Summary:")
    print(report.india_case_summary())

    print("\nMortality Rate by Region (%):")
    print(report.mortality_rate_by_region())

    print("\nRecovery Rate by Region (%):")
    print(report.compare_recovery_rates())

    print("\nOutliers in Confirmed Cases:")
    print(report.detect_outliers())

    print("\nGroup by Country Counts:")
    print(report.group_by_country())    

    print("\nCountries with Zero Recovered Cases:")
    print(report.country_with_zero_recovered_cases())