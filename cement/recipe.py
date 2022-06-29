import warnings
import pandas as pd
warnings.simplefilter(action='ignore', category=FutureWarning) #annoying warning in pandas
pd.options.mode.chained_assignment = None #annoying warning in pandas
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn import linear_model
from sklearn import preprocessing
from itertools import product
import matplotlib.pyplot as plt

df=pd.read_csv('concrete-data.csv')
#df=df[df['Age']==28]
#separate result data
y=df['MPa']

#remove age and Mpa columns for just materials
mat_cols=df.columns[:-1]
materials=df[mat_cols]
materials.columns=list(map(str,range(len(mat_cols))))
num_cols=materials.columns
#materials = materials.apply(zscore)
#generate interaction columns
col1=num_cols
col2=num_cols
col3=num_cols
for i in product(col1, col2, col3):
    name="*".join(i)
    materials[name]=materials[list(i)].prod(axis=1)
x=materials.copy()
#normalize data
#x=preprocessing.normalize(x,norm='l1')

#split into test and train data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(x_train, y_train)

y_pred = regr.predict(x_test)
# The coefficients
print("Coefficients: \n", regr.coef_)
# The mean squared error
print("Mean absolute error: %.2f MPa" % mean_absolute_error(y_test, y_pred))
# The coefficient of determination: 1 is perfect prediction
print("Coefficient of determination: %.2f" % r2_score(y_test, y_pred))

# Plot outputs
plt.scatter(y_pred, y_test, color="black")
plt.xticks(())
plt.yticks(())

plt.show()