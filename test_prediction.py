
from machine_learning.predict import predictor

result = predictor.predict_match(
    pickup_distance_km=0.2,
    drop_distance_km=0.3,
    time_difference_min=5,
    route_similarity=99.9
)

print("\n========== AI RIDE MATCHING ==========")

print("Result:", result["result"])

print(
    "Match Probability:",
    result["match_probability"],
    "%"
)

print("Prediction:", result["match"])
