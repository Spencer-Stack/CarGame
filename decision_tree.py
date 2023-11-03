import pandas as pd

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn


from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


class BinaryClassifierModel:
    def __init__(self):
        self.model = DecisionTreeClassifier()

    def train(self, feature_file, label_file):
        """
        Train the model and evaluate training and testing accuracy.

        feature_file: CSV file with feature data (n x 30)
        label_file: CSV file with label data (n x 2)
        """
        X = pd.read_csv(feature_file)
        y = pd.read_csv(label_file)

        # Split the data into a training set and a testing set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model on the training set
        self.model.fit(X_train, y_train)

        # Make predictions on the training set and testing set
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)

        # Calculate training and testing accuracy
        train_accuracy = accuracy_score(y_train, y_train_pred)
        test_accuracy = accuracy_score(y_test, y_test_pred)

        print("Training Accuracy: {:.2f}%".format(train_accuracy * 100))
        print("Testing Accuracy: {:.2f}%".format(test_accuracy * 100))

    def predict(self, X):
        """
        Predict binary values for input data.

        X: List of feature vectors (n x 30)

        Returns: List of predicted binary values (n x 2)
        """
        return self.model.predict(X)

    def start(self):
        # Train the model using CSV files and evaluate accuracy
        feature_file = 'distances.csv'
        label_file = 'actions.csv'
        self.train(feature_file, label_file)


