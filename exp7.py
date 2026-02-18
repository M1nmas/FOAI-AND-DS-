import pandas as pd 
data=pd.read_csv('data.csv')
print("dataset loaded")
print(data.head())
correlation_matrix=data.corr()
print("\ncorrelation between features: ")
print(correlation_matrix)
correlation_matrix.to_csv("correlation_output.csv")