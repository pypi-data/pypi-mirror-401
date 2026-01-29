"""
KWS Library - Python client for KWS Platform API

A comprehensive Python library for interacting with the KWS Platform backend API,
including dataset management, model training, experiments, and dataset split file access.
"""

from .client import KWSClient
from .minio_client import DatasetSplitFilesClient
from .telegram_notifier import TelegramNotifier

__version__ = "0.0.1"
__all__ = ["KWSClient", "DatasetSplitFilesClient", "TelegramNotifier"]
