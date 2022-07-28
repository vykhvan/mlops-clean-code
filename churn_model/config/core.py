"""
Pydantic classes for create and validation config.
"""
from pathlib import Path
from typing import Sequence

from pydantic import BaseModel
from strictyaml import YAML, load

import churn_model

# Project Directories
PACKAGE_ROOT = Path(churn_model.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yaml"
DATASET_DIR = PACKAGE_ROOT / "datasets"
MODEL_DIR = PACKAGE_ROOT / "models"
REPORT_DIR = PACKAGE_ROOT / "reports"


class AppConfig(BaseModel):
    """Application level configuration.

    Package and pipeline management.
    """

    package_name: str
    training_data_file: str
    pipeline_save_file: str
    report_save_file: str


class ModelConfig(BaseModel):
    """Model level configuration.

    Configuration for feature engineering and model training.
    """

    target: str
    features: Sequence[str]
    cat_features: Sequence[str]
    test_size: float
    random_state: int
    n_estimators: int
    max_depth: int
    criterion: str


class Config(BaseModel):
    """Master configuration class."""

    app_config: AppConfig
    model_config: ModelConfig


def find_config_file() -> Path:
    """Locate the configuration file."""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH!r}")


def fetch_config_from_yaml(cfg_path: Path = None) -> YAML:
    """Parse YAML containing the package configuration."""

    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with open(cfg_path, "r") as conf_file:
            parsed_config = load(conf_file.read())
            return parsed_config
    raise OSError(f"Did not find config file at path: {cfg_path}")


def create_and_validate_config(parsed_config: YAML = None) -> Config:
    """Run validation on config values."""
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    _config = Config(
        app_config=AppConfig(**parsed_config.data),
        model_config=ModelConfig(**parsed_config.data),
    )

    return _config


config = create_and_validate_config()
