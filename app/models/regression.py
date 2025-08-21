from pathlib import Path
import joblib
import numpy as np
import pandas as pd

from ..services.preprocess import build_pipeline, FEATURE_ORDER, CATEGORICAL_FEATURES, NUMERIC_FEATURES, BINARY_FEATURES

ARTIFACT_DIR = Path(__file__).resolve().parents[2] / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "model.joblib"

class SalaryModel:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def predict_one(self, d: dict) -> float:
        # Ensure columns exist in correct order; missing keys default
        row = {**{f: 0 for f in BINARY_FEATURES}, **{f: None for f in CATEGORICAL_FEATURES + NUMERIC_FEATURES}, **d}
        df = pd.DataFrame([row], columns=FEATURE_ORDER)
        pred = self.pipeline.predict(df)[0]
        return float(pred)

class ModelRegistry:
    _model = None

    @classmethod
    def is_loaded(cls) -> bool:
        return cls._model is not None

    @classmethod
    def get(cls) -> SalaryModel:
        if cls._model is None:
            cls.load()
        return cls._model

    @classmethod
    def load(cls, force: bool = False):
        if force:
            cls._model = None
        if cls._model is None:
            if MODEL_PATH.exists():
                pipeline = joblib.load(MODEL_PATH)
                cls._model = SalaryModel(pipeline)
            else:
                # Fallback: fresh untrained pipeline to avoid crashes; will be poor at prediction
                pipeline = build_pipeline()
                cls._model = SalaryModel(pipeline)
