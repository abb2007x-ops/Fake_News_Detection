import os
import pickle

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from preprocess import clean_text
from model import create_model


# ==========================================
# PATHS
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATASET_DIR = os.path.join(
    BASE_DIR,
    "dataset"
)

FAKE_PATH = os.path.join(
    DATASET_DIR,
    "Fake.csv"
)

REAL_PATH = os.path.join(
    DATASET_DIR,
    "True.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "saved_model"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "fake_news_model.pkl"
)


# ==========================================
# START
# ==========================================

print("\n===================================")
print("     FAKE NEWS MODEL TRAINING")
print("===================================\n")


# ==========================================
# CHECK DATASET
# ==========================================

if not os.path.exists(FAKE_PATH):
    raise FileNotFoundError(
        f"Fake.csv not found at:\n{FAKE_PATH}"
    )

if not os.path.exists(REAL_PATH):
    raise FileNotFoundError(
        f"True.csv not found at:\n{REAL_PATH}"
    )


# ==========================================
# LOAD DATA
# ==========================================

print("Loading Fake.csv...")

fake_df = pd.read_csv(FAKE_PATH)

print(
    f"Fake news articles: {len(fake_df)}"
)


print("\nLoading True.csv...")

real_df = pd.read_csv(REAL_PATH)

print(
    f"Real news articles: {len(real_df)}"
)


# ==========================================
# ADD LABELS
# ==========================================

fake_df["label"] = 0
real_df["label"] = 1


# ==========================================
# COMBINE DATASETS
# ==========================================

df = pd.concat(
    [fake_df, real_df],
    ignore_index=True
)

print(
    f"\nTotal articles: {len(df)}"
)


# ==========================================
# CLEAN COLUMN NAMES
# ==========================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
)

print("\nAvailable columns:")

print(list(df.columns))


# ==========================================
# CHECK REQUIRED COLUMNS
# ==========================================

required_columns = [
    "title",
    "text",
    "label"
]

for column in required_columns:

    if column not in df.columns:

        raise ValueError(
            f"Required column missing: {column}"
        )


# ==========================================
# HANDLE MISSING VALUES
# ==========================================

df["title"] = (
    df["title"]
    .fillna("")
    .astype(str)
)

df["text"] = (
    df["text"]
    .fillna("")
    .astype(str)
)


# ==========================================
# REMOVE EMPTY ARTICLES
# ==========================================

df = df[
    (
        df["title"].str.strip() != ""
    )
    |
    (
        df["text"].str.strip() != ""
    )
].copy()


print(
    f"\nArticles after removing empty rows: "
    f"{len(df)}"
)


# ==========================================
# COMBINE TITLE + ARTICLE
# ==========================================

print(
    "\nCombining title and article text..."
)

df["combined_text"] = (
    df["title"]
    + " "
    + df["text"]
)


# ==========================================
# CLEAN COMBINED TEXT
# ==========================================

print(
    "Cleaning text..."
)

df["combined_text"] = (
    df["combined_text"]
    .apply(clean_text)
)


# ==========================================
# REMOVE EMPTY CLEANED TEXT
# ==========================================

df = df[
    df["combined_text"].str.strip() != ""
].copy()


print(
    f"Usable articles: {len(df)}"
)


# ==========================================
# FEATURES AND TARGET
# ==========================================

X = df["combined_text"]

y = df["label"]


# ==========================================
# CLASS DISTRIBUTION
# ==========================================

print("\nClass distribution:")

print(
    y.value_counts()
)


# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

print(
    "\nSplitting dataset..."
)


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print(
    f"Training samples: {len(X_train)}"
)

print(
    f"Testing samples: {len(X_test)}"
)


# ==========================================
# CREATE MODEL
# ==========================================

print(
    "\nCreating TF-IDF + Logistic Regression..."
)

model = create_model()


# ==========================================
# TRAIN MODEL
# ==========================================

print(
    "\nTraining model..."
)

print(
    "This may take several minutes."
)


model.fit(
    X_train,
    y_train
)


print(
    "\nTraining completed successfully!"
)


# ==========================================
# TEST MODEL
# ==========================================

print(
    "\nTesting model..."
)


predictions = model.predict(
    X_test
)


# ==========================================
# ACCURACY
# ==========================================

accuracy = accuracy_score(
    y_test,
    predictions
)


print(
    "\n==================================="
)

print(
    f"Accuracy: {accuracy * 100:.2f}%"
)

print(
    "===================================\n"
)


# ==========================================
# CLASSIFICATION REPORT
# ==========================================

print(
    "Classification Report:\n"
)


print(
    classification_report(
        y_test,
        predictions,
        target_names=[
            "FAKE",
            "REAL"
        ]
    )
)


# ==========================================
# CONFUSION MATRIX
# ==========================================

print(
    "Confusion Matrix:\n"
)


print(
    confusion_matrix(
        y_test,
        predictions
    )
)


# ==========================================
# SAVE MODEL
# ==========================================

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


with open(
    MODEL_PATH,
    "wb"
) as file:

    pickle.dump(
        model,
        file
    )


print(
    "\n==================================="
)

print(
    "MODEL SAVED SUCCESSFULLY!"
)

print(
    "==================================="
)

print(
    f"\nModel location:\n{MODEL_PATH}"
)