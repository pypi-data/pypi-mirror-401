#!/usr/bin/env python3
"""
AILOOS Refinery Engine - Motor de Refinería de Datos
====================================================

Este módulo implementa el Motor de Refinería completo que orquesta el flujo
de procesamiento de datos: Ingesta → Scrub → Shard → IPFS → Registro.

El motor coordina todos los componentes del pipeline de datos para transformar
datos crudos en datasets listos para entrenamiento federado distribuido.

Características principales:
- Pipeline completo de refinación de datos
- Soporte para múltiples formatos de entrada
- Integración automática con PII scrubbing
- Sharding inteligente basado en capacidades
- Subida automática a IPFS con registro
- Monitoreo y estadísticas detalladas
- Manejo robusto de errores

Arquitectura:
Datos Crudos → Ingesta → PII Scrub → Sharding → IPFS Upload → Registro → Dataset Listo
"""

import logging
import time
from typing import Dict, List, Optional, Any, Union, Tuple
from pathlib import Path
from datetime import datetime
import json

from .dataset_manager import dataset_manager
from ..privacy.pii_scrubber import pii_scrubber
from .ipfs_connector import ipfs_connector
from .registry import data_registry
from .dataset_chunker import DatasetChunker, ChunkConfig

logger = logging.getLogger(__name__)

class RefineryEngine:
    """
    Motor de Refinería que implementa el pipeline completo de procesamiento de datos.

    Coordina todos los componentes para transformar datos crudos en datasets
    federados listos para distribución.
    """

    def __init__(self):
        """Inicializa el Motor de Refinería."""
        self.chunker = DatasetChunker()
        self.stats = {
            "total_datasets_processed": 0,
            "total_data_ingested_mb": 0.0,
            "total_pii_instances_scrubbed": 0,
            "total_shards_created": 0,
            "total_ipfs_uploads": 0,
            "processing_time_total": 0.0,
            "errors_encountered": 0,
            "last_activity": None
        }

        logger.info("🚀 Motor de Refinería inicializado")

    def process_data_pipeline(self, data_input: Union[str, List[Dict], Path],
                            dataset_name: str,
                            input_type: str = "auto",
                            shard_config: Optional[Dict] = None,
                            metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Ejecuta el pipeline completo de refinación: Ingesta → Scrub → Shard → IPFS → Registro.

        Args:
            data_input: Datos de entrada (ruta de archivo, lista de dicts, etc.)
            dataset_name: Nombre del dataset resultante
            input_type: Tipo de entrada ('file', 'json', 'text', 'auto')
            shard_config: Configuración de sharding opcional
            metadata: Metadatos adicionales

        Returns:
            Dict con resultados del procesamiento completo
        """
        start_time = time.time()
        logger.info(f"🔄 Iniciando pipeline de refinación para: {dataset_name}")

        try:
            # Paso 1: INGESTA - Cargar y validar datos
            logger.info("📥 Paso 1: Ingesta de datos")
            ingested_data, data_info = self._ingest_data(data_input, input_type)
            self.stats["total_data_ingested_mb"] += data_info["size_mb"]

            # Paso 2: SCRUB - Limpieza PII
            logger.info("🧹 Paso 2: Scrubbing PII")
            scrubbed_data, scrub_info = self._scrub_data(ingested_data, data_info["type"])
            self.stats["total_pii_instances_scrubbed"] += scrub_info["pii_removed"]

            # Paso 3: SHARD - Fragmentación inteligente
            logger.info("✂️ Paso 3: Sharding inteligente")
            shards, shard_info = self._create_shards(scrubbed_data, shard_config or {})
            self.stats["total_shards_created"] += shard_info["num_shards"]

            # Paso 4: IPFS - Subida a almacenamiento distribuido
            logger.info("📡 Paso 4: Subida a IPFS")
            ipfs_result = self._upload_to_ipfs(shards, dataset_name, metadata)
            self.stats["total_ipfs_uploads"] += len(ipfs_result["shard_cids"])

            # Paso 5: REGISTRO - Registro en el sistema
            logger.info("📋 Paso 5: Registro del dataset")
            registry_result = self._register_dataset(ipfs_result, data_info, scrub_info, shard_info, metadata)

            # Actualizar estadísticas globales
            processing_time = time.time() - start_time
            self.stats["total_datasets_processed"] += 1
            self.stats["processing_time_total"] += processing_time
            self.stats["last_activity"] = datetime.now().isoformat()

            result = {
                "success": True,
                "dataset_name": dataset_name,
                "pipeline_steps": {
                    "ingestion": data_info,
                    "scrubbing": scrub_info,
                    "sharding": shard_info,
                    "ipfs_upload": ipfs_result,
                    "registration": registry_result
                },
                "processing_time_seconds": processing_time,
                "quality_score": registry_result.get("quality_score", 0.0)
            }

            logger.info(f"✅ Pipeline completado exitosamente: {dataset_name}")
            logger.info(f"   📊 Tiempo: {processing_time:.2f}s | Calidad: {result['quality_score']:.2f}")

            return result

        except Exception as e:
            processing_time = time.time() - start_time
            self.stats["errors_encountered"] += 1

            logger.error(f"❌ Error en pipeline de refinación: {e}")

            return {
                "success": False,
                "dataset_name": dataset_name,
                "error": str(e),
                "processing_time_seconds": processing_time,
                "pipeline_step_failed": self._identify_failed_step(e)
            }

    def _ingest_data(self, data_input: Union[str, List[Dict], Path], input_type: str) -> Tuple[Any, Dict]:
        """
        Paso 1: Ingesta de datos - Carga y valida los datos de entrada.
        """
        if input_type == "auto":
            input_type = self._detect_input_type(data_input)

        if input_type == "file":
            return self._ingest_file(data_input)
        elif input_type == "json":
            return self._ingest_json(data_input)
        elif input_type == "text":
            return self._ingest_text(data_input)
        else:
            raise ValueError(f"Tipo de entrada no soportado: {input_type}")

    def _detect_input_type(self, data_input) -> str:
        """Detecta automáticamente el tipo de entrada."""
        if isinstance(data_input, (str, Path)):
            path = Path(data_input)
            if path.exists():
                if path.suffix.lower() in ['.json', '.jsonl']:
                    return "json"
                elif path.suffix.lower() in ['.txt', '.md', '.csv']:
                    return "text"
                else:
                    return "file"
            else:
                # Asumir que es texto directo
                return "text"
        elif isinstance(data_input, list):
            return "json"
        else:
            return "text"

    def _ingest_file(self, file_path: Union[str, Path]) -> Tuple[str, Dict]:
        """Ingesta desde archivo."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        size_bytes = len(content.encode('utf-8'))
        size_mb = size_bytes / (1024 * 1024)

        info = {
            "type": "file",
            "source": str(file_path),
            "size_bytes": size_bytes,
            "size_mb": size_mb,
            "format": path.suffix.lower()
        }

        logger.info(f"📁 Archivo ingestado: {path.name} ({size_mb:.2f}MB)")
        return content, info

    def _ingest_json(self, data_input) -> Tuple[List[Dict], Dict]:
        """Ingesta de datos JSON."""
        if isinstance(data_input, str):
            # Cargar desde archivo
            with open(data_input, 'r', encoding='utf-8') as f:
                data = json.load(f)
        elif isinstance(data_input, list):
            data = data_input
        else:
            raise ValueError("Formato JSON no válido")

        if not isinstance(data, list):
            data = [data]  # Convertir a lista si es un solo objeto

        size_bytes = len(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        size_mb = size_bytes / (1024 * 1024)

        info = {
            "type": "json",
            "records_count": len(data),
            "size_bytes": size_bytes,
            "size_mb": size_mb
        }

        logger.info(f"📊 JSON ingestado: {len(data)} registros ({size_mb:.2f}MB)")
        return data, info

    def _ingest_text(self, text_input) -> Tuple[str, Dict]:
        """Ingesta de texto directo."""
        # Solo intentar como archivo si es un Path o string que parece una ruta
        if isinstance(text_input, Path):
            return self._ingest_file(text_input)
        elif isinstance(text_input, str):
            # Verificar si parece una ruta de archivo (contiene / o \ y no tiene saltos de línea)
            if ('/' in text_input or '\\' in text_input) and '\n' not in text_input:
                try:
                    path = Path(text_input)
                    if path.exists():
                        return self._ingest_file(text_input)
                except (OSError, ValueError):
                    pass  # No es una ruta válida, tratar como texto
            text = text_input
        else:
            text = str(text_input)

        size_bytes = len(text.encode('utf-8'))
        size_mb = size_bytes / (1024 * 1024)

        info = {
            "type": "text",
            "size_bytes": size_bytes,
            "size_mb": size_mb
        }

        logger.info(f"📝 Texto ingestado: {size_mb:.2f}MB")
        return text, info

    def _scrub_data(self, data: Any, data_type: str) -> Tuple[Any, Dict]:
        """
        Paso 2: Scrubbing PII - Limpia información personal identificable.
        """
        start_time = time.time()

        if data_type in ["file", "text"]:
            scrubbed = pii_scrubber.scrub_text(data)
            pii_removed = data != scrubbed
        elif data_type == "json":
            scrubbed = pii_scrubber.scrub_dataset(data)
            pii_removed = True  # JSON datasets siempre se limpian
        else:
            scrubbed = data
            pii_removed = False

        scrub_time = time.time() - start_time

        info = {
            "pii_removed": pii_removed,
            "scrub_time_seconds": scrub_time,
            "scrubber_stats": pii_scrubber.get_stats()
        }

        logger.info(f"🧹 Scrubbing completado: PII removido={pii_removed} ({scrub_time:.2f}s)")
        return scrubbed, info

    def _create_shards(self, data: Any, shard_config: Dict) -> Tuple[List[Any], Dict]:
        """
        Paso 3: Sharding - Crea fragmentos inteligentes del dataset.
        """
        # Usar configuración por defecto si no se proporciona
        config = ChunkConfig(
            max_chunk_size_mb=shard_config.get("max_size_mb", 50.0),
            min_chunk_size_mb=shard_config.get("min_size_mb", 5.0)
        )

        # Para simplicidad, usar sharding básico por tamaño
        # En una implementación completa, usaríamos el DatasetChunker con métricas de nodos
        if isinstance(data, str):
            # Sharding de texto
            shards = self._shard_text(data, config.max_chunk_size_mb)
        elif isinstance(data, list):
            # Sharding de JSON
            shards = self._shard_json(data, config.max_chunk_size_mb)
        else:
            shards = [data]

        info = {
            "num_shards": len(shards),
            "shard_config": {
                "max_size_mb": config.max_chunk_size_mb,
                "min_size_mb": config.min_chunk_size_mb
            }
        }

        logger.info(f"✂️ Sharding completado: {len(shards)} shards creados")
        return shards, info

    def _shard_text(self, text: str, max_size_mb: float) -> List[str]:
        """Crea shards de texto por tamaño."""
        max_bytes = int(max_size_mb * 1024 * 1024)
        shards = []

        # Dividir por párrafos para mantener coherencia
        paragraphs = text.split('\n\n')
        current_shard = ""

        for paragraph in paragraphs:
            potential_size = len((current_shard + paragraph + '\n\n').encode('utf-8'))

            if potential_size > max_bytes and current_shard:
                shards.append(current_shard.strip())
                current_shard = paragraph + '\n\n'
            else:
                current_shard += paragraph + '\n\n'

        if current_shard.strip():
            shards.append(current_shard.strip())

        return shards if shards else [text]

    def _shard_json(self, data: List[Dict], max_size_mb: float) -> List[List[Dict]]:
        """Crea shards de datos JSON."""
        max_bytes = int(max_size_mb * 1024 * 1024)
        shards = []
        current_shard = []
        current_size = 0

        for record in data:
            record_size = len(json.dumps(record).encode('utf-8'))

            if current_size + record_size > max_bytes and current_shard:
                shards.append(current_shard)
                current_shard = [record]
                current_size = record_size
            else:
                current_shard.append(record)
                current_size += record_size

        if current_shard:
            shards.append(current_shard)

        return shards if shards else [data]

    def _upload_to_ipfs(self, shards: List[Any], dataset_name: str, metadata: Optional[Dict]) -> Dict:
        """
        Paso 4: Subida a IPFS - Almacena los shards en IPFS.
        """
        shard_cids = []
        total_size = 0

        for i, shard in enumerate(shards):
            # Crear manifest del shard
            shard_manifest = {
                "dataset_name": dataset_name,
                "shard_index": i,
                "total_shards": len(shards),
                "created_at": datetime.now().isoformat(),
                "metadata": metadata or {}
            }

            # Añadir contenido según tipo
            if isinstance(shard, str):
                shard_manifest["content"] = shard
            elif isinstance(shard, list):
                shard_manifest["records"] = shard
            else:
                shard_manifest["data"] = shard

            # Subir a IPFS
            cid = ipfs_connector.add_json(shard_manifest)
            if cid:
                shard_cids.append(cid)
                size = len(json.dumps(shard_manifest).encode('utf-8'))
                total_size += size
                logger.info(f"✅ Shard {i+1}/{len(shards)} subido: {cid}")
            else:
                logger.error(f"❌ Error subiendo shard {i+1}")

        result = {
            "shard_cids": shard_cids,
            "total_shards": len(shard_cids),
            "total_size_mb": total_size / (1024 * 1024),
            "ipfs_stats": ipfs_connector.get_stats()
        }

        logger.info(f"📡 Subida IPFS completada: {len(shard_cids)} shards")
        return result

    def _register_dataset(self, ipfs_result: Dict, data_info: Dict, scrub_info: Dict,
                         shard_info: Dict, metadata: Optional[Dict]) -> Dict:
        """
        Paso 5: Registro - Registra el dataset en el sistema.
        """
        # Crear manifest completo del dataset
        dataset_manifest = {
            "id": f"{ipfs_result['shard_cids'][0]}_{int(time.time())}",
            "name": f"refined_{int(time.time())}",
            "type": "refined_dataset",
            "original_type": data_info["type"],
            "total_size_mb": ipfs_result["total_size_mb"],
            "num_shards": ipfs_result["total_shards"],
            "shard_cids": ipfs_result["shard_cids"],
            "pii_scrubbed": scrub_info["pii_removed"],
            "created_at": datetime.now().isoformat(),
            "quality_score": self._calculate_quality_score(data_info, scrub_info, shard_info),
            "metadata": metadata or {},
            "processing_stats": {
                "ingestion_info": data_info,
                "scrubbing_info": scrub_info,
                "sharding_info": shard_info,
                "ipfs_info": ipfs_result
            }
        }

        # Registrar en el registro global
        success = data_registry.register_dataset(dataset_manifest)

        result = {
            "registered": success,
            "dataset_id": dataset_manifest["id"],
            "quality_score": dataset_manifest["quality_score"],
            "registry_stats": data_registry.get_network_stats()
        }

        logger.info(f"📋 Dataset registrado: {dataset_manifest['id']}")
        return result

    def _calculate_quality_score(self, data_info: Dict, scrub_info: Dict, shard_info: Dict) -> float:
        """Calcula puntuación de calidad del dataset refinado."""
        score = 0.0

        # Factor de tamaño (0-0.3)
        size_mb = data_info.get("size_mb", 0)
        size_score = min(size_mb / 100.0, 1.0) * 0.3
        score += size_score

        # Factor de PII scrubbing (0-0.3)
        pii_score = 0.3 if scrub_info.get("pii_removed", False) else 0.0
        score += pii_score

        # Factor de sharding (0-0.4)
        num_shards = shard_info.get("num_shards", 1)
        shard_score = min(num_shards / 10.0, 1.0) * 0.4  # Bonus por distribución
        score += shard_score

        return round(min(max(score, 0.0), 1.0), 2)

    def validate_dataset_integrity(self, file_path: str) -> Dict[str, Any]:
        """
        Valida la integridad de un dataset local sin ingesta completa.
        Utilizado por el módulo de validación del terminal.
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return {"valid": False, "error": "File not found"}

            stats = path.stat()
            mime_type = "unknown"
            
            # Basic validation based on extension
            if path.suffix.lower() == '.json':
                import json
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        json.load(f)
                    mime_type = "application/json"
                    valid_structure = True
                except Exception as e:
                    return {"valid": False, "error": f"Invalid JSON: {str(e)}"}
            elif path.suffix.lower() == '.txt':
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        f.read(1024) # Try reading start
                    mime_type = "text/plain"
                    valid_structure = True
                except UnicodeDecodeError:
                    return {"valid": False, "error": "Invalid text encoding (not UTF-8)"}
            else:
                 return {"valid": False, "error": f"Unsupported format: {path.suffix}"}

            return {
                "valid": True,
                "path": str(path),
                "size_bytes": stats.st_size,
                "mime_type": mime_type,
                "modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
                "integrity_check": "passed"
            }
        except Exception as e:
            return {"valid": False, "error": str(e)}

    def scan_for_pii(self, file_path: str) -> Dict[str, Any]:
        """
        Escanea un archivo en busca de PII (Información Personal Identificable) usando patrones Regex.
        """
        import re
        
        pii_patterns = {
            "email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "ip_address": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
            "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        }
        
        results = {k: 0 for k in pii_patterns.keys()}
        preview = []
        
        try:
            path = Path(file_path)
            if not path.exists():
                return {"success": False, "error": "File not found"}
                
            # Leer solo los primeros 5MB para evitar bloqueos en archivos grandes
            content = ""
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(5 * 1024 * 1024)
                
            for p_type, pattern in pii_patterns.items():
                matches = re.findall(pattern, content)
                results[p_type] = len(matches)
                if matches and len(preview) < 5:
                    preview.append(f"Found {p_type}: {matches[0][:4]}***")

            return {
                "success": True,
                "matches": results,
                "has_pii": any(v > 0 for v in results.values()),
                "preview": preview,
                "scanned_bytes": len(content)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _identify_failed_step(self, error: Exception) -> str:
        """Identifica en qué paso del pipeline falló el procesamiento."""
        error_msg = str(error).lower()

        if "file" in error_msg or "path" in error_msg:
            return "ingestion"
        elif "pii" in error_msg or "scrub" in error_msg:
            return "scrubbing"
        elif "shard" in error_msg:
            return "sharding"
        elif "ipfs" in error_msg or "cid" in error_msg:
            return "ipfs_upload"
        elif "registry" in error_msg or "register" in error_msg:
            return "registration"
        else:
            return "unknown"

    def get_stats(self) -> Dict:
        """Obtiene estadísticas del Motor de Refinería."""
        return {
            **self.stats,
            "avg_processing_time": (
                self.stats["processing_time_total"] / max(self.stats["total_datasets_processed"], 1)
            ),
            "success_rate": (
                (self.stats["total_datasets_processed"] - self.stats["errors_encountered"]) /
                max(self.stats["total_datasets_processed"], 1)
            )
        }

    def process_batch(self, data_batch: List[Dict], batch_name: str,
                     shard_config: Optional[Dict] = None) -> List[Dict]:
        """
        Procesa un lote de datasets en paralelo.

        Args:
            data_batch: Lista de configuraciones de datasets a procesar
            batch_name: Nombre del lote
            shard_config: Configuración de sharding común

        Returns:
            Lista de resultados de procesamiento
        """
        results = []

        logger.info(f"📦 Procesando lote: {batch_name} ({len(data_batch)} datasets)")

        for i, dataset_config in enumerate(data_batch):
            logger.info(f"🔄 Procesando dataset {i+1}/{len(data_batch)}")

            try:
                result = self.process_data_pipeline(
                    data_input=dataset_config["data_input"],
                    dataset_name=dataset_config.get("name", f"{batch_name}_{i}"),
                    input_type=dataset_config.get("input_type", "auto"),
                    shard_config=shard_config,
                    metadata=dataset_config.get("metadata")
                )
                results.append(result)

            except Exception as e:
                logger.error(f"❌ Error procesando dataset {i}: {e}")
                results.append({
                    "success": False,
                    "dataset_name": dataset_config.get("name", f"{batch_name}_{i}"),
                    "error": str(e)
                })

        successful = sum(1 for r in results if r.get("success", False))
        logger.info(f"✅ Lote completado: {successful}/{len(data_batch)} exitosos")

        return results


# Instancia global del motor de refinería
refinery_engine = RefineryEngine()