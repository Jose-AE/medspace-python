from flask import Flask, jsonify
import pandas as pd
from sklearn.linear_model import LinearRegression
from .models.price_predictor import PricePredictor
from flask import request
from datetime import datetime, timedelta


# Create Flask API
app = Flask(__name__)


@app.route("/predict_earnings", methods=["POST"])
def predict_earnings():
    try:
        # Recibir datos del backend
        data = request.get_json()

        # Validar estructura
        if not isinstance(data, list) or not all("amount" in item and "paymentDate" in item for item in data):
            return jsonify({"error": "Formato inválido. Se esperaba lista de objetos con 'amount' y 'paymentDate'."}), 400

        # Convertir a DataFrame
        df = pd.DataFrame(data)
        df["fecha_ordinal"] = pd.to_datetime(df["paymentDate"]).map(datetime.toordinal)
        X = df[["fecha_ordinal"]]
        y = df["amount"]

        # Entrenar modelo
        model = LinearRegression()
        model.fit(X, y)

        # Predecir próximos 7 días
        last_date = pd.to_datetime(df["paymentDate"]).max()
        future_dates = [last_date + timedelta(days=i) for i in range(1, 8)]
        future_ordinals = [[d.toordinal()] for d in future_dates]
        predictions = model.predict(future_ordinals)

        # Preparar respuesta
        result = [{"date": d.strftime("%Y-%m-%d"), "predictedAmount": round(pred, 2)} for d, pred in zip(future_dates, predictions)]

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/predict_price", methods=["GET"])
def predict_price():
    zip_code = request.args.get("zip_code", "01000")
    size = int(request.args.get("size", 1000))

    model = PricePredictor()
    result = model.predict(zip_code=zip_code, size=size)

    return jsonify(result)


@app.route("/predict_price/train", methods=["GET"])
def train():
    model = PricePredictor()
    model.train()

    return jsonify({"message": "Model trained successfully"})


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
