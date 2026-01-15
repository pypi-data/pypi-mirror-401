"""
CPV (Checkpoints Versioning) - Model and Data Versioning for AI Teams

A Python package for managing model and data checkpoints using Git, DVC, and AWS S3.
Provides semantic versioning, atomic operations, and integrated cloud storage.
"""

__version__ = "0.1.0"
__author__ = "AI Team"
__license__ = "MIT"

from cp_manage.utilities import (
    CPVConfig,
    ModelsCheckpointsManage,
    DataCheckpointsManage,
    CombinedCheckpointsManage,
    ModelArtifacts,
    DataArtifacts,
)

__all__ = [
    "CPVConfig",
    "ModelsCheckpointsManage",
    "DataCheckpointsManage",
    "CombinedCheckpointsManage",
    "ModelArtifacts",
    "DataArtifacts",
]
