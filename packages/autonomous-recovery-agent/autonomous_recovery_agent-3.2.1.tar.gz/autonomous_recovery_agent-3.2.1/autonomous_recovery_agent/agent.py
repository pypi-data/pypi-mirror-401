"""
Autonomous Recovery Agent - Main entry point
"""

import logging
import threading
import time
import os
from flask import Flask, request, jsonify
from typing import Optional, Dict, Any, Callable, List
from dataclasses import dataclass, field
from dotenv import dotenv_values

from .alerts.alert_manager import AlertManager
from .alerts.email_alert import EmailAlert

from .maintenance.manager import MaintenanceManager, MaintenanceLevel
from .traffic.throttler import TrafficThrottler
from .config_manager import ConfigurationManager
from .monitoring.disk_monitor import DiskMonitor
from .monitoring.service_monitor import ServiceMonitor
from .monitoring.database_monitor import DatabaseMonitor
from .recovery.engine import RecoveryEngine
from .flask_integration import FlaskIntegration
from .mongodb_integration import patch_pymongo


# =====================================================
# CONFIG
# =====================================================

@dataclass
class AgentConfig:
    enabled: bool = True
    log_level: str = "INFO"
    check_interval: int = 30

    service_monitoring: bool = True
    max_service_memory_mb: float = 500
    max_service_cpu_percent: float = 80

    database_monitoring: bool = True
    mongodb_url: Optional[str] = None
    max_db_connection_time_ms: float = 100
    max_db_query_time_ms: float = 500

    auto_recovery: bool = True
    max_restart_attempts: int = 3
    restart_cooldown: int = 60

    disk_monitoring: bool = True
    disk_cleanup_threshold: float = 0.85
    disk_critical_threshold: float = 0.95
    max_log_age_days: int = 30
    max_temp_age_hours: int = 24

    config_management: bool = True
    config_dirs: List[str] = field(default_factory=lambda: [".", "config"])
    watch_config_files: bool = True

    maintenance_mode: bool = True
    maintenance_status_file: str = "maintenance_status.json"

    traffic_throttling: bool = True
    default_rps: int = 100
    overload_threshold: float = 0.8
    recovery_threshold: float = 0.5

    enable_web_ui: bool = True
    web_ui_port: int = 8081
    web_ui_host: str = "0.0.0.0"

    enable_api: bool = True
    api_prefix: str = "/recovery"


# =====================================================
# AGENT
# =====================================================

class AutonomousRecoveryAgent:

    def __init__(
        self,
        flask_app: Optional[Flask] = None,
        mongodb_url: Optional[str] = None,
        config: Optional[AgentConfig] = None,
        logger: Optional[logging.Logger] = None,
    ):
        self.flask_app = flask_app
        self.mongodb_url = mongodb_url
        self.config = config or AgentConfig()
        self.logger = logger or logging.getLogger("AutonomousRecoveryAgent")

        self._running = False

        self._setup_logging()
        self._init_alerts()
        self._initialize_components()

    # -------------------------------------------------
    # LOGGING
    # -------------------------------------------------

    def _setup_logging(self):
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(self.config.log_level)

    # -------------------------------------------------
    # ALERTS
    # -------------------------------------------------

    def _init_alerts(self):
        self.email_alert = EmailAlert(
            smtp_host=os.getenv("SMTP_HOST"),
            smtp_port=int(os.getenv("SMTP_PORT", 587)),
            username=os.getenv("SMTP_USERNAME"),
            password=os.getenv("SMTP_PASSWORD"),
            from_email=os.getenv("ALERT_FROM_EMAIL"),
            to_emails=os.getenv("ALERT_TO_EMAILS", "").split(","),
            logger=self.logger,
        )

        self.alert_manager = AlertManager(
            email_alert=self.email_alert,
            logger=self.logger,
        )

    # -------------------------------------------------
    # COMPONENTS
    # -------------------------------------------------

    def _initialize_components(self):

        if self.config.service_monitoring:
            self.service_monitor = ServiceMonitor(
                process_name="python",
                max_memory_mb=self.config.max_service_memory_mb,
                max_cpu_percent=self.config.max_service_cpu_percent,
                logger=self.logger,
            )

        if self.config.database_monitoring and self.mongodb_url:
            self.database_monitor = DatabaseMonitor(
                mongodb_url=self.mongodb_url,
                max_connection_time_ms=self.config.max_db_connection_time_ms,
                max_query_time_ms=self.config.max_db_query_time_ms,
                logger=self.logger,
            )

        if self.config.disk_monitoring:
            self.disk_monitor = DiskMonitor(logger=self.logger)

        if self.config.traffic_throttling and self.flask_app:
            self.traffic_throttler = TrafficThrottler(logger=self.logger)

        if self.config.maintenance_mode:
            self.maintenance_manager = MaintenanceManager(
                status_file=self.config.maintenance_status_file,
                logger=self.logger,
            )

        if self.config.config_management:
            self.config_manager = ConfigurationManager(
                config_dirs=self.config.config_dirs,
                logger=self.logger,
            )

        if self.config.auto_recovery:
            self.recovery_engine = RecoveryEngine(logger=self.logger)

        patch_pymongo()

        if self.flask_app:
            self.flask_integration = FlaskIntegration(
                flask_app=self.flask_app,
                agent=self,
                api_prefix=self.config.api_prefix,
                enable_api=self.config.enable_api,
                logger=self.logger,
            )

    # -------------------------------------------------
    # START / STOP
    # -------------------------------------------------

    def start(self):
        self.logger.info("🚀 Starting Autonomous Recovery Agent")

        self._running = True

        if self.service_monitor:
            self.service_monitor.start()

        if self.database_monitor:
            self.database_monitor.start()

        if self.disk_monitor:
            self.disk_monitor.start()

        if self.config_manager and self.config.watch_config_files:
            self.config_manager.start_watching()
            self._register_config_callbacks()

        threading.Thread(
            target=self._monitoring_loop,
            daemon=True,
            name="AgentMonitor",
        ).start()

        self.logger.info("✅ Agent started successfully")

    def stop(self):
        self.logger.info("🛑 Stopping agent")
        self._running = False

    # -------------------------------------------------
    # MONITOR LOOP
    # -------------------------------------------------

    def _monitoring_loop(self):
        while self._running:
            try:
                if self.service_monitor:
                    health = self.service_monitor.check_health()
                    if health["status"] != "healthy":
                        self._handle_service_unhealthy(health)

                if self.database_monitor:
                    health, changed = self.database_monitor.check_health()
                    if not health["is_reachable"]:
                        self._handle_database_unhealthy(health)

                time.sleep(self.config.check_interval)

            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
                time.sleep(5)

    # -------------------------------------------------
    # HANDLERS
    # -------------------------------------------------

    def _handle_service_unhealthy(self, health):
        self.logger.warning("⚠️ Service unhealthy")

        self.alert_manager.notify(
            title="🚨 Service Unhealthy",
            message=health.get("error_message"),
            severity="WARNING",
        )

        if self.recovery_engine:
            self.recovery_engine.recover_service("flask", health)

    def _handle_database_unhealthy(self, health):
        self.logger.error("🚨 Database down")

        self.alert_manager.notify(
            title="🚨 Database Down",
            message=health.get("error_message"),
            severity="CRITICAL",
        )

        if self.recovery_engine:
            self.recovery_engine.recover_database("mongodb", health)

    # -------------------------------------------------
    # CONFIG HOT RELOAD
    # -------------------------------------------------

    def _register_config_callbacks(self):
        self.config_manager.register_callback(".env", self._on_env_change)

    def _on_env_change(self, _, change):
        env = dotenv_values(change.file_path)
        new_url = env.get("MONGODB_URL")

        if new_url and self.database_monitor:
            self.logger.info("🔄 MongoDB URL updated from .env")
            self.database_monitor.update_mongodb_url(new_url)