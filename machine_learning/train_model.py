
import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "matching_pairs.csv"

MODEL_DIR = BASE_DIR / "machine_learning" / "models"

MODEL_FILE = MODEL_DIR / "ride_match_model.pkl"

FEATURE_FILE = MODEL_DIR / "feature_names.pkl"


# ==========================================
# LOAD DATASET
# ==========================================

print("\nLoading matching dataset...")

df = pd.read_csv(DATA_FILE)

print("Dataset shape:", df.shape)


# ==========================================
# SELECT FEATURES
# ==========================================

FEATURES = [
    "pickup_distance_km",
    "drop_distance_km",
    "time_difference_min",
    "route_similarity"
]

TARGET = "matching_label"

X = df[FEATURES]
y = df[TARGET]


# ==========================================
# DATA VALIDATION
# ==========================================

if X.isnull().any().any() or y.isnull().any():
    raise ValueError("Dataset contains missing values.")

if y.nunique() != 2:
    raise ValueError(
        "Both matching classes (0 and 1) are required."
    )

if y.value_counts().min() < 2:
    raise ValueError(
        "Not enough examples in one of the classes."
    )

print("\nFeature columns:")
print(FEATURES)

print("\nLabel distribution:")
print(y.value_counts())


# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))


# ==========================================
# RANDOM FOREST MODEL
# ==========================================

print("\nTraining Random Forest Classifier...")

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)


# ==========================================
# MODEL PREDICTIONS
# ==========================================

y_pred = model.predict(X_test)


# ==========================================
# MODEL EVALUATION
# ==========================================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

print("\n========== MODEL RESULTS ==========")

print(f"Accuracy:  {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall:    {recall * 100:.2f}%")
print(f"F1 Score:  {f1 * 100:.2f}%")


# ==========================================
# CLASSIFICATION REPORT
# ==========================================

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# ==========================================
# CONFUSION MATRIX
# ==========================================

print("\nConfusion Matrix:")

print(confusion_matrix(y_test, y_pred))


# ==========================================
# FEATURE IMPORTANCE
# ==========================================

importance = pd.DataFrame({

    "Feature": FEATURES,

    "Importance": model.feature_importances_

}).sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance:")

print(importance.to_string(index=False))


# ==========================================
# SAVE TRAINED MODEL
# ==========================================

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(model, MODEL_FILE)

joblib.dump(FEATURES, FEATURE_FILE)

print("\n================================")
print("MODEL TRAINED SUCCESSFULLY!")
print("================================")

print("Model saved at:", MODEL_FILE)

print("Features saved at:", FEATURE_FILE)
