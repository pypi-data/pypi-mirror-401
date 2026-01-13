from __future__ import annotations

from pathlib import Path
from typing import Any, BinaryIO, Optional, Union

import httpx

from ..errors import ApiError, AuthenticationError, RateLimitError
from ..types import UploadResult


class StorageResource:
    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def upload(
        self,
        file: Union[str, Path, BinaryIO],
        *,
        filename: Optional[str] = None,
        folder_ulid: Optional[str] = None,
    ) -> UploadResult:
        if isinstance(file, (str, Path)):
            path = Path(file)
            with path.open("rb") as handle:
                return self._do_upload(handle, filename or path.name, folder_ulid)
        return self._do_upload(file, filename or "upload.bin", folder_ulid)

    def resolve_path(self, path: str) -> Optional[UploadResult]:
        res = self._client.get("storage/resolve/", params={"path": path})
        if res.status_code == 404:
            return None
        data = self._json(res)
        return UploadResult(
            obj_ulid=str(data.get("obj_ulid", "")),
            uri=str(data.get("uri", "")),
            filename=str(data.get("filename", "")),
            size_bytes=int(data.get("size_bytes") or 0),
        )

    def _do_upload(
        self, handle: BinaryIO, filename: str, folder_ulid: Optional[str]
    ) -> UploadResult:
        files = {"file": (filename, handle)}
        data = {"folder_ulid": folder_ulid} if folder_ulid else {}
        res = self._client.post("storage/upload/", files=files, data=data)
        payload = self._json(res)
        return UploadResult(
            obj_ulid=str(payload.get("obj_ulid", "")),
            uri=str(payload.get("uri", "")),
            filename=str(payload.get("filename", "")),
            size_bytes=int(payload.get("size_bytes") or 0),
        )

    def _json(self, res: httpx.Response) -> dict[str, Any]:
        if res.status_code in (401, 403):
            raise AuthenticationError(
                status_code=res.status_code,
                body=_safe_json(res),
                message="Unauthorized",
            )
        if res.status_code == 429:
            err = RateLimitError(
                status_code=429, body=_safe_json(res), message="Rate limited"
            )
            err.retry_after = res.headers.get("Retry-After")
            raise err
        if res.status_code < 200 or res.status_code >= 300:
            raise ApiError(status_code=res.status_code, body=_safe_json(res))

        data = _safe_json(res)
        return data if isinstance(data, dict) else {"data": data}


def _safe_json(res: httpx.Response) -> Any:
    try:
        return res.json()
    except Exception:
        return res.text
