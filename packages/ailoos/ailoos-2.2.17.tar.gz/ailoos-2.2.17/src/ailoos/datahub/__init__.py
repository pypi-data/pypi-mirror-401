"""
DataHub - Infraestructura completa para gestión de datasets
==========================================================

Módulo principal del sistema DataHub que proporciona:

- DatasetRegistry: Registro y catálogo de datasets disponibles
- DatasetDownloader: Descarga segura desde IPFS con validación
- DatasetValidator: Validación de integridad y calidad de datasets
- DatasetManager: Gestión local de datasets en nodos
- DataHubAPI: API REST para acceso al catálogo de datasets

Este módulo implementa una infraestructura completa para la gestión
distribuida de datasets en el ecosistema AILOOS.
"""

from .models import Dataset, DatasetChunk, DatasetValidation, DatasetDownload
from .registry import DatasetRegistry
from .downloader import DatasetDownloader, DownloadConfig
from .validator import DatasetValidator, ValidationConfig
from .manager import DatasetManager, CacheConfig
from .api import DataHubAPI, create_datahub_app

__all__ = [
    'Dataset',
    'DatasetChunk',
    'DatasetValidation',
    'DatasetDownload',
    'DatasetRegistry',
    'DatasetDownloader',
    'DownloadConfig',
    'DatasetValidator',
    'ValidationConfig',
    'DatasetManager',
    'CacheConfig',
    'DataHubAPI',
    'create_datahub_app'
]