"""
API Module - Contains all API endpoint wrappers
"""

from .auth import AuthAPI
from .datasets import DatasetsAPI
from .models import ModelsAPI
from .experiments import ExperimentsAPI
from .keywords import KeywordsAPI
from .sentences import SentencesAPI
from .audio import AudioAPI
from .features import FeaturesAPI
from .dataset_splits import DatasetSplitsAPI
from .jobs import JobsAPI
from .embeddings import EmbeddingsAPI
from .fewshot import FewShotAPI
from .predict import PredictAPI
from .dashboard import DashboardAPI
from .tasks import TasksAPI
from .collection import CollectionAPI
from .recordings import RecordingsAPI
from .metrics import MetricsAPI
from .visualize import VisualizeAPI
from .compare import CompareAPI
from .devices import DevicesAPI
from .artifacts import ArtifactsAPI
from .deployed_models import DeployedModelsAPI
from .quality_control import QualityControlAPI
from .reward_payout import RewardPayoutAPI
from .config import ConfigAPI
from .metadata import MetadataAPI
from .notifications import NotificationsAPI
from .admin import AdminAPI
from .users import UsersAPI

__all__ = [
    "AuthAPI", "DatasetsAPI", "ModelsAPI", "ExperimentsAPI",
    "KeywordsAPI", "SentencesAPI", "AudioAPI", "FeaturesAPI",
    "DatasetSplitsAPI", "JobsAPI", "EmbeddingsAPI", "FewShotAPI",
    "PredictAPI", "DashboardAPI", "TasksAPI", "CollectionAPI",
    "RecordingsAPI", "MetricsAPI", "VisualizeAPI", "CompareAPI",
    "DevicesAPI", "ArtifactsAPI", "DeployedModelsAPI",
    "QualityControlAPI", "RewardPayoutAPI", "ConfigAPI",
    "MetadataAPI", "NotificationsAPI", "AdminAPI", "UsersAPI"
]
