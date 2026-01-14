"""
轻量级 GCP Access Token 生成器
"""

import base64
import json
import os
import subprocess
import time
from pathlib import Path

import httpx

TOKEN_URI = "https://oauth2.googleapis.com/token"


def get_token_from_adc(
    credentials: dict | None = None,
    proxy: str | None = None,
) -> str:
    """
    从 Application Default Credentials 获取 access token

    Args:
        credentials: 凭证字典，可以是:
            - 用户凭证 (包含 refresh_token, client_id, client_secret)
            - 服务账号 (包含 private_key, client_email)
            - None: 自动从文件读取
        proxy: HTTP 代理地址，如 "http://127.0.0.1:7890"

    Returns:
        access_token 字符串
    """
    client_kwargs = {"proxy": proxy} if proxy else {}

    # 如果传入了凭证字典
    if credentials is not None:
        if "refresh_token" in credentials:
            return _refresh_user_token(credentials, client_kwargs)
        elif "private_key" in credentials:
            return _get_token_from_service_account_dict(credentials, client_kwargs)
        else:
            raise ValueError("无效的凭证格式")

    # 优先检查 ADC 文件 (gcloud auth application-default login)
    adc_path = Path.home() / ".config" / "gcloud" / "application_default_credentials.json"

    if adc_path.exists():
        with open(adc_path) as f:
            adc = json.load(f)

        if "refresh_token" in adc:
            return _refresh_user_token(adc, client_kwargs)

    # 检查服务账号
    sa_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if sa_path and Path(sa_path).exists():
        with open(sa_path) as f:
            sa = json.load(f)
        return _get_token_from_service_account_dict(sa, client_kwargs)

    raise RuntimeError("未找到凭证，请先运行: gcloud auth application-default login")


def _refresh_user_token(creds: dict, client_kwargs: dict) -> str:
    """用 refresh_token 换 access_token"""
    token_uri = creds.get("token_uri", TOKEN_URI)
    with httpx.Client(**client_kwargs) as client:
        resp = client.post(
            token_uri,
            data={
                "client_id": creds["client_id"],
                "client_secret": creds["client_secret"],
                "refresh_token": creds["refresh_token"],
                "grant_type": "refresh_token",
            },
        )
        resp.raise_for_status()
        return resp.json()["access_token"]


def _get_token_from_service_account_dict(sa: dict, client_kwargs: dict) -> str:
    """从服务账号字典获取 token (需要 cryptography 库)"""
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

    token_uri = sa.get("token_uri", TOKEN_URI)

    now = int(time.time())
    header = {"alg": "RS256", "typ": "JWT"}
    payload = {
        "iss": sa["client_email"],
        "sub": sa["client_email"],
        "aud": token_uri,
        "iat": now,
        "exp": now + 3600,
        "scope": "https://www.googleapis.com/auth/cloud-platform",
    }

    def b64(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

    h = b64(json.dumps(header).encode())
    p = b64(json.dumps(payload).encode())
    msg = f"{h}.{p}".encode()

    key = serialization.load_pem_private_key(sa["private_key"].encode(), None)
    if not isinstance(key, RSAPrivateKey):
        raise TypeError("服务账号私钥必须是 RSA 密钥")
    sig = key.sign(msg, padding.PKCS1v15(), hashes.SHA256())

    jwt = f"{h}.{p}.{b64(sig)}"

    with httpx.Client(**client_kwargs) as client:
        resp = client.post(
            token_uri,
            data={
                "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                "assertion": jwt,
            },
        )
        resp.raise_for_status()
        return resp.json()["access_token"]


def get_token_from_gcloud() -> str:
    """直接从 gcloud CLI 获取 token"""
    result = subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()
