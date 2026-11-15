
import joblib
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR / "machine_learning" /
    "models" / "ride_match_model.pkl"
)

FEATURE_PATH = (
    BASE_DIR / "machine_learning" /
    "models" / "feature_names.pkl"
)


class RideMatchPredictor:

    def __init__(self):

        self.model = joblib.load(MODEL_PATH)

        self.features = joblib.load(FEATURE_PATH)

    def predict_match(
        self,
        pickup_distance_km,
        drop_distance_km,
        time_difference_min,
        route_similarity
    ):

        input_data = pd.DataFrame([{

            "pickup_distance_km": pickup_distance_km,

            "drop_distance_km": drop_distance_km,

            "time_difference_min": time_difference_min,

            "route_similarity": route_similarity

        }])

        input_data = input_data[self.features]

        prediction = self.model.predict(input_data)[0]

        probability = self.model.predict_proba(
            input_data
        )[0]

        return {
            "match": int(prediction),
            "match_probability": round(
                float(probability[1]) * 100, 2
            ),
            "result": (
                "Potential Match"
                if prediction == 1
                else "Not a Match"
            )
        }


predictor = RideMatchPredictor()
