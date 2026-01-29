import asyncio
import socket
from typing import TypedDict
from parlancy import IpAddress


GetHostResult = TypedDict("GetHostResult", { 'ip': IpAddress, })



async def get_host() -> GetHostResult:
    """Get host machine's subnet IP address"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return {"ip": ip}


def get_host_sync() -> GetHostResult:
    """get the hostname of the machine synchronously - async is better"""
    return asyncio.run(get_host())
