"""
Autonomous Recovery Agent - Main entry point
"""
import logging
import threading
import time
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass

from .monitoring.service_monitor import ServiceMonitor
from .monitoring.database_monitor import DatabaseMonitor
from .recovery.engine import RecoveryEngine
from .flask_integration import FlaskIntegration
from .mongodb_integration import patch_pymongo


@dataclass
class AgentConfig:
    """Configuration for the autonomous recovery agent"""
    
    # General settings
    enabled: bool = True
    log_level: str = "INFO"
    check_interval: int = 30
    
    # Service monitoring
    service_monitoring: bool = True
    max_service_memory_mb: float = 500
    max_service_cpu_percent: float = 80
    
    # Database monitoring
    database_monitoring: bool = True
    mongodb_url: Optional[str] = None
    max_db_connection_time_ms: float = 100
    max_db_query_time_ms: float = 500
    
    # Recovery settings
    auto_recovery: bool = True
    max_restart_attempts: int = 3
    restart_cooldown: int = 60
    
    # Web UI
    enable_web_ui: bool = True
    web_ui_port: int = 8081
    web_ui_host: str = "0.0.0.0"
    
    # API endpoints
    enable_api: bool = True
    api_prefix: str = "/recovery"
    
    # Custom callbacks
    on_service_unhealthy: Optional[Callable] = None
    on_database_unhealthy: Optional[Callable] = None
    on_recovery_completed: Optional[Callable] = None


class AutonomousRecoveryAgent:
    """
    Autonomous Recovery Agent for Flask + MongoDB applications
    
    Usage:
        agent = AutonomousRecoveryAgent(
            flask_app=app,
            mongodb_url="mongodb://localhost:27017"
        )
        agent.start()
    """
    
    def __init__(
        self,
        flask_app=None,
        mongodb_url: Optional[str] = None,
        config: Optional[AgentConfig] = None,
        logger: Optional[logging.Logger] = None
    ):
        self.flask_app = flask_app
        self.mongodb_url = mongodb_url
        self.config = config or AgentConfig()
        self.logger = logger or logging.getLogger(__name__)
        
        # Initialize components
        self.service_monitor = None
        self.database_monitor = None
        self.recovery_engine = None
        self.flask_integration = None
        
        # Runtime state
        self._running = False
        self._monitor_thread = None
        self._web_ui_thread = None
        
        self._setup_logging()
        self._initialize_components()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(getattr(logging, self.config.log_level))
    
    def _initialize_components(self):
        """Initialize monitoring and recovery components"""
        
        # Initialize service monitor
        if self.config.service_monitoring:
            from .monitoring.service_monitor import ServiceMonitor
            self.service_monitor = ServiceMonitor(
                process_name="python",
                max_memory_mb=self.config.max_service_memory_mb,
                max_cpu_percent=self.config.max_service_cpu_percent,
                logger=self.logger
            )
        
        # Initialize database monitor
        if self.config.database_monitoring and self.mongodb_url:
            from .monitoring.database_monitor import DatabaseMonitor
            self.database_monitor = DatabaseMonitor(
                mongodb_url=self.mongodb_url,
                max_connection_time_ms=self.config.max_db_connection_time_ms,
                max_query_time_ms=self.config.max_db_query_time_ms,
                logger=self.logger
            )
        
        # Initialize recovery engine
        if self.config.auto_recovery:
            from .recovery.engine import RecoveryEngine
            self.recovery_engine = RecoveryEngine(
                max_attempts=self.config.max_restart_attempts,
                cooldown_seconds=self.config.restart_cooldown,
                logger=self.logger
            )
        
        # Patch pymongo for automatic recovery
        try:
            from .mongodb_integration import patch_pymongo
            patch_pymongo()
            self.logger.info("pymongo patched for automatic recovery")
        except Exception as e:
            self.logger.warning(f"Failed to patch pymongo: {e}")
        
        # Integrate with Flask
        if self.flask_app:
            from .flask_integration import FlaskIntegration
            self.flask_integration = FlaskIntegration(
                flask_app=self.flask_app,
                agent=self,
                api_prefix=self.config.api_prefix,
                enable_api=self.config.enable_api,
                logger=self.logger
            )
    
    def start(self):
        """Start the autonomous recovery agent"""
        if self._running:
            self.logger.warning("Agent is already running")
            return
        
        self.logger.info("🚀 Starting Autonomous Recovery Agent...")
        
        try:
            # Start service monitoring
            if self.service_monitor:
                self.service_monitor.start()
                self.logger.info("✅ Service monitoring started")
            
            # Start database monitoring
            if self.database_monitor:
                self.database_monitor.start()
                self.logger.info("✅ Database monitoring started")
            
            # Start recovery engine
            if self.recovery_engine:
                self.recovery_engine.start()
                self.logger.info("✅ Recovery engine started")
            
            # Integrate with Flask
            if self.flask_integration:
                self.flask_integration.integrate()
                self.logger.info("✅ Flask integration completed")
            
            # Start Web UI
            if self.config.enable_web_ui:
                self._start_web_ui()
            
            # Start main monitoring thread
            self._running = True
            self._monitor_thread = threading.Thread(
                target=self._monitoring_loop,
                daemon=True,
                name="RecoveryAgentMonitor"
            )
            self._monitor_thread.start()
            
            self.logger.info("🎉 Autonomous Recovery Agent started successfully!")
            self.logger.info(f"📊 Web Dashboard: http://{self.config.web_ui_host}:{self.config.web_ui_port}")
            self.logger.info(f"🩺 Health endpoint: /health")
            self.logger.info(f"⚙️  Recovery API: {self.config.api_prefix}")
            
            # Register shutdown handler
            import atexit
            atexit.register(self.stop)
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start agent: {e}")
            raise
    
    def stop(self):
        """Stop the autonomous recovery agent"""
        if not self._running:
            return
        
        self.logger.info("🛑 Stopping Autonomous Recovery Agent...")
        self._running = False
        
        # Stop all components
        if self.service_monitor:
            self.service_monitor.stop()
        
        if self.database_monitor:
            self.database_monitor.stop()
        
        if self.recovery_engine:
            self.recovery_engine.stop()
        
        self.logger.info("✅ Autonomous Recovery Agent stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self._running:
            try:
                # Check service health
                if self.service_monitor:
                    service_health = self.service_monitor.check_health()
                    if service_health and service_health.get("status") in ["unhealthy", "critical"]:
                        self._handle_service_unhealthy(service_health)
                
                # Check database health
                if self.database_monitor:
                    db_health = self.database_monitor.check_health()
                    if db_health and db_health.get("status") in ["disconnected", "error"]:
                        self._handle_database_unhealthy(db_health)
                
                # Sleep until next check
                time.sleep(self.config.check_interval)
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(5)
    
    def _handle_service_unhealthy(self, health_data: Dict[str, Any]):
        """Handle unhealthy service"""
        self.logger.warning(f"⚠️ Service unhealthy: {health_data.get('error_message')}")
        
        # Call custom callback
        if self.config.on_service_unhealthy:
            try:
                self.config.on_service_unhealthy(health_data)
            except Exception as e:
                self.logger.error(f"Error in service unhealthy callback: {e}")
        
        # Trigger automatic recovery
        if self.config.auto_recovery and self.recovery_engine:
            result = self.recovery_engine.recover_service(
                service_type="flask",
                health_data=health_data
            )
            
            # Call recovery completed callback
            if self.config.on_recovery_completed:
                try:
                    self.config.on_recovery_completed(result)
                except Exception as e:
                    self.logger.error(f"Error in recovery completed callback: {e}")
    
    def _handle_database_unhealthy(self, health_data: Dict[str, Any]):
        """Handle unhealthy database"""
        self.logger.warning(f"⚠️ Database unhealthy: {health_data.get('error_message')}")
        
        # Call custom callback
        if self.config.on_database_unhealthy:
            try:
                self.config.on_database_unhealthy(health_data)
            except Exception as e:
                self.logger.error(f"Error in database unhealthy callback: {e}")
        
        # Trigger automatic recovery
        if self.config.auto_recovery and self.recovery_engine:
            result = self.recovery_engine.recover_database(
                db_type="mongodb",
                health_data=health_data
            )
            
            # Call recovery completed callback
            if self.config.on_recovery_completed:
                try:
                    self.config.on_recovery_completed(result)
                except Exception as e:
                    self.logger.error(f"Error in recovery completed callback: {e}")
    
    def _start_web_ui(self):
        """Start Web UI in a separate thread"""
        try:
            from .web_ui import start_web_ui
            self._web_ui_thread = threading.Thread(
                target=start_web_ui,
                args=(self.config.web_ui_host, self.config.web_ui_port, self),
                daemon=True,
                name="RecoveryAgentWebUI"
            )
            self._web_ui_thread.start()
            self.logger.info(f"🌐 Web UI started on http://{self.config.web_ui_host}:{self.config.web_ui_port}")
        except Exception as e:
            self.logger.error(f"Failed to start Web UI: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        status = {
            "running": self._running,
            "service_monitoring": self.service_monitor is not None,
            "database_monitoring": self.database_monitor is not None,
            "auto_recovery": self.recovery_engine is not None,
            "web_ui_enabled": self.config.enable_web_ui
        }
        
        # Add service health
        if self.service_monitor:
            status["service_health"] = self.service_monitor.check_health()
        
        # Add database health
        if self.database_monitor:
            status["database_health"] = self.database_monitor.check_health()
        
        return status
    
    def trigger_recovery(self, component: str, reason: str = "Manual trigger") -> Dict[str, Any]:
        """Manually trigger recovery for a component"""
        if component == "service" and self.recovery_engine:
            return self.recovery_engine.recover_service("flask", {"reason": reason})
        elif component == "database" and self.recovery_engine:
            return self.recovery_engine.recover_database("mongodb", {"reason": reason})
        else:
            return {"success": False, "error": f"Unknown component: {component}"}