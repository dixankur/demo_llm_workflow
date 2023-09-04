
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load the dataset
data = pd.read_csv('./data/P001/final_dataset.csv')

# Split the dataset into features and target
X = data.drop(['priority', 'number'], axis=1)
y = data['priority']

# Split the dataset into training and test folds
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train a RandomForest model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Make predictions on the test fold
predictions = model.predict(X_test)

# Save predictions as 'final_predictions' in csv format
final_predictions = pd.DataFrame({'number': X_test['number'], 'priority': predictions})
final_predictions.to_csv('./data/P001/final_predictions.csv', index=False)
