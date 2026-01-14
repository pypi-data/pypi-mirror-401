"""
Inference Package - FASE 4: API de Inferencia y Model Management
Sistema completo de inferencia enterprise-grade para EmpoorioLM.
"""

# API de inferencia principal
# from .api import EmpoorioLMInferenceAPI, InferenceConfig  # TODO: Implementar

# Sistema de gestión de modelos (FASE 4)
from .model_registry import (
    ModelRegistry,
    ModelMetadata,
    ModelVersion,
    ModelStatus,
    ModelType
)
from .model_lifecycle_manager import (
    ModelLifecycleManager,
    Environment,
    LifecycleStage,
    DeploymentConfig
)

# Optimizaciones Maturity 2
from .quantization import AdvancedQuantizer, quantize_empoorio_model
from .model_drift_monitor import ModelDriftMonitor, create_drift_monitor, DriftThresholds
from .vllm_batching import VLLMInferenceEngine, create_vllm_engine, BatchingConfig, DynamicBatcher

# Ensemble System (FASE 9)
from .ensemble_system import (
    VotingEnsemble,
    BaggingEnsemble,
    BoostingEnsemble,
    StackingEnsemble,
    WeightedEnsemble,
    EnsembleManager,
    VotingType,
    EnsembleType,
    ModelPrediction,
    EnsembleResult
)

__all__ = [
    # API principal
    # 'EmpoorioLMInferenceAPI',
    # 'InferenceConfig',

    # Sistema de gestión de modelos (FASE 4)
    'ModelRegistry',
    'ModelMetadata',
    'ModelVersion',
    'ModelStatus',
    'ModelType',
    'ModelLifecycleManager',
    'Environment',
    'LifecycleStage',
    'DeploymentConfig',

    # Cuantización (Maturity 2)
    'AdvancedQuantizer',
    'quantize_empoorio_model',

    # Monitoreo de deriva (Maturity 2)
    'ModelDriftMonitor',
    'create_drift_monitor',
    'DriftThresholds',

    # Batching vLLM (Maturity 2)
    'VLLMInferenceEngine',
    'create_vllm_engine',
    'BatchingConfig',
    'DynamicBatcher',
    
    # Ensemble System (FASE 9)
    'VotingEnsemble',
    'BaggingEnsemble',
    'BoostingEnsemble',
    'StackingEnsemble',
    'WeightedEnsemble',
    'EnsembleManager',
    'VotingType',
    'EnsembleType',
    'ModelPrediction',
    'EnsembleResult'
    ]