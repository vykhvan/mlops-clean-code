"""
Churn Pipeline.
"""

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from churn_model.config.core import config

preprocessor = ColumnTransformer(
    transformers=[
        ("categorical_columns", OneHotEncoder(), config.model_config.cat_features),
    ],
    remainder="passthrough",
)

random_forest = RandomForestClassifier(
    n_estimators=config.model_config.n_estimators,
    max_depth=config.model_config.max_depth,
    criterion=config.model_config.criterion,
)

churn_pipeline = Pipeline(
    steps=[("preprocessor", preprocessor), ("random_forest", random_forest)]
)
