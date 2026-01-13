import time
import threading
import logging
from typing import Dict, Any, Optional, Tuple
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError


class DatabaseMonitor:
    """Monitor MongoDB health and handle reconnections"""

    def __init__(
        self,
        mongodb_url: str,
        max_connection_time_ms: float = 100,
        max_query_time_ms: float = 500,
        check_interval: int = 30,
        logger: Optional[logging.Logger] = None,
        alert_manager: Optional[Any] = None,  # 🔔 NEW
    ):
        self.mongodb_url = mongodb_url
        self.max_connection_time_ms = max_connection_time_ms
        self.max_query_time_ms = max_query_time_ms
        self.check_interval = check_interval
        self.logger = logger or logging.getLogger(__name__)
        self.alert_manager = alert_manager

        self._running = False
        self._thread = None
        self._client: Optional[MongoClient] = None
        self._last_health = {}
        self._last_connected_state = False
        self._recovery_attempts = 0

    # ==============================
    # Lifecycle
    # ==============================

    def start(self):
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True,
            name="DatabaseMonitor"
        )
        self._thread.start()
        self.logger.info("📡 Database monitoring started")

    def stop(self):
        self._running = False

        if self._thread:
            self._thread.join(timeout=5)

        if self._client:
            try:
                self._client.close()
                self.logger.info("🧹 MongoDB connection closed")
            except Exception:
                pass

        self.logger.info("🛑 Database monitoring stopped")

    # ==============================
    # Hot Reload Support (.env)
    # ==============================

    def update_mongodb_url(self, new_url: str):
        if not new_url or new_url == self.mongodb_url:
            return

        self.logger.info("🔄 Reloading MongoDB connection from updated config")
        self.mongodb_url = new_url

        if self._client:
            try:
                self._client.close()
            except Exception:
                pass

        self._client = None
        self._last_connected_state = False

    # ==============================
    # Health Check
    # ==============================

    def check_health(self) -> Tuple[Dict[str, Any], bool]:
        state_changed = False

        try:
            if not self._client:
                self._client = MongoClient(
                    self.mongodb_url,
                    serverSelectionTimeoutMS=5000
                )

            start = time.time()
            self._client.admin.command("ping")
            connection_time_ms = (time.time() - start) * 1000

            server_status = self._client.admin.command("serverStatus")

            status = "connected"
            error_message = None

            if connection_time_ms > self.max_connection_time_ms:
                status = "slow"
                error_message = f"Slow response: {connection_time_ms:.1f}ms"

            health = {
                "status": status,
                "metrics": {
                    "connection_time_ms": round(connection_time_ms, 2),
                    "active_connections": server_status.get("connections", {}).get("active", 0),
                    "memory_mb": server_status.get("mem", {}).get("resident", 0)
                },
                "error_message": error_message,
                "is_reachable": True,
                "timestamp": time.time()
            }

            # 🔄 RECONNECTED
            if not self._last_connected_state:
                state_changed = True
                self.logger.info("✅ Database reconnected")

                if self.alert_manager:
                    self.alert_manager.send(
                        level="INFO",
                        title="Database Reconnected",
                        message="MongoDB connection has been restored successfully."
                    )

                self._recovery_attempts = 0

            self._last_connected_state = True
            self._last_health = health
            return health, state_changed

        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            health = {
                "status": "disconnected",
                "error_message": str(e),
                "is_reachable": False,
                "timestamp": time.time()
            }

            if self._last_connected_state:
                state_changed = True
                self.logger.warning("⚠️ Database disconnected")

                if self.alert_manager:
                    self.alert_manager.send(
                        level="CRITICAL",
                        title="Database Disconnected",
                        message=f"MongoDB is unreachable.\n\nError: {str(e)}"
                    )

            self._last_connected_state = False
            self._last_health = health
            self._recovery_attempts += 1

            return health, state_changed

        except Exception as e:
            self.logger.error(f"❌ Database health check error: {e}")
            return {
                "status": "error",
                "error_message": str(e),
                "is_reachable": False,
                "timestamp": time.time()
            }, False

    # ==============================
    # Background Loop
    # ==============================

    def _monitoring_loop(self):
        while self._running:
            try:
                self.check_health()
                time.sleep(self.check_interval)
            except Exception as e:
                self.logger.error(f"Monitoring loop error: {e}")
                time.sleep(5)
