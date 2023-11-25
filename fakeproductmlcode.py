import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

#reading our dataset which contains features and labels whether product is genuine or fake
product_data = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/fake_product_dataset.csv")

#dropping all null values of our dataset
product_data.dropna(inplace=True)

label_map = {'fake': 0, 'genuine': 1}
df = product_data['label'].map(label_map)

plt.scatter(product_data['retail_price'], product_data['discounted_price'], c=df, alpha=0.5)

print(product_data.head())

#defining features and labels of our product
features = product_data[['retail_price', 'discounted_price']]
labels = product_data["label"]

print(features)

#splitting our features and labels into X and y for train and test
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.02)

X_train.head()

y_train.head()

#making our model using Logistic Regression
model = LogisticRegression()

#fitting our X_train and y_train into the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

#getting accuracy percentage of the model
accuracy = model.score(X_test, y_test)*100
print("Model accuracy:", accuracy)

blockchain_verified = True

# Example user input:
user_input = pd.DataFrame(
{
   'retail_price': [100],
   'discounted_price': [40],
})

# Make a prediction
product_genuine = model.predict(user_input)

#Final output using product information in user input
if blockchain_verified and product_genuine:
    print("Product is genuine")
else:
    print("Product is likely fake")