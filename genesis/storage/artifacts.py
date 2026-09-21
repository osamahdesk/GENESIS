from __future__ import annotations

import hashlib
from pathlib import Path

from genesis.core import ArtifactKind, ArtifactRef


class ArtifactStore:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def put_text(self, artifact_id: str, filename: str, content: str, kind: ArtifactKind, producer: str) -> ArtifactRef:
        path = self.root / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        return ArtifactRef(artifact_id, str(path), kind, digest, producer)
