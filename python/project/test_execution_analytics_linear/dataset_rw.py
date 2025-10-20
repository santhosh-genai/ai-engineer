import pandas as pd

class DatasetLoader:
    def __init__(self, file_path):
        try:
            self.data = pd.read_csv(file_path)
        except Exception as e:
            print("Error loading dataset:", e)

    def get_data(self):
        return self.data

    def set_data(self, data, file_path):
        self.data = data
        self.data.to_csv(file_path, index=False)
