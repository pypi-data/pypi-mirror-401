"""
CPH Regression - A generic, config-driven regression training package.

This package provides a reusable PyTorch Lightning pipeline for training
regression models on any tabular dataset using YAML configuration files.
"""

__version__ = "0.1.0"
__author__ = "chandra"

from cph_regression.regression.modelmodule import ModelModuleRGS
from cph_regression.regression.datamodule import DataModuleRGS
from cph_regression.regression.modelfactory import RegressionModel
from cph_regression.regression.dataset import RegressionDataset
from cph_regression.regression.callbacks import ONNXExportCallback

__all__ = [
    "ModelModuleRGS",
    "DataModuleRGS",
    "RegressionModel",
    "RegressionDataset",
    "ONNXExportCallback",
]
