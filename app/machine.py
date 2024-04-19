from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
import joblib
import datetime


class Machine:
    """
    Machine class encapsulating a RandomForestClassifier for predicting
    the 'Rarity' of data instances based on their features.
    """

    def __init__(self, df: DataFrame):
        """
        Initializes the Machine with a RandomForestClassifier trained on the provided DataFrame.

        :param df: A DataFrame containing the feature set and target 'Rarity'.
        """
        self.name = "Random Forest Classifier"
        target = df["Rarity"]
        features = df.drop(columns=["Rarity"])
        self.model = RandomForestClassifier(
            max_depth=10, random_state=42, n_estimators=75)
        self.model.fit(features, target)
        self.timestamp = datetime.datetime.now()

    def __call__(self, feature_basis: DataFrame):
        """
        Makes a prediction on the basis of provided features and returns the prediction
        along with the maximum confidence score for that prediction.

        :param feature_basis: A DataFrame containing the features for prediction.
        :return: A tuple containing the predictions and their maximum confidence scores.
        """
        predictions = self.model.predict(feature_basis)
        confidences = self.model.predict_proba(feature_basis)
        max_confidences = [max(confidence) for confidence in confidences]
        return predictions, max_confidences

    def save(self, filepath: str):
        """
        Saves the Machine instance to a file using joblib.

        :param filepath: The path to the file where the instance should be saved.
        :return: The result of the joblib.dump() operation.
        """
        return joblib.dump(self, filepath)

    @staticmethod
    def open(filepath: str):
        """
        Loads a Machine instance from a file using joblib.

        :param filepath: The path to the file from which to load the instance.
        :return: The loaded Machine instance.
        """
        return joblib.load(filepath)

    def info(self) -> str:
        """
        Returns information about the model, including the base model name and timestamp.

        :return: A string containing the information.
        """
        return f"Base Model: {self.name}<br>Timestamp: {
            self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
