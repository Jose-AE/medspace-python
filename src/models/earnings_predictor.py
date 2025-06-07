class EarningsPredictor:
    def __init__(self, model):
        self.model = model

    def predict(self, features):
        """
        Predict earnings based on the provided features.

        :param features: A dictionary containing the input features for prediction.
        :return: Predicted earnings value.
        """
        # Convert features to the format expected by the model
        input_data = self._prepare_input(features)

        # Make prediction using the model
        prediction = self.model.predict(input_data)

        return prediction

    def train(self, training_data):
        """
        Train the earnings prediction model using the provided training data.

        :param training_data: A DataFrame containing the training data.
        """
        # Extract features and target variable from the training data
        X = training_data.drop(columns=["target"])
        y = training_data["target"]

        # Fit the model
        self.model.fit(X, y)
