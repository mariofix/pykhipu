from typing import Optional


class _ClientOptions:
    client_id: Optional[str] = None
    proxy: Optional[str] = None
    verify_ssl_certs: Optional[bool] = None
