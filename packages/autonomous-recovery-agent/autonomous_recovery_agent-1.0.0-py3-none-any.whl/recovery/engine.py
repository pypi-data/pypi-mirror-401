"""
Recovery engine for automatic problem resolution
"""
import time
import logging
from typing import Dict, Any, Optional


class RecoveryEngine:
    """Handle automatic recovery actions"""
    
    def __init__(
        self,
        max_attempts: int = 3,
        cooldown_seconds: int = 60,
        logger: Optional[logging.Logger] = None
    ):
        self.max_attempts = max_attempts
        self.cooldown_seconds = cooldown_seconds
        self.logger = logger or logging.getLogger(__name__)
        
        self._recovery_history = []
        self._attempt_counts = {}
    
    def start(self):
        """Start recovery engine"""
        self.logger.info("Recovery engine started")
    
    def stop(self):
        """Stop recovery engine"""
        self.logger.info("Recovery engine stopped")
    
    def recover_service(self, service_type: str, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """Recover a service"""
        service_id = f"service_{service_type}"
        
        # Check cooldown
        if self._is_in_cooldown(service_id):
            return {
                "success": False,
                "message": "Service in cooldown period",
                "action": "none"
            }
        
        # Check max attempts
        if self._attempt_counts.get(service_id, 0) >= self.max_attempts:
            return {
                "success": False,
                "message": "Max recovery attempts reached",
                "action": "none"
            }
        
        self.logger.warning(f"Attempting to recover {service_type} service")
        
        try:
            # Different recovery strategies based on error
            error_msg = health_data.get('error_message', '').lower()
            
            if 'memory' in error_msg:
                result = self._recover_memory_issue(service_type)
            else:
                result = self._restart_service(service_type)
            
            # Update attempt count
            self._attempt_counts[service_id] = self._attempt_counts.get(service_id, 0) + 1
            self._record_recovery(service_id, result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Service recovery failed: {e}")
            result = {
                "success": False,
                "message": f"Recovery failed: {str(e)}",
                "action": "failed"
            }
            self._record_recovery(service_id, result)
            return result
    
    def recover_database(self, db_type: str, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """Recover a database"""
        db_id = f"db_{db_type}"
        
        # Check cooldown
        if self._is_in_cooldown(db_id):
            return {
                "success": False,
                "message": "Database in cooldown period",
                "action": "none"
            }
        
        self.logger.warning(f"Attempting to recover {db_type} database")
        
        try:
            # Different recovery strategies
            error_msg = health_data.get('error_message', '').lower()
            
            if 'connection' in error_msg or 'disconnected' in health_data.get('status', ''):
                result = self._recover_database_connection(db_type)
            elif 'slow' in health_data.get('status', ''):
                result = self._optimize_database_performance(db_type)
            else:
                result = self._reset_database_connection(db_type)
            
            self._record_recovery(db_id, result)
            return result
            
        except Exception as e:
            self.logger.error(f"Database recovery failed: {e}")
            result = {
                "success": False,
                "message": f"Recovery failed: {str(e)}",
                "action": "failed"
            }
            self._record_recovery(db_id, result)
            return result
    
    def _recover_memory_issue(self, service_type: str) -> Dict[str, Any]:
        """Recover from memory issues"""
        self.logger.info(f"Recovering {service_type} from memory issues")
        # In production, you might:
        # 1. Clear caches
        # 2. Restart workers
        # 3. Increase memory limits
        
        return {
            "success": True,
            "message": "Memory recovery initiated",
            "action": "memory_cleanup"
        }
    
    def _restart_service(self, service_type: str) -> Dict[str, Any]:
        """Restart a service"""
        self.logger.info(f"Restarting {service_type} service")
        # In production, you would:
        # 1. Gracefully shutdown
        # 2. Wait for processes to stop
        # 3. Restart
        
        return {
            "success": True,
            "message": f"{service_type} service restart initiated",
            "action": "restart"
        }
    
    def _recover_database_connection(self, db_type: str) -> Dict[str, Any]:
        """Recover database connection"""
        self.logger.info(f"Recovering {db_type} connection")
        # In production, you would:
        # 1. Reset connection pool
        # 2. Switch to replica
        # 3. Enable read-only mode
        
        return {
            "success": True,
            "message": f"{db_type} connection recovery initiated",
            "action": "connection_reset"
        }
    
    def _reset_database_connection(self, db_type: str) -> Dict[str, Any]:
        """Reset database connection"""
        return {
            "success": True,
            "message": f"{db_type} connection reset",
            "action": "reset"
        }
    
    def _optimize_database_performance(self, db_type: str) -> Dict[str, Any]:
        """Optimize database performance"""
        return {
            "success": True,
            "message": f"{db_type} performance optimization initiated",
            "action": "optimize"
        }
    
    def _is_in_cooldown(self, component_id: str) -> bool:
        """Check if component is in cooldown period"""
        for recovery in reversed(self._recovery_history):
            if recovery.get('component_id') == component_id:
                recovery_time = recovery.get('timestamp', 0)
                if time.time() - recovery_time < self.cooldown_seconds:
                    return True
        return False
    
    def _record_recovery(self, component_id: str, result: Dict[str, Any]):
        """Record recovery attempt"""
        recovery = {
            "component_id": component_id,
            "timestamp": time.time(),
            "success": result.get("success", False),
            "action": result.get("action", "unknown"),
            "message": result.get("message", "")
        }
        self._recovery_history.append(recovery)
    
    def get_recovery_history(self, limit: int = 10) -> list:
        """Get recovery history"""
        return self._recovery_history[-limit:]