from typing import List
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

NUMERIC_FEATURES: List[str] = ["years_experience"]
CATEGORICAL_FEATURES: List[str] = ["education_level", "job_title", "city", "company_size"]
BINARY_FEATURES: List[str] = ["skills_python", "skills_java", "skills_aws", "skills_sql"]

FEATURE_ORDER: List[str] = NUMERIC_FEATURES + CATEGORICAL_FEATURES + BINARY_FEATURES

def build_preprocessor() -> ColumnTransformer:
    pre = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(with_mean=True, with_std=True), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
            ("bin", "passthrough", BINARY_FEATURES),
        ],
        remainder="drop",
        n_jobs=None,
        verbose_feature_names_out=False,
    )
    return pre

def build_pipeline() -> Pipeline:
    pre = build_preprocessor()
    model = LinearRegression()
    pipe = Pipeline(steps=[("pre", pre), ("lr", model)])
    return pipe
