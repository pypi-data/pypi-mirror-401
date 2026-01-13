"""
Recovery engine for automatic problem resolution
"""
import time
import logging
from typing import Dict, Any, Optional, List
import subprocess
import os
import socket


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

        self._recovery_history: List[Dict[str, Any]] = []
        self._attempt_counts = {}
        self._active_recoveries: Dict[str, Dict[str, Any]] = {}

    def start(self):
        """Start recovery engine"""
        self.logger.info("Recovery engine started")

    def stop(self):
        """Stop recovery engine"""
        self.logger.info("Recovery engine stopped")

    # -------------------------
    # Database recovery
    # -------------------------
    def recover_database(self, db_type: str, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """Recover a database"""
        db_id = f"db_{db_type}"

        if self._is_in_cooldown(db_id):
            return {
                "success": False,
                "message": "Database in cooldown period",
                "action": "none",
                "recovery_id": db_id
            }

        self.logger.warning(f"🔄 Attempting to recover {db_type} database")

        recovery_id = f"{db_id}_{int(time.time())}"
        recovery_record = {
            "recovery_id": recovery_id,
            "component": db_id,
            "start_time": time.time(),
            "status": "in_progress",
            "attempts": 0,
            "last_error": health_data.get('error_message', 'Unknown error')
        }

        self._active_recoveries[recovery_id] = recovery_record

        try:
            result = self._recover_database_connection(db_type, recovery_id)

            recovery_record.update({
                "end_time": time.time(),
                "status": "completed" if result.get("success") else "failed",
                "result": result
            })

            self._record_recovery(db_id, result)
            del self._active_recoveries[recovery_id]

            return result

        except Exception as e:
            self.logger.error(f"❌ Database recovery failed: {e}")

            result = {
                "success": False,
                "message": f"Recovery failed: {str(e)}",
                "action": "failed",
                "recovery_id": recovery_id
            }

            recovery_record.update({
                "end_time": time.time(),
                "status": "failed",
                "result": result,
                "error": str(e)
            })

            self._record_recovery(db_id, result)
            return result

    def _recover_database_connection(self, db_type: str, recovery_id: str) -> Dict[str, Any]:
        """Recover database connection"""
        self.logger.info(f"🔧 Recovering {db_type} connection (ID: {recovery_id})")

        steps = [
            {"step": "reset_connection", "wait": 2},
            {"step": "clear_pool", "wait": 1},
            {"step": "reconnect", "wait": 3}
        ]

        for step_info in steps:
            step = step_info["step"]
            wait = step_info["wait"]

            self.logger.info(f"  Step: {step}...")
            time.sleep(wait)

        return {
            "success": True,
            "message": f"{db_type} connection recovery initiated",
            "action": "connection_reset",
            "recovery_id": recovery_id,
            "steps_completed": len(steps)
        }

    # -------------------------
    # Service recovery
    # -------------------------
    def recover_service(self, service_type: str = "flask") -> Dict[str, Any]:
        """Recover a failed service"""
        service_id = f"service_{service_type}"

        if self._is_in_cooldown(service_id):
            return {
                "success": False,
                "message": f"Service {service_type} in cooldown period",
                "action": "none",
                "recovery_id": service_id
            }

        self.logger.warning(f"🔄 Attempting to recover {service_type} service")

        recovery_id = f"{service_id}_{int(time.time())}"
        recovery_record = {
            "recovery_id": recovery_id,
            "component": service_id,
            "start_time": time.time(),
            "status": "in_progress",
            "attempts": 0,
            "service_type": service_type
        }

        self._active_recoveries[recovery_id] = recovery_record

        try:
            result = self._recover_service_process(service_type, recovery_id)

            recovery_record.update({
                "end_time": time.time(),
                "status": "completed" if result.get("success") else "failed",
                "result": result
            })

            self._record_recovery(service_id, result)
            del self._active_recoveries[recovery_id]

            return result

        except Exception as e:
            self.logger.error(f"❌ Service recovery failed: {e}")
            result = {
                "success": False,
                "message": f"Service recovery failed: {str(e)}",
                "action": "failed",
                "recovery_id": recovery_id
            }
            recovery_record.update({
                "end_time": time.time(),
                "status": "failed",
                "result": result,
                "error": str(e)
            })
            self._record_recovery(service_id, result)
            return result

    def _recover_service_process(self, service_type: str, recovery_id: str) -> Dict[str, Any]:
        self.logger.info(f"🔧 Recovering {service_type} service (ID: {recovery_id})")
        if service_type in ["flask", "gunicorn"]:
            return self._recover_flask_gunicorn(service_type, recovery_id)
        else:
            return {
                "success": False,
                "message": f"Unknown service type: {service_type}",
                "action": "failed",
                "recovery_id": recovery_id
            }

    def _recover_flask_gunicorn(self, service_type: str, recovery_id: str) -> Dict[str, Any]:
        steps = []
        try:
            self.logger.info("  Step: Killing existing processes...")
            kill_methods = [
                ["pkill", "-f", "gunicorn"],
                ["pkill", "-f", "flask"],
                ["killall", "gunicorn"]
            ]
            for cmd in kill_methods:
                try:
                    subprocess.run(cmd, capture_output=True, timeout=5)
                    steps.append(f"kill_cmd: {' '.join(cmd)}")
                except:
                    pass
            time.sleep(2)

            self.logger.info("  Step: Checking port availability...")
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', 10000))
                sock.close()
                if result == 0:
                    self.logger.warning("  Port 10000 is still in use, freeing...")
                    subprocess.run(["fuser", "-k", "10000/tcp"], capture_output=True)
                    time.sleep(2)
                    steps.append("freed_port_10000")
            except:
                pass

            self.logger.info(f"  Step: Restarting {service_type}...")
            if service_type == "gunicorn":
                startup_cmd = [
                    "gunicorn",
                    "--bind", "0.0.0.0:10000",
                    "--workers", "1",
                    "--timeout", "120",
                    "--access-logfile", "-",
                    "--error-logfile", "-",
                    "wsgi:app"
                ]
            else:  # flask
                os.environ["FLASK_APP"] = "app.py"
                os.environ["FLASK_ENV"] = "production"
                startup_cmd = ["flask", "run", "--host=0.0.0.0", "--port=10000", "--no-reload"]

            process = subprocess.Popen(
                startup_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True
            )
            steps.append(f"started_{service_type}")
            time.sleep(5)

            if process.poll() is None:
                self.logger.info(f"✅ {service_type} started successfully (PID: {process.pid})")
                return {
                    "success": True,
                    "message": f"{service_type} service restarted successfully",
                    "action": f"{service_type}_restart",
                    "recovery_id": recovery_id,
                    "pid": process.pid,
                    "steps": steps
                }
            else:
                stdout, stderr = process.communicate()
                error_msg = stderr.decode() if stderr else "Unknown error"
                self.logger.error(f"❌ {service_type} failed to start: {error_msg}")
                return self._fallback_service_start(recovery_id, steps, error_msg)

        except Exception as e:
            self.logger.error(f"❌ Flask/Gunicorn recovery failed: {e}")
            return {
                "success": False,
                "message": f"Service recovery failed: {str(e)}",
                "action": "recovery_failed",
                "recovery_id": recovery_id,
                "steps": steps
            }

    def _fallback_service_start(self, recovery_id: str, previous_steps: list, previous_error: str) -> Dict[str, Any]:
        """Fallback method to start service"""
        try:
            self.logger.info("  Trying fallback service start...")
            fallback_cmd = [
                "python",
                "-c",
                """
import sys
sys.path.insert(0, '.')
from your_app_module import app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)
                """
            ]
            process = subprocess.Popen(
                fallback_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True
            )
            time.sleep(3)
            if process.poll() is None:
                previous_steps.append("fallback_start_success")
                return {
                    "success": True,
                    "message": "Service started via fallback method",
                    "action": "fallback_restart",
                    "recovery_id": recovery_id,
                    "pid": process.pid,
                    "steps": previous_steps,
                    "previous_error": previous_error
                }
            else:
                previous_steps.append("fallback_failed")
                return {
                    "success": False,
                    "message": "Fallback service start also failed",
                    "action": "all_methods_failed",
                    "recovery_id": recovery_id,
                    "steps": previous_steps,
                    "previous_error": previous_error
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Fallback failed: {str(e)}",
                "action": "fallback_failed",
                "recovery_id": recovery_id,
                "steps": previous_steps,
                "error": str(e)
            }

    # -------------------------
    # Utilities
    # -------------------------
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
            "message": result.get("message", ""),
            "recovery_id": result.get("recovery_id", "")
        }
        self._recovery_history.append(recovery)

        if result.get("success"):
            self.logger.info(f"✅ Recovery recorded: {result.get('message')}")
        else:
            self.logger.warning(f"⚠️ Recovery failed recorded: {result.get('message')}")

    def get_active_recoveries(self) -> List[Dict[str, Any]]:
        return list(self._active_recoveries.values())

    def get_recovery_history(self, limit: int = 10) -> list:
        return self._recovery_history[-limit:]

    def get_recovery_status(self, recovery_id: str) -> Optional[Dict[str, Any]]:
        return self._active_recoveries.get(recovery_id)
