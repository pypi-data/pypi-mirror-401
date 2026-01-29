"""
Regression module for generic regression tasks.

This module provides reusable components for training regression models
using PyTorch Lightning. All components are fully config-driven and can
be used for any regression task by simply changing the YAML configuration.
"""

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
