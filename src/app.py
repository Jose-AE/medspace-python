from flask import Flask, jsonify
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
import pandas as pd
import threading
import time

# Read training data
df = pd.read_csv("data/training_data.csv")
df["address_zip"] = df["address_zip"].astype(str).str.zfill(5)

# Read prediction data
prediction_data_df = pd.read_csv("data/predict_data.csv")
prediction_data_df["address_zip"] = prediction_data_df["address_zip"].astype(str).str.zfill(5)
prediction_data = prediction_data_df.iloc[0].to_dict()
zip_code = prediction_data["address_zip"]
size = prediction_data["size"]

# Filter by exact zip code
filtered_df = df[df["address_zip"] == zip_code]
group_info = f"Código postal exacto: {zip_code}"

# If there is no coincidence, search by prefix (group by mayoralty)
if filtered_df.empty:
    prefix = zip_code[:2] if len(zip_code) >= 2 else zip_code[0]
    group_info = f"Prefijo de alcaldía (2 dígitos): {prefix}XXX"
    filtered_df = df[df["address_zip"].str.startswith(prefix)]

# Verify if there is data
if filtered_df.empty:
    result = {"error": f"No hay datos disponibles para el código postal {zip_code} ni su zona."}
else:
    # Prepare data for training
    X = filtered_df[["address_zip", "size"]]
    y = filtered_df["rental_price"]

    # Preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ("zip_encoder", OneHotEncoder(handle_unknown="ignore"), ["address_zip"]),
            ("passthrough", "passthrough", ["size"])
        ]
    )

    # Create pipeline and train model
    model = make_pipeline(preprocessor, LinearRegression())
    model.fit(X, y)

    # Input data for prediction
    input_df = pd.DataFrame([{
        "address_zip": zip_code,
        "size": size
    }])

    # Make prediction
    raw_prediction = model.predict(input_df)[0]
    prediction = max(0, round(raw_prediction, 2))

    result = {"PrecioIdeal": round(prediction, 2)}

# Show in console
print("Enviando datos al modelo:", prediction_data)
print("Respuesta recibida:", result)

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