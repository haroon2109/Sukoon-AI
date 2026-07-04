from fastapi import Request
from slowapi import Limiter

def get_client_ip(request: Request) -> str:
    """
    Safely retrieves the real client IP address, respecting standard proxy headers
    (like X-Forwarded-For and X-Real-IP) and falling back to direct socket client host.
    """
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        parts = [ip.strip() for ip in x_forwarded_for.split(",")]
        if parts and parts[0]:
            return parts[0]
            
    x_real_ip = request.headers.get("x-real-ip")
    if x_real_ip:
        return x_real_ip
        
    if request.client:
        return request.client.host
        
    return "127.0.0.1"

# Global Rate Limiter using proxy-aware IP derivation
limiter = Limiter(key_func=get_client_ip)
