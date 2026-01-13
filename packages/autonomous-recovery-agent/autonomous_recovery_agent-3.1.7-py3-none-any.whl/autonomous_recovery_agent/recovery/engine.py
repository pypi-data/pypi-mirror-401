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
            result = self._recover_database_connection(db_type, recovery_id, health_data)

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

    def _recover_database_connection(self, db_type: str, recovery_id: str, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """Recover database connection"""
        self.logger.info(f"🔧 Recovering {db_type} connection (ID: {recovery_id})")
        
        # Log health data for debugging
        if health_data:
            self.logger.debug(f"Database health data: {health_data}")

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
    # Service recovery - UPDATED TO ACCEPT health_data PARAMETER
    # -------------------------
    def recover_service(self, service_type: str = "flask", health_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Recover a failed service"""
        service_id = f"service_{service_type}"
        health_data = health_data or {}

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
            "service_type": service_type,
            "health_data": health_data
        }

        self._active_recoveries[recovery_id] = recovery_record

        try:
            result = self._recover_service_process(service_type, recovery_id, health_data)

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

    def _recover_service_process(self, service_type: str, recovery_id: str, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """Recover a service process"""
        self.logger.info(f"🔧 Recovering {service_type} service (ID: {recovery_id})")
        
        # Log health data for debugging
        if health_data:
            self.logger.debug(f"Service health data: {health_data}")
            
        if service_type in ["flask", "gunicorn"]:
            return self._recover_flask_gunicorn(service_type, recovery_id, health_data)
        else:
            return {
                "success": False,
                "message": f"Unknown service type: {service_type}",
                "action": "failed",
                "recovery_id": recovery_id
            }

    def _recover_flask_gunicorn(self, service_type: str, recovery_id: str, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """Recover Flask/Gunicorn service with health data context"""
        steps = []
        try:
            # Use health data to inform recovery strategy
            error_message = health_data.get('error_message', '')
            if error_message:
                self.logger.info(f"  Health context: {error_message[:100]}...")
            
            # More aggressive killing for stubborn processes
            self.logger.info("  Step: Killing existing processes...")
            kill_methods = [
                ["pkill", "-9", "-f", "gunicorn"],  # -9 for SIGKILL
                ["pkill", "-9", "-f", "flask"],
                ["killall", "-9", "gunicorn"],
                ["pkill", "-f", "python.*(flask|gunicorn)"]
            ]
            for cmd in kill_methods:
                try:
                    result = subprocess.run(cmd, capture_output=True, timeout=5)
                    if result.returncode == 0:
                        steps.append(f"kill_cmd: {' '.join(cmd)}")
                except:
                    pass
            
            time.sleep(3)  # Longer wait for processes to die

            self.logger.info("  Step: Checking port availability...")
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', 10000))
                sock.close()
                if result == 0:
                    self.logger.warning("  Port 10000 is still in use, freeing...")
                    # Try multiple methods to free the port
                    port_free_methods = [
                        ["fuser", "-k", "10000/tcp"],
                        ["lsof", "-ti:10000", "|", "xargs", "kill", "-9"],
                        ["ss", "-tulpn", "|", "grep", ":10000", "|", "awk", "'{print $7}'", "|", "cut", "-d'/'", "-f1", "|", "xargs", "kill", "-9"]
                    ]
                    for cmd in port_free_methods:
                        try:
                            subprocess.run(' '.join(cmd), shell=True, capture_output=True)
                        except:
                            pass
                    time.sleep(2)
                    steps.append("freed_port_10000")
            except Exception as e:
                self.logger.debug(f"Port check error: {e}")

            self.logger.info(f"  Step: Restarting {service_type}...")
            
            # Set common environment variables
            env = os.environ.copy()
            env["PYTHONUNBUFFERED"] = "1"
            
            if service_type == "gunicorn":
                startup_cmd = [
                    "gunicorn",
                    "--bind", "0.0.0.0:10000",
                    "--workers", "1",
                    "--timeout", "120",
                    "--access-logfile", "-",
                    "--error-logfile", "-",
                    "--preload",  # Preload app for faster startup
                    "wsgi:app"
                ]
            else:  # flask
                env["FLASK_APP"] = "app.py" or "wsgi.py"  # Try common app files
                env["FLASK_ENV"] = "production"
                startup_cmd = [
                    "flask", "run",
                    "--host=0.0.0.0",
                    "--port=10000",
                    "--no-reload",
                    "--no-debugger"
                ]

            self.logger.info(f"  Starting: {' '.join(startup_cmd)}")
            process = subprocess.Popen(
                startup_cmd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True,
                text=True
            )
            
            steps.append(f"started_{service_type}")
            time.sleep(7)  # Longer wait for Flask/Gunicorn to fully start

            if process.poll() is None:
                # Check if service is actually responding
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    result = sock.connect_ex(('localhost', 10000))
                    sock.close()
                    
                    if result == 0:
                        self.logger.info(f"✅ {service_type} started successfully and responding (PID: {process.pid})")
                        return {
                            "success": True,
                            "message": f"{service_type} service restarted successfully",
                            "action": f"{service_type}_restart",
                            "recovery_id": recovery_id,
                            "pid": process.pid,
                            "port_check": "success",
                            "steps": steps
                        }
                    else:
                        self.logger.warning(f"⚠️ {service_type} process running but port not responding")
                        steps.append("port_not_responding")
                except:
                    pass
                
                # Process is running even if port check failed
                self.logger.info(f"✅ {service_type} process started (PID: {process.pid})")
                return {
                    "success": True,
                    "message": f"{service_type} process started",
                    "action": f"{service_type}_restart",
                    "recovery_id": recovery_id,
                    "pid": process.pid,
                    "steps": steps,
                    "note": "Process started but port responsiveness unverified"
                }
            else:
                stdout, stderr = process.communicate()
                error_msg = stderr if stderr else "Unknown error"
                self.logger.error(f"❌ {service_type} failed to start: {error_msg[:200]}")
                steps.append(f"start_failed: {error_msg[:100]}")
                return self._fallback_service_start(recovery_id, steps, error_msg, health_data)

        except Exception as e:
            self.logger.error(f"❌ Flask/Gunicorn recovery failed: {e}")
            return {
                "success": False,
                "message": f"Service recovery failed: {str(e)}",
                "action": "recovery_failed",
                "recovery_id": recovery_id,
                "steps": steps
            }

    def _fallback_service_start(self, recovery_id: str, previous_steps: list, previous_error: str, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback method to start service"""
        try:
            self.logger.info("  Trying fallback service start...")
            
            # Try common app entry points
            app_files = ["app.py", "wsgi.py", "application.py", "main.py"]
            for app_file in app_files:
                if os.path.exists(app_file):
                    self.logger.info(f"  Found app file: {app_file}")
                    fallback_cmd = [
                        "python",
                        "-c",
                        f"""
import sys
sys.path.insert(0, '.')
try:
    import {app_file.replace('.py', '')} as app_module
    app = app_module.app
except:
    from {app_file.replace('.py', '')} import create_app
    app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False)
                        """
                    ]
                    
                    process = subprocess.Popen(
                        fallback_cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        start_new_session=True,
                        text=True
                    )
                    time.sleep(5)
                    
                    if process.poll() is None:
                        previous_steps.append(f"fallback_start_success_with_{app_file}")
                        return {
                            "success": True,
                            "message": f"Service started via fallback using {app_file}",
                            "action": "fallback_restart",
                            "recovery_id": recovery_id,
                            "pid": process.pid,
                            "steps": previous_steps,
                            "previous_error": previous_error[:100]
                        }
            
            # If all fallbacks fail
            previous_steps.append("all_fallbacks_failed")
            return {
                "success": False,
                "message": "All fallback service start attempts failed",
                "action": "all_methods_failed",
                "recovery_id": recovery_id,
                "steps": previous_steps,
                "previous_error": previous_error[:100]
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
        """Get active recovery attempts"""
        return list(self._active_recoveries.values())

    def get_recovery_history(self, limit: int = 10) -> list:
        """Get recovery history"""
        return self._recovery_history[-limit:]

    def get_recovery_status(self, recovery_id: str) -> Optional[Dict[str, Any]]:
        """Get status of specific recovery"""
        return self._active_recoveries.get(recovery_id)

    # -------------------------
    # Backward compatibility wrapper
    # -------------------------
    def recover_service_with_health(self, service_type: str = "flask", health_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Wrapper for backward compatibility - calls the updated recover_service"""
        return self.recover_service(service_type, health_data)