"""
Flask integration for Autonomous Recovery Agent
"""
from flask import Blueprint, jsonify, request
import logging
from typing import Optional


class FlaskIntegration:
    """Integrate autonomous recovery with Flask application"""
    
    def __init__(
        self,
        flask_app,
        agent,
        api_prefix: str = "/recovery",
        enable_api: bool = True,
        logger: Optional[logging.Logger] = None
    ):
        self.app = flask_app
        self.agent = agent
        self.api_prefix = api_prefix
        self.enable_api = enable_api
        self.logger = logger or logging.getLogger(__name__)
    
    def integrate(self):
        """Integrate with Flask application"""
        
        # Add health check endpoint
        @self.app.route('/health')
        def health_check():
            """Health check endpoint"""
            status = {
                "status": "healthy",
                "service": "flask",
                "recovery_agent": "active" if self.agent._running else "inactive"
            }
            
            # Add agent status if available
            try:
                agent_status = self.agent.get_status()
                status["agent_status"] = agent_status
            except Exception as e:
                status["agent_status_error"] = str(e)
            
            return jsonify(status)
        
        # Add recovery API endpoints if enabled
        if self.enable_api:
            self._add_recovery_api()
        
        # Patch database connections for automatic recovery
        self._patch_database_connections()
        
        self.logger.info("Flask integration completed")
    
    def _add_recovery_api(self):
        """Add recovery API endpoints to Flask"""
        
        recovery_bp = Blueprint('recovery', __name__, url_prefix=self.api_prefix)
        
        @recovery_bp.route('/status', methods=['GET'])
        def get_status():
            """Get recovery agent status"""
            try:
                status = self.agent.get_status()
                return jsonify({
                    "status": "ok",
                    "agent": status
                })
            except Exception as e:
                return jsonify({
                    "status": "error",
                    "error": str(e)
                }), 500
        
        @recovery_bp.route('/trigger', methods=['POST'])
        def trigger_recovery():
            """Manually trigger recovery"""
            data = request.get_json() or {}
            component = data.get('component', 'service')
            reason = data.get('reason', 'Manual trigger')
            
            try:
                result = self.agent.trigger_recovery(component, reason)
                return jsonify({
                    "status": "ok" if result.get('success') else "error",
                    "result": result
                })
            except Exception as e:
                return jsonify({
                    "status": "error",
                    "error": str(e)
                }), 500
        
        @recovery_bp.route('/health', methods=['GET'])
        def recovery_health():
            """Get detailed health information"""
            try:
                status = {
                    "service": self.agent.service_monitor.check_health() if self.agent.service_monitor else None,
                    "database": self.agent.database_monitor.check_health() if self.agent.database_monitor else None
                }
                return jsonify({
                    "status": "ok",
                    "health": status
                })
            except Exception as e:
                return jsonify({
                    "status": "error",
                    "error": str(e)
                }), 500
        
        # Register blueprint
        self.app.register_blueprint(recovery_bp)
        self.logger.info(f"Recovery API endpoints registered at {self.api_prefix}")
    
    def _patch_database_connections(self):
        """Patch database connections to use recovery-aware clients"""
        try:
            # Check if pymongo is being used
            import pymongo
            from pymongo import MongoClient
            
            # Create a recovery-aware MongoClient wrapper
            class RecoveryAwareMongoClient(MongoClient):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self._recovery_agent = self.agent
                
                def _retry_on_failure(self, operation, *args, **kwargs):
                    """Retry operation on failure with recovery"""
                    max_retries = 3
                    
                    for attempt in range(max_retries):
                        try:
                            return operation(*args, **kwargs)
                        except Exception as e:
                            self.logger.warning(f"Database operation failed (attempt {attempt + 1}): {e}")
                            
                            # Trigger recovery if this is the first failure
                            if attempt == 0 and self.agent.recovery_engine:
                                self.agent.recovery_engine.recover_database(
                                    "mongodb",
                                    {"error": str(e), "operation": operation.__name__}
                                )
                            
                            # Wait before retry
                            import time
                            time.sleep(1)
                    
                    # All retries failed
                    raise Exception(f"Database operation failed after {max_retries} attempts")
            
            # Monkey-patch pymongo.MongoClient
            import pymongo
            original_mongo_client = pymongo.MongoClient
            
            def patched_mongo_client(*args, **kwargs):
                client = RecoveryAwareMongoClient(*args, **kwargs)
                client.agent = self.agent
                client.logger = self.logger
                return client
            
            pymongo.MongoClient = patched_mongo_client
            pymongo.mongo_client.MongoClient = patched_mongo_client
            
            self.logger.info("Database connections patched for automatic recovery")
            
        except ImportError:
            # pymongo not installed, skip patching
            pass
        except Exception as e:
            self.logger.error(f"Failed to patch database connections: {e}")