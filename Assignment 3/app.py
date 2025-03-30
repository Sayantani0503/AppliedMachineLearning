from flask import Flask, request, jsonify
import joblib
from score import score  # Import the scoring function

app = Flask(__name__)


model = joblib.load("/content/best_model.pkl")

@app.route("/score", methods=["POST"])
def score_endpoint():
    try:
        # Get JSON data from request
        data = request.get_json()

        if "text" not in data or not isinstance(data["text"], str):
            return jsonify({"error": "Invalid input. 'text' must be a string."}), 400

        threshold = data.get("threshold", 0.5)
        if not (0 <= threshold <= 1):
            return jsonify({"error": "Threshold must be between 0 and 1."}), 400


        prediction, propensity = score(data["text"], model, threshold)

        return jsonify({
            "prediction": bool(prediction),
            "propensity": float(propensity)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
