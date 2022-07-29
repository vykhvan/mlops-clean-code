import json
import logging
import typing as t
from pathlib import Path

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from churn_model import __version__ as _version
from churn_model.config.core import DATASET_DIR, MODEL_DIR, REPORT_DIR, config

format = "%(asctime)-15s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=format)


def load_dataset(*, file_name: str) -> pd.DataFrame:
    """Load the dataset.

    Args:
        file_name: The name of the file to load.

    Returns:
        dataframe: A Pandas DataFrame with loaded data.
    """
    dataframe = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"))
    logging.info("Dataframe loaded: %s" % str(dataframe.shape))
    return dataframe


def save_report(report: dict) -> None:
    """Save the classification model report.

    Args:
        report: Dictionary with model training results.

    Returns:
        None
    """
    with open(REPORT_DIR / config.app_config.report_save_file, "w") as json_file:
        json.dump(report, json_file)
    logging.info(
        "Report saved: %s" % str(REPORT_DIR / config.app_config.report_save_file)
    )


def save_pipeline(*, pipeline_to_persist: Pipeline) -> None:
    """Persist the pipeline.
    Saves the versioned model, and overwrites any previous
    saved models. This ensures that when the package is
    published, there is only one trained model that can be
    called, and we know exactly how it was built.

    Args:
        pipeline_to_persist: scikit-learn transform pipeline.

    Returs:
        None
    """

    # Prepare versioned save file name
    save_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
    save_path = MODEL_DIR / save_file_name
    remove_old_pipelines(files_to_keep=[save_file_name])
    joblib.dump(pipeline_to_persist, save_path)
    logging.info("Saving pipeline: %s" % save_path)


def load_pipeline(*, file_name: str) -> Pipeline:
    """Load a persisted pipeline.

    Args:
        file_name: The name of the model pipeline.

    Returns:
        pipeline: The loaded scikit-learn pipeline.
    """

    file_path = MODEL_DIR / file_name
    trained_model = joblib.load(filename=file_path)
    return trained_model


def remove_old_pipelines(*, files_to_keep: t.List[str]) -> None:
    """
    Remove old model pipelines.
    This is to ensure there is a simple one-to-one
    mapping between the package version and the model
    version to be imported and used by other applications.

    Args:
        files_to_keep: list of file names that should NOT be deleted.

    Returns:
        None
    """
    do_not_delete = files_to_keep + ["__init__.py"]
    logging.info("Removing old model pipelines")
    for model_file in MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()
