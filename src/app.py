from flask import Flask, jsonify
from sklearn.linear_model import LinearRegression
import pandas as pd


# Read training data
df = pd.read_csv("data/training_data.csv")
X = df[["address_zip", "size", "category"]]
y = df["rental_price"]

# Train the model
model = LinearRegression()
model.fit(X, y)

# Read prediction data from CSV
prediction_data_df = pd.read_csv("data/predict_data.csv")
prediction_data = prediction_data_df.iloc[0].to_dict()

# Make prediction
input_data = prediction_data_df[["address_zip", "size", "category"]]
prediction = model.predict(input_data)[0]
result = {"PrecioIdeal": round(prediction, 2)}


# Create Flask API
app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_result():
    return jsonify(result)


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
