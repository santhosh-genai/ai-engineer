import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

# load dataset
df = pd.read_csv('C:\\Users\\2276038\\Desktop\\learning\\ai-engineer\\python\\classes\\machine_learning\\decision_tree_regression_model\\decisiontree.csv')
df = df.dropna()

# encode categorical variables
le_dic = {}
for column in df.columns:
    if df[column].dtype == 'object':
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        le_dic[column] = le

# split features and target
X = df.drop(['Day', 'Play'], axis=1)
y = df['Play']

model = DecisionTreeClassifier(criterion='entropy', max_depth=3)
model.fit(X, y)

# visualize the decision tree
plt.figure(figsize=(12,12))
plot_tree(model, feature_names=X.columns, class_names=le_dic['Play'].classes_, filled=True, fontsize=12)
plt.title('Decision Tree for Play Prediction')
plt.show()

def predict_play(weather, temp, humidity, wind):
    w = le_dic['Weather'].transform([weather])[0]
    t = le_dic['Temperature'].transform([temp])[0]
    h = le_dic['Humidity'].transform([humidity])[0]
    wi = le_dic['Wind'].transform([wind])[0]
    input_data = pd.DataFrame([[w, t, h, wi]], columns=X.columns)
    prediction = model.predict(input_data)[0]
    return le_dic['Play'].inverse_transform([prediction])[0]

# Example prediction
print(predict_play('Sunny', 'Hot', 'Normal', 'Weak'))  # Output: 'Yes' based on the model
print(predict_play('Rain', 'Mild', 'High', 'Strong'))  # Output: 'No' based on the model