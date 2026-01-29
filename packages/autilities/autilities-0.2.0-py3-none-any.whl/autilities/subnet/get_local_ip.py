from socket import socket, AF_INET, SOCK_DGRAM
from asyncio import run
from parlancy import IpAddress





async def get_local_ip() -> IpAddress:
    """Obtain the local IP Address"""
    soc = socket(AF_INET, SOCK_DGRAM)
    try:
        soc.connect(('10.254.254.254', 1))
        ip = soc.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        soc.close()
    return ip


def get_local_ip_sync() -> IpAddress:
    result = run(get_local_ip())
    return result
