# %%
import covid_report_pandas as cr
import matplotlib.pyplot as plt

class covid_visualization(cr.CovidReport):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.data = self.load_data()

    # Bar Chart of Top 5 Countries by Confirmed Cases
    def plot_top_5_countries_by_case_count(self):
        data = super().top_5_countries_by_case_count()
        plt.bar(data['Country/Region'], data['Confirmed'], color='blue')
        plt.xlabel('Country/Region')
        plt.ylabel('Confirmed Cases')
        plt.title('Top 5 Countries by Confirmed COVID-19 Cases')
        plt.show()

    # Pie Chart of Death Distribution by Region
    def plot_summarize_cases_by_region(self):
        data = super().summarize_cases_by_region()
        plt.pie(data['Deaths'], labels=data['WHO Region'], autopct='%1.1f%%')
        plt.title('Death Distribution by Region')
        plt.show()
        
    # Line Chart comparing Confirmed and Deaths for Top 5 Countries
    def plot_line_confirmed_deaths_by_region(self):
        data = super().summarize_cases_by_region()
        plt.plot(data['WHO Region'], data['Confirmed'], marker='o', color='blue')
        plt.plot(data['WHO Region'], data['Deaths'], marker='o', color='red')
        plt.xticks(rotation=45)
        plt.xlabel('WHO Region')
        plt.grid()
        plt.ylabel('Cases')
        plt.yscale('log')
        plt.title('Confirmed and Death Cases by Region')
        plt.legend(['Confirmed', 'Deaths'])
        plt.show()

# %%
if __name__ == "__main__":
    file_path = 'c:/Users/2276038/Desktop/Learning/python/assignments/Assignment_week5/country_wise_latest.csv'
    report = covid_visualization(file_path)
report.plot_top_5_countries_by_case_count()
report.plot_summarize_cases_by_region()
report.plot_line_confirmed_deaths_by_region()
