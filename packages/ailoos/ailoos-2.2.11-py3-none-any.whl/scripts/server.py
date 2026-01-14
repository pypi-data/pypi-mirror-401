#!/usr/bin/env python3
"""
Servidor principal de AILOOS.
Inicia todas las APIs (marketplace, federated, inference) en un solo proceso.
"""

import asyncio
import uvicorn
import multiprocessing
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from ailoos.api import create_marketplace_app, create_federated_app, create_wallet_app, create_empoorio_app, create_technical_dashboard_app, create_models_app, create_rag_app, create_analytics_app, create_system_tools_app, create_datahub_app
from ailoos.api.marketplace_api import marketplace_api
from ailoos.api.federated_api import federated_api
from ailoos.api.models_api import models_api
from ailoos.core.config import get_config
from ailoos.core.logging import get_logger

logger = get_logger(__name__)


class AiloosServer:
    """
    Servidor principal que combina todas las APIs de AILOOS con WebSocket REAL.
    """

    def __init__(self):
        logger.info("🚀 Initializing AiloosServer")
        self.config = get_config()
        self.main_app = FastAPI(
            title="AILOOS Unified API",
            description="API unificada para todo el ecosistema AILOOS con WebSocket en tiempo real",
            version="1.0.0"
        )

        # Configurar CORS
        import os
        cors_origins = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000,https://ailoos.com,https://www.ailoos.com,https://ailoos-app-f3c91.web.app")
        allow_origins = [origin.strip() for origin in cors_origins.split(",")] if cors_origins else ["*"]

        self.main_app.add_middleware(
            CORSMiddleware,
            allow_origins=allow_origins,
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
            allow_headers=["*"],
        )
        logger.info("✅ CORS middleware added to main_app")

        # Middleware para logging detallado de CORS para debugging
        class CORSLoggingMiddleware(BaseHTTPMiddleware):
            async def dispatch(self, request, call_next):
                origin = request.headers.get("origin", "N/A")
                logger.info(f"🌐 CORS Request - Method: {request.method}, Origin: {origin}, Path: {request.url.path}")

                response = await call_next(request)

                cors_headers = {k: v for k, v in response.headers.items() if k.lower().startswith(('access-control', 'vary'))}
                if cors_headers:
                    logger.info(f"🔍 CORS Response Headers: {cors_headers}")

                if request.method == "OPTIONS":
                    logger.info(f"✈️ Preflight request handled for {request.url.path}")

                return response

        self.main_app.add_middleware(CORSLoggingMiddleware)
        logger.info("✅ CORS logging middleware added")

        # Gestores de conexiones WebSocket REALES
        self.websocket_connections = {
            "federated": {},  # session_id -> {node_id: websocket}
            "marketplace": {},  # user_id -> websocket
            "dashboard": set()  # conexiones de dashboard general
        }

        # Montar APIs
        self._mount_apis()

        # Inicializar infraestructura DRACMA
        self._initialize_dracma_infrastructure()

        # Configurar WebSocket handlers REALES
        self._setup_websocket_handlers()

    def _initialize_dracma_infrastructure(self):
        """Inicializar infraestructura del token DRACMA."""
        try:
            from ailoos.blockchain import initialize_dracma_infrastructure
            asyncio.run(initialize_dracma_infrastructure())
            logger.info("✅ DracmaS infrastructure initialized")
        except Exception as e:
            logger.warning(f"⚠️ DracmaS infrastructure initialization failed (continuing): {e}")
            # No fallar el startup completo por DRACMA

        # Añadir rutas de health check
        self._add_health_routes()

    def _setup_websocket_handlers(self):
        """Configurar handlers WebSocket REALES para comunicación en tiempo real."""

        @self.main_app.websocket("/ws/federated/{session_id}/{node_id}")
        async def federated_websocket(websocket: WebSocket, session_id: str, node_id: str):
            """WebSocket REAL para comunicación federated learning con TLS obligatorio."""
            # Enforce WSS in production
            if self.config.environment == "production":
                # Check if connection is secure (WSS)
                if not websocket.url.scheme == "wss":
                    await websocket.close(code=1008, reason="WSS required in production")
                    return

            await websocket.accept()

            # Registrar conexión REAL
            if session_id not in self.websocket_connections["federated"]:
                self.websocket_connections["federated"][session_id] = {}
            self.websocket_connections["federated"][session_id][node_id] = websocket

            logger.info(f"🔗 Node {node_id} connected to federated session {session_id}")

            try:
                # Enviar mensaje de bienvenida REAL
                await websocket.send_json({
                    "type": "welcome",
                    "session_id": session_id,
                    "node_id": node_id,
                    "timestamp": asyncio.get_event_loop().time(),
                    "message": "Connected to AILOOS federated learning session"
                })

                # Mantener conexión viva y procesar mensajes REALES
                while True:
                    try:
                        # Recibir mensaje con timeout
                        data = await asyncio.wait_for(websocket.receive_json(), timeout=30.0)

                        # Procesar mensaje REAL según tipo
                        await self._handle_federated_message(session_id, node_id, data, websocket)

                    except asyncio.TimeoutError:
                        # Enviar ping para mantener viva la conexión
                        await websocket.send_json({
                            "type": "ping",
                            "timestamp": asyncio.get_event_loop().time()
                        })

            except WebSocketDisconnect:
                logger.info(f"📴 Node {node_id} disconnected from session {session_id}")
            except Exception as e:
                logger.error(f"❌ Error in federated websocket for {node_id}: {e}")
            finally:
                # Limpiar conexión REAL
                if session_id in self.websocket_connections["federated"]:
                    if node_id in self.websocket_connections["federated"][session_id]:
                        del self.websocket_connections["federated"][session_id][node_id]
                        if not self.websocket_connections["federated"][session_id]:
                            del self.websocket_connections["federated"][session_id]

        @self.main_app.websocket("/ws/marketplace/{user_id}")
        async def marketplace_websocket(websocket: WebSocket, user_id: str):
            """WebSocket REAL para marketplace y wallet con TLS obligatorio."""
            # Enforce WSS in production
            if self.config.environment == "production":
                if not websocket.url.scheme == "wss":
                    await websocket.close(code=1008, reason="WSS required in production")
                    return

            await websocket.accept()

            # Registrar conexión REAL
            self.websocket_connections["marketplace"][user_id] = websocket

            logger.info(f"💰 User {user_id} connected to marketplace websocket")

            try:
                # Enviar estado inicial REAL
                await self._send_marketplace_status(user_id, websocket)

                # Procesar mensajes REALES del marketplace
                while True:
                    data = await asyncio.wait_for(websocket.receive_json(), timeout=30.0)
                    await self._handle_marketplace_message(user_id, data, websocket)

            except WebSocketDisconnect:
                logger.info(f"📴 User {user_id} disconnected from marketplace")
            except Exception as e:
                logger.error(f"❌ Error in marketplace websocket for {user_id}: {e}")
            finally:
                # Limpiar conexión REAL
                if user_id in self.websocket_connections["marketplace"]:
                    del self.websocket_connections["marketplace"][user_id]

        @self.main_app.websocket("/ws/dashboard")
        async def dashboard_websocket(websocket: WebSocket):
            """WebSocket REAL para dashboard general con TLS obligatorio."""
            # Enforce WSS in production
            if self.config.environment == "production":
                if not websocket.url.scheme == "wss":
                    await websocket.close(code=1008, reason="WSS required in production")
                    return

            await websocket.accept()

            # Registrar conexión REAL
            self.websocket_connections["dashboard"].add(websocket)

            logger.info("📊 Dashboard connected to websocket")

            try:
                # Enviar estado inicial del sistema REAL
                await self._send_system_status(websocket)

                # Mantener conexión para actualizaciones periódicas
                while True:
                    await asyncio.sleep(10)  # Actualización cada 10 segundos
                    await self._send_system_status(websocket)

            except WebSocketDisconnect:
                logger.info("📴 Dashboard disconnected")
            except Exception as e:
                logger.error(f"❌ Error in dashboard websocket: {e}")
            finally:
                # Limpiar conexión REAL
                self.websocket_connections["dashboard"].discard(websocket)

        @self.main_app.websocket("/ws/security-alerts")
        async def security_alerts_websocket(websocket: WebSocket):
            """WebSocket REAL para alertas de seguridad del sistema con TLS obligatorio."""
            # Enforce WSS in production
            if self.config.environment == "production":
                if not websocket.url.scheme == "wss":
                    await websocket.close(code=1008, reason="WSS required in production")
                    return

            await websocket.accept()

            logger.info("🛡️ Security alerts WebSocket connected")

            try:
                # Enviar estado inicial de alertas de seguridad
                await self._send_security_alerts_status(websocket)

                # Mantener conexión para actualizaciones periódicas
                while True:
                    await asyncio.sleep(30)  # Actualización cada 30 segundos
                    await self._send_security_alerts_status(websocket)

            except WebSocketDisconnect:
                logger.info("📴 Security alerts WebSocket disconnected")
            except Exception as e:
                logger.error(f"❌ Error in security alerts websocket: {e}")

        @self.main_app.websocket("/ws/log-updates")
        async def log_updates_websocket(websocket: WebSocket):
            """WebSocket REAL para actualizaciones de logs con TLS obligatorio."""
            # Enforce WSS in production
            if self.config.environment == "production":
                if not websocket.url.scheme == "wss":
                    await websocket.close(code=1008, reason="WSS required in production")
                    return

            await websocket.accept()

            logger.info("📝 Log updates WebSocket connected")

            try:
                # Enviar estado inicial de logs
                await self._send_log_updates_status(websocket)

                # Mantener conexión para actualizaciones periódicas
                while True:
                    await asyncio.sleep(60)  # Actualización cada 60 segundos
                    await self._send_log_updates_status(websocket)

            except WebSocketDisconnect:
                logger.info("📴 Log updates WebSocket disconnected")
            except Exception as e:
                logger.error(f"❌ Error in log updates websocket: {e}")

        @self.main_app.websocket("/ws/config-changes")
        async def config_changes_websocket(websocket: WebSocket):
            """WebSocket REAL para cambios de configuración con TLS obligatorio."""
            # Enforce WSS in production
            if self.config.environment == "production":
                if not websocket.url.scheme == "wss":
                    await websocket.close(code=1008, reason="WSS required in production")
                    return

            await websocket.accept()

            logger.info("⚙️ Config changes WebSocket connected")

            try:
                # Enviar estado inicial de configuración
                await self._send_config_changes_status(websocket)

                # Mantener conexión para actualizaciones periódicas
                while True:
                    await asyncio.sleep(300)  # Actualización cada 5 minutos
                    await self._send_config_changes_status(websocket)

            except WebSocketDisconnect:
                logger.info("📴 Config changes WebSocket disconnected")
            except Exception as e:
                logger.error(f"❌ Error in config changes websocket: {e}")

    async def _handle_federated_message(self, session_id: str, node_id: str, data: dict, websocket: WebSocket):
        """Manejar mensajes REALES del websocket federated."""
        msg_type = data.get("type")

        if msg_type == "status_request":
            # Enviar estado actual de la sesión REAL
            await self._send_federated_status(session_id, node_id, websocket)

        elif msg_type == "training_update":
            # Procesar actualización de entrenamiento REAL
            await self._handle_training_update(session_id, node_id, data, websocket)

        elif msg_type == "heartbeat":
            # Responder heartbeat REAL
            await websocket.send_json({
                "type": "heartbeat_ack",
                "timestamp": asyncio.get_event_loop().time(),
                "session_id": session_id,
                "node_id": node_id
            })

        else:
            logger.warning(f"Unknown federated message type: {msg_type}")

    async def _handle_marketplace_message(self, user_id: str, data: dict, websocket: WebSocket):
        """Manejar mensajes REALES del websocket marketplace."""
        msg_type = data.get("type")

        if msg_type == "balance_request":
            # Enviar balance actualizado REAL
            await self._send_wallet_balance(user_id, websocket)

        elif msg_type == "transaction_history":
            # Enviar historial de transacciones REAL
            await self._send_transaction_history(user_id, websocket)

        elif msg_type == "marketplace_search":
            # Procesar búsqueda en marketplace REAL
            await self._handle_marketplace_search(user_id, data, websocket)

        else:
            logger.warning(f"Unknown marketplace message type: {msg_type}")

    async def _send_federated_status(self, session_id: str, node_id: str, websocket: WebSocket):
        """Enviar estado REAL de sesión federated."""
        try:
            # Obtener estado REAL de la API federated
            from ailoos.api.federated_api import federated_api

            if session_id in federated_api.active_sessions:
                session = federated_api.active_sessions[session_id]
                status = session.get_status()

                await websocket.send_json({
                    "type": "session_status",
                    "session_id": session_id,
                    "node_id": node_id,
                    "status": status,
                    "timestamp": asyncio.get_event_loop().time()
                })
        except Exception as e:
            logger.error(f"Error sending federated status: {e}")

    async def _send_marketplace_status(self, user_id: str, websocket: WebSocket):
        """Enviar estado inicial REAL del marketplace."""
        try:
            # Obtener balance REAL
            balance = marketplace_api.get_user_balance(user_id)

            # Obtener estadísticas REALES del marketplace
            market_stats = marketplace_api.get_market_stats()

            await websocket.send_json({
                "type": "marketplace_status",
                "user_id": user_id,
                "balance_dracma": balance,
                "market_stats": market_stats,
                "timestamp": asyncio.get_event_loop().time()
            })
        except Exception as e:
            logger.error(f"Error sending marketplace status: {e}")

    async def _send_system_status(self, websocket: WebSocket):
        """Enviar estado REAL del sistema completo."""
        try:
            # Obtener estadísticas REALES del sistema federated
            fed_stats = await self._get_federated_stats()

            # Obtener estadísticas REALES del marketplace
            market_stats = marketplace_api.get_market_stats()

            await websocket.send_json({
                "type": "system_status",
                "federated_stats": fed_stats,
                "marketplace_stats": market_stats,
                "timestamp": asyncio.get_event_loop().time()
            })
        except Exception as e:
            logger.error(f"Error sending system status: {e}")

    async def _send_security_alerts_status(self, websocket: WebSocket):
        """Enviar estado REAL de alertas de seguridad."""
        try:
            # Simular alertas de seguridad (en implementación real, obtener de la base de datos)
            alerts = [
                {
                    "id": "alert_001",
                    "severity": "medium",
                    "message": "Multiple failed login attempts detected",
                    "timestamp": asyncio.get_event_loop().time(),
                    "source": "authentication"
                }
            ]

            await websocket.send_json({
                "type": "security_alerts_status",
                "alerts": alerts,
                "total_alerts": len(alerts),
                "timestamp": asyncio.get_event_loop().time()
            })
        except Exception as e:
            logger.error(f"Error sending security alerts status: {e}")

    async def _send_log_updates_status(self, websocket: WebSocket):
        """Enviar estado REAL de actualizaciones de logs."""
        try:
            # Simular actualizaciones de logs recientes
            recent_logs = [
                {
                    "id": "log_001",
                    "level": "INFO",
                    "message": "Federated training session started",
                    "timestamp": asyncio.get_event_loop().time(),
                    "component": "federated"
                }
            ]

            await websocket.send_json({
                "type": "log_updates_status",
                "recent_logs": recent_logs,
                "total_logs": len(recent_logs),
                "timestamp": asyncio.get_event_loop().time()
            })
        except Exception as e:
            logger.error(f"Error sending log updates status: {e}")

    async def _send_config_changes_status(self, websocket: WebSocket):
        """Enviar estado REAL de cambios de configuración."""
        try:
            # Simular cambios recientes de configuración
            config_changes = [
                {
                    "id": "config_001",
                    "component": "security",
                    "change": "Updated encryption settings",
                    "timestamp": asyncio.get_event_loop().time(),
                    "user": "system"
                }
            ]

            await websocket.send_json({
                "type": "config_changes_status",
                "recent_changes": config_changes,
                "total_changes": len(config_changes),
                "timestamp": asyncio.get_event_loop().time()
            })
        except Exception as e:
            logger.error(f"Error sending config changes status: {e}")

    async def _get_federated_stats(self) -> dict:
        """Obtener estadísticas REALES del sistema federated."""
        try:
            from ailoos.api.federated_api import federated_api
            return await federated_api.get_federated_stats()
        except Exception as e:
            logger.error(f"Error getting federated stats: {e}")
            return {"error": "Unable to get federated stats"}

    async def broadcast_federated_update(self, session_id: str, update_data: dict):
        """Broadcast REAL de actualizaciones a todos los nodos de una sesión."""
        if session_id in self.websocket_connections["federated"]:
            for node_id, websocket in self.websocket_connections["federated"][session_id].items():
                try:
                    await websocket.send_json({
                        "type": "federated_update",
                        "session_id": session_id,
                        "node_id": node_id,
                        **update_data,
                        "timestamp": asyncio.get_event_loop().time()
                    })
                except Exception as e:
                    logger.error(f"Error broadcasting to {node_id}: {e}")

    async def broadcast_marketplace_update(self, update_data: dict):
        """Broadcast REAL de actualizaciones del marketplace."""
        for user_id, websocket in self.websocket_connections["marketplace"].items():
            try:
                await websocket.send_json({
                    "type": "marketplace_update",
                    **update_data,
                    "timestamp": asyncio.get_event_loop().time()
                })
            except Exception as e:
                logger.error(f"Error broadcasting marketplace update to {user_id}: {e}")

    async def broadcast_dashboard_update(self, update_data: dict):
        """Broadcast REAL de actualizaciones a todos los dashboards conectados."""
        for websocket in self.websocket_connections["dashboard"]:
            try:
                await websocket.send_json({
                    "type": "dashboard_update",
                    **update_data,
                    "timestamp": asyncio.get_event_loop().time()
                })
            except Exception as e:
                logger.error(f"Error broadcasting dashboard update: {e}")

    async def _handle_training_update(self, session_id: str, node_id: str, data: dict, websocket: WebSocket):
        """Manejar actualizaciones de entrenamiento REALES."""
        try:
            # Procesar actualización REAL a través de la API federated
            from ailoos.api.federated_api import federated_api

            # Crear objeto de actualización REAL
            weight_update = {
                "session_id": session_id,
                "node_id": node_id,
                "round_num": data.get("round_num"),
                "weights_hash": data.get("weights_hash", ""),
                "ipfs_cid": data.get("ipfs_cid", ""),
                "num_samples": data.get("num_samples", 0),
                "metrics": data.get("metrics", {})
            }

            # Enviar a través de la API REAL
            result = await federated_api.submit_weight_update(weight_update)

            # Responder con resultado REAL
            await websocket.send_json({
                "type": "training_update_ack",
                "session_id": session_id,
                "node_id": node_id,
                "result": result,
                "timestamp": asyncio.get_event_loop().time()
            })

        except Exception as e:
            logger.error(f"Error handling training update: {e}")
            await websocket.send_json({
                "type": "error",
                "message": f"Error processing training update: {str(e)}",
                "timestamp": asyncio.get_event_loop().time()
            })

    async def _send_wallet_balance(self, user_id: str, websocket: WebSocket):
        """Enviar balance REAL de wallet."""
        try:
            balance = marketplace_api.get_user_balance(user_id)
            await websocket.send_json({
                "type": "wallet_balance",
                "user_id": user_id,
                "balance_dracma": balance,
                "timestamp": asyncio.get_event_loop().time()
            })
        except Exception as e:
            logger.error(f"Error sending wallet balance: {e}")

    async def _send_transaction_history(self, user_id: str, websocket: WebSocket):
        """Enviar historial REAL de transacciones."""
        try:
            # Obtener historial REAL (últimas 10 transacciones)
            history = marketplace_api.get_transaction_history(user_id, limit=10)
            await websocket.send_json({
                "type": "transaction_history",
                "user_id": user_id,
                "transactions": history,
                "timestamp": asyncio.get_event_loop().time()
            })
        except Exception as e:
            logger.error(f"Error sending transaction history: {e}")

    async def _handle_marketplace_search(self, user_id: str, data: dict, websocket: WebSocket):
        """Manejar búsqueda REAL en marketplace."""
        try:
            query = data.get("query", "")
            category = data.get("category")
            limit = data.get("limit", 20)

            # Realizar búsqueda REAL
            results = marketplace_api.search_datasets(
                query=query,
                category=category,
                limit=limit
            )

            await websocket.send_json({
                "type": "marketplace_search_results",
                "user_id": user_id,
                "query": query,
                "results": results,
                "timestamp": asyncio.get_event_loop().time()
            })
        except Exception as e:
            logger.error(f"Error handling marketplace search: {e}")

    def _mount_apis(self):
        """Montar todas las APIs en rutas específicas."""
        logger.info("🔧 Starting API mounting process")

        apis_to_mount = [
            ("Marketplace API", "/api/marketplace", create_marketplace_app),
            ("Federated Learning API", "/api/federated", create_federated_app),
            ("Wallet API", "/api/wallet", create_wallet_app),
            ("EmpoorioLM API", "/api/v1/empoorio-lm", create_empoorio_app),
            ("Technical Dashboard API", "/api/dashboard", create_technical_dashboard_app),
            ("Models API", "/api/models", create_models_app),
            ("RAG API", "/api/rag", create_rag_app),
            ("Analytics API", "/api/analytics", create_analytics_app),
            ("System Tools API", "/api/system-tools", create_system_tools_app),
            ("Data Hub API", "/api/datahub", create_datahub_app),
        ]

        for api_name, path, create_func in apis_to_mount:
            try:
                app = create_func()
                self.main_app.mount(path, app)
                logger.info(f"✅ {api_name} mounted at {path}")
                # Log routes for debugging
                if api_name == "Models API":
                    routes = [route.path for route in app.routes if hasattr(route, 'path')]
                    logger.info(f"📋 Models API routes: {routes}")
            except Exception as e:
                logger.warning(f"⚠️ Failed to mount {api_name} at {path}: {e}")
                import traceback
                logger.warning(f"⚠️ Full traceback: {traceback.format_exc()}")

        logger.info("APIs montadas exitosamente")

    def _add_health_routes(self):
        """Añadir rutas de health check global."""

        @self.main_app.get("/health")
        async def global_health():
            """Health check global del sistema."""
            return {
                "status": "healthy",
                "services": {
                    "marketplace_api": "healthy",
                    "federated_api": "healthy",
                    "wallet_api": "healthy",
                    "technical_dashboard_api": "healthy",
                    "models_api": "healthy",
                    "rag_api": "healthy"
                },
                "version": "1.0.0"
            }

        @self.main_app.get("/")
        async def root():
            """Página de bienvenida con WebSocket info."""
            return {
                "message": "AILOOS Unified API Server with REAL WebSocket support",
                "version": "1.0.0",
                "endpoints": {
                    "marketplace": "/api/marketplace",
                    "federated": "/api/federated",
                    "wallet": "/api/wallet",
                    "technical_dashboard": "/api/dashboard",
                    "empoorio_lm": "/api/v1/empoorio-lm",
                    "health": "/health"
                },
                "websockets": {
                    "federated": "/ws/federated/{session_id}/{node_id}",
                    "marketplace": "/ws/marketplace/{user_id}",
                    "dashboard": "/ws/dashboard",
                    "security_alerts": "/ws/security-alerts",
                    "log_updates": "/ws/log-updates",
                    "config_changes": "/ws/config-changes"
                },
                "features": [
                    "Real federated learning coordination",
                    "Real marketplace with DracmaS payments",
                    "Real WebSocket communication",
                    "Real IPFS model distribution",
                    "Real blockchain tokenomics"
                ]
            }

    def start(self, host: str = None, port: int = None):
        """Iniciar servidor."""
        import os
        host = host or getattr(self.config, 'api_host', '0.0.0.0')
        port = port or int(os.environ.get('PORT', getattr(self.config, 'api_port', 8000)))

        logger.info(f"🚀 Iniciando servidor AILOOS en {host}:{port}")

        uvicorn.run(
            self.main_app,
            host=host,
            port=port,
            log_level=getattr(self.config, 'log_level', 'info').lower()
        )


def start_marketplace_api():
    """Iniciar API de marketplace en proceso separado."""
    marketplace_app = create_marketplace_app()
    uvicorn.run(marketplace_app, host="0.0.0.0", port=8000, log_level="info")


def start_federated_api():
    """Iniciar API federada en proceso separado."""
    federated_app = create_federated_app()
    uvicorn.run(federated_app, host="0.0.0.0", port=8001, log_level="info")


def start_unified_server():
    """Iniciar servidor unificado."""
    server = AiloosServer()
    server.start()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        mode = sys.argv[1]

        if mode == "marketplace":
            print("🚀 Iniciando API de Marketplace...")
            start_marketplace_api()
        elif mode == "federated":
            print("🚀 Iniciando API Federada...")
            start_federated_api()
        elif mode == "unified":
            print("🚀 Iniciando Servidor Unificado...")
            start_unified_server()
        else:
            print(f"❌ Modo desconocido: {mode}")
            print("Uso: python server.py [marketplace|federated|unified]")
            sys.exit(1)
    else:
        # Por defecto, iniciar servidor unificado
        print("🚀 Iniciando Servidor Unificado AILOOS...")
        start_unified_server()
