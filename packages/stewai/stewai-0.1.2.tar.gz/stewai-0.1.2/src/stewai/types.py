from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional


@dataclass(frozen=True)
class IngestSource:
    uri: str
    kind: Literal["url", "file"] = "url"
    label: Optional[str] = None

    def to_dict(self) -> dict:
        data = {"uri": self.uri, "kind": self.kind}
        if self.label:
            data["label"] = self.label
        return data


@dataclass(frozen=True)
class UploadResult:
    obj_ulid: str
    uri: str
    filename: str
    size_bytes: int

    def to_ingest_source(self, label: Optional[str] = None) -> IngestSource:
        return IngestSource(uri=self.uri, kind="file", label=label)
