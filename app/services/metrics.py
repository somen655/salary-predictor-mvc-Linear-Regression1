from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from .preprocess import build_pipeline, FEATURE_ORDER

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "salary_data.csv"
ARTIFACT = ROOT / "artifacts" / "model.joblib"
METRICS = ROOT / "artifacts" / "metrics.json"

def evaluate_from_csv(test_size: float = 0.2, random_state: int = 42):
    df = pd.read_csv(DATA)
    y = df["salary_in_inr"]
    X = df.drop(columns=["salary_in_inr"])

    pipe = build_pipeline()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)

    r2 = float(r2_score(y_test, preds))
    mae = float(mean_absolute_error(y_test, preds))

    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, ARTIFACT)

    METRICS.write_text(json.dumps({"r2": r2, "mae": mae, "n_test": int(len(y_test))}, indent=2))

    return {"r2": r2, "mae": mae, "n_test": int(len(y_test))}
