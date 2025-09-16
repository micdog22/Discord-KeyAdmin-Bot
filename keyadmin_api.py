import os
import httpx
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

# Ajuste estes caminhos se seu painel usar rotas diferentes
ENDPOINTS = {
    "create": "/criar_key.php",
    "status": "/status.php",
    "ban": "/banir_key.php",
    "unban": "/desbanir_key.php",
    "reset_hwid": "/reset_hwid.php",
    "delete": "/deletar_key.php",
}

def _join(base: str, path: str) -> str:
    return base.rstrip("/") + path

@dataclass
class KeyAdminConfig:
    base_url: str
    cliente_hash: str
    api_key: str
    software_id: str

    @classmethod
    def from_env(cls) -> "KeyAdminConfig":
        return cls(
            base_url=os.getenv("KEYADMIN_BASE_URL", "").strip(),
            cliente_hash=os.getenv("KEYADMIN_CLIENTE_HASH", "").strip(),
            api_key=os.getenv("KEYADMIN_API_KEY", "").strip(),
            software_id=os.getenv("KEYADMIN_SOFTWARE_ID", "").strip(),
        )

class KeyAdminAPI:
    def __init__(self, cfg: KeyAdminConfig | None = None):
        self.cfg = cfg or KeyAdminConfig.from_env()
        if not self.cfg.base_url:
            raise RuntimeError("KEYADMIN_BASE_URL não definido")

    async def _post(self, path: str, payload: dict) -> dict:
        url = _join(self.cfg.base_url, path)
        body = {
            **payload,
            "cliente_hash": self.cfg.cliente_hash,
            "api_key": self.cfg.api_key,
            "software_id": self.cfg.software_id,
        }
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(url, json=body)
            r.raise_for_status()
            try:
                return r.json()
            except Exception:
                return {"raw": r.text, "status_code": r.status_code}

    async def create_keys(self, validade: str, qtd: int, prefixo: str = "", sufixo: str = "", tamanho: int = 20) -> dict:
        return await self._post(ENDPOINTS["create"], {
            "validade": validade,
            "qtd": qtd,
            "prefixo": prefixo,
            "sufixo": sufixo,
            "tamanho": tamanho
        })

    async def status_key(self, key: str) -> dict:
        return await self._post(ENDPOINTS["status"], {"key": key})

    async def ban_key(self, key: str, motivo: str | None = None) -> dict:
        data = {"key": key}
        if motivo:
            data["motivo"] = motivo
        return await self._post(ENDPOINTS["ban"], data)

    async def unban_key(self, key: str) -> dict:
        return await self._post(ENDPOINTS["unban"], {"key": key})

    async def reset_hwid(self, key: str) -> dict:
        return await self._post(ENDPOINTS["reset_hwid"], {"key": key})

    async def delete_key(self, key: str) -> dict:
        return await self._post(ENDPOINTS["delete"], {"key": key})