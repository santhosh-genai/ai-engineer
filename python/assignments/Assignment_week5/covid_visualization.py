import covid_report_pandas as cr
import matplotlib.pyplot as plt

class covid_visualization(cr.CovidReport):
    def __init__(self, file_path):
        super().__init__(file_path)
