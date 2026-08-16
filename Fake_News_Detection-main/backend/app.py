from flask import Flask, request, jsonify
from flask_cors import CORS

from predict import predict_news


# ==========================================
# CREATE FLASK APP
# ==========================================

app = Flask(__name__)

CORS(app)


# ==========================================
# HOME ROUTE
# ==========================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "status": "success",
        "message": "Fake News Detection API is running."
    })


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy"
    })


# ==========================================
# PREDICTION ROUTE
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # Get JSON data
        data = request.get_json(
            silent=True
        )


        # Check request
        if data is None:

            return jsonify({
                "success": False,
                "error": "Request must contain JSON data."
            }), 400


        # Get text
        text = data.get("text")


        # Validate text
        if text is None:

            return jsonify({
                "success": False,
                "error": "Missing 'text' field."
            }), 400


        if not isinstance(text, str):

            return jsonify({
                "success": False,
                "error": "'text' must be a string."
            }), 400


        if not text.strip():

            return jsonify({
                "success": False,
                "error": "News text cannot be empty."
            }), 400


        # Predict
        result = predict_news(text)


        # Return result
        return jsonify({
            "success": True,
            "prediction": result["prediction"],
            "confidence": result["confidence"]
        })


    except FileNotFoundError as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


    except ValueError as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 400


    except Exception as error:

        print(
            f"Server error: {error}"
        )

        return jsonify({
            "success": False,
            "error": "Internal server error."
        }), 500


# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":

    print("\n===================================")
    print("   FAKE NEWS DETECTION API")
    print("===================================")

    print(
        "\nServer running at:"
        "\nhttp://127.0.0.1:5000"
    )

    print(
        "\nPrediction endpoint:"
        "\nPOST http://127.0.0.1:5000/predict"
    )

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )