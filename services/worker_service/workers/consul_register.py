import os
import requests
import socket
import logging
from threading import Timer

logger = logging.getLogger(__name__)

def get_ip():
    # Simple way to get the current machine's IP (for local dev)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def register_with_consul():
    consul_host = os.getenv("CONSUL_HOST", "localhost")
    consul_port = os.getenv("CONSUL_PORT", "8500")
    service_name = os.getenv("SERVICE_NAME", "worker-service")
    service_port = int(os.getenv("SERVICE_PORT", "8001"))
    
    url = f"http://{consul_host}:{consul_port}/v1/agent/service/register"
    
    payload = {
        "Name": service_name,
        "Port": service_port,
        "Address": get_ip(),
        "Check": {
            # Minimal health check for demo purposes
            "HTTP": f"http://{get_ip()}:{service_port}/mock/auth/me/",
            "Interval": "10s",
            "Timeout": "2s"
        }
    }

    try:
        response = requests.put(url, json=payload, timeout=5)
        if response.status_code == 200:
            logger.info(f"Successfully registered {service_name} with Consul at {consul_host}:{consul_port}")
        else:
            logger.error(f"Failed to register with Consul: {response.text}")
    except Exception as e:
        logger.error(f"Error registering with Consul: {e}")

def start_registration():
    # Delay registration slightly to ensure server is up
    t = Timer(5.0, register_with_consul)
    t.daemon = True
    t.start()
