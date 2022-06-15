# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1syd2AkQO3DNxBSu7nKgpFyQgoF4tOClp
"""

# -*- coding: utf-8 -*-
"""BCA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fNBDXJItEZut1UqxNl380lBCk2ADt1dr
"""

## import necessary packages 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import time
from sklearn import metrics


# read the data
data = pd.read_csv("AL21.txt")

# Visualization
data['LOWEST_RATING'].value_counts().sort_values().plot(kind = 'barh')
plt.title("Frequency Distribution of Bridge Condition")
plt.show()

# missing value analysis
percent_missing = data.isnull().sum() / len(data)
missing_value_df = pd.DataFrame({'column_name': data.columns,
                                 'percent_missing': percent_missing})

missing_value_df_above_10percent = missing_value_df[missing_value_df['percent_missing'] > 0.3]
data_drop_feature_with_MV = data.drop(missing_value_df_above_10percent['column_name'], axis = 1)
data_dropMV = data_drop_feature_with_MV.dropna()

data_final = data_dropMV.select_dtypes(exclude= 'object')
print("shape of the preprocessed data", data_final.shape)


# categorization of the target variable 
data_final["LOWEST_RATING"] = np.where(data_final["LOWEST_RATING"] > 5, 0, 1)

#visualization 
data_final["LOWEST_RATING"].value_counts().plot(kind= 'barh')
plt.show()


# separating X and y variable
X = data_final.drop("LOWEST_RATING", axis = 1)
y = data_final["LOWEST_RATING"]
#generating train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, stratify = y)

start_time = time.time()
clf = RandomForestClassifier(n_estimators=50)
clf.fit(X_train, y_train)
pred = clf.predict(X_test)
accuracy_RF = metrics.accuracy_score(y_test, pred)
execution_time =  (time.time() - start_time)
print("--- %s seconds ---" % execution_time)
print("accuracy of the RF model: ", accuracy_RF)


clf = LogisticRegression()
clf.fit(X_train, y_train)
pred = clf.predict(X_test)
accuracy_LR = metrics.accuracy_score(y_test, pred)
print("accuracy of the LR model: ", accuracy_LR)

# write scores to a file 
with open("metrics.txt", 'w') as outfile:
    outfile.write("execution_time: %2.2f \n" % execution_time)
    outfile.write("accuracy: %2.2f%% \n" % accuracy_RF)
    outfile.write("accuracy: %2.2f%%" % accuracy_LR)




