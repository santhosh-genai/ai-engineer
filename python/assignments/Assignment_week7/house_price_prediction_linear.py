import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

class HousePricePredictionLinear:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_data(self):
        self.data = pd.read_csv(self.filepath)
        return self.data[['Square_Footage', 'House_Price']]
    
    def missing_values(self):
        for col in ['Square_Footage', 'House_Price']:
            mean_value = self.data[col].mean()
            self.data[col] = self.data[col].fillna(mean_value)
        return self.data
if __name__ == "__main__":
    house_price_prediction = HousePricePredictionLinear('C:\\Users\\2276038\\Desktop\\Learning\\python\\assignments\\Assignment_week7\\house_price_regression_dataset.csv')
    data = house_price_prediction.load_data()
    print("House Price Data:\n", data.head())
    cleaned_data = house_price_prediction.missing_values()
    print("Cleaned Data:\n", cleaned_data)
plt.scatter(cleaned_data['Square_Footage'], cleaned_data['House_Price'], color='blue')
plt.title('Square Footage vs House Price') 
plt.xlabel('Square Footage')
plt.ylabel('House Price')
plt.grid()
plt.show()

x=cleaned_data[['Square_Footage']].values
y=cleaned_data['House_Price'].values
xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.2,random_state=42)
model = LinearRegression()
model.fit(xtrain, ytrain)
print("Model Intercept:", model.intercept_)
print("Model Coefficients:", model.coef_)

ypred = model.predict(xtest)
print("Predicted House Prices:", ypred)
print("Mean Squared Error:", mean_squared_error(ytest, ypred))
print("R^2 Score:", r2_score(ytest, ypred))

plt.scatter(xtest, ytest, color='blue', label='Actual Prices')
plt.plot(xtest, ypred, color='red', linewidth=2, label='Predicted Prices')
plt.title('Actual vs Predicted House Prices')
plt.xlabel('Square Footage')
plt.ylabel('House Price')
plt.legend()
plt.grid()
plt.show()

sq_ft = int(input("Enter the square footage of the house to predict its price: "))
ypred = model.predict([[sq_ft]])
print("Predicted House Price for", sq_ft, "sq ft:", ypred)