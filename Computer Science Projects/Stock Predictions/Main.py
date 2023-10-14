# import:
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# importing and preparing stock_data sheet
stock_data = pd.read_csv("C:/Users/Omen 15/Desktop/TSLA.csv")
stock_data.head()

# Separating the stock_data into X-axis and Y-axis
X_Axis = stock_data[['High','Low','Open','Volume']].values
Y_Axis = stock_data['Close'].values

# Spliting the data into it's testing and training sets
X_train, X_test, y_train, y_test = train_test_split(X_Axis,Y_Axis, test_size=0.3, random_state=1)

# Creating and training Regression Model
Model = LinearRegression()
Model.fit(X_train, y_train)

#  Printing Coefficient
print(Model.coef_)

# Use model to make predictions
predicted = Model.predict(X_test)
print(predicted)

# Combining both the actual and predicted data value into a table
Actual_Predicted_Table = pd.DataFrame({'Actual': y_test.flatten(), 'Prdicted': predicted.flatten()})
print(Actual_Predicted_Table)

# plotting the graph to see the difference from Actual set and difference set
graph = Actual_Predicted_Table.head(20)
# print(graph.plot(kind='bar'))