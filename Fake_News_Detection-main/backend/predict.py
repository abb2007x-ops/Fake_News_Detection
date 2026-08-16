import os
import pickle

from preprocess import clean_text


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "saved_model",
    "fake_news_model.pkl"
)


def load_model():

    if not os.path.exists(MODEL_PATH):

        raise FileNotFoundError(
            "Trained model not found. "
            "Please run train.py first."
        )

    with open(
        MODEL_PATH,
        "rb"
    ) as file:

        model = pickle.load(file)

    return model


model = load_model()


def predict_news(text):

    cleaned_text = clean_text(text)

    if not cleaned_text:

        raise ValueError(
            "News text cannot be empty."
        )


    # Prediction
    prediction = model.predict(
        [cleaned_text]
    )[0]


    # Probability
    probabilities = model.predict_proba(
        [cleaned_text]
    )[0]


    # Probability of predicted class
    confidence = float(
        probabilities[prediction]
    )


    if prediction == 0:

        label = "FAKE"

    else:

        label = "REAL"


    return {
        "prediction": label,
        "confidence": round(
            confidence * 100,
            2
        )
    }