from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from pydantic import BaseModel, Field


class EvidenceRef(BaseModel):
    """Resolvable evidence reference.

    v0.3.0 supports deterministic SHA-256 verification of file-backed artifacts.
    """
    id: str
    type: str = Field(..., description="Evidence type. v0.3 supports: 'hash'")
    ref: str = Field(..., description="Resolvable reference. v0.3 supports file:// URIs")
    sha256: str = Field(..., description="Expected SHA-256 hex digest (64 chars)")
    attestor: Optional[str] = None


@dataclass
class EvidenceResult:
    id: str
    ok: bool
    message: str


@dataclass
class EvidenceReport:
    ok: bool
    results: List[EvidenceResult]
    verified_ids: Set[str]


def _compute_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _resolve_file_uri(ref: str, base_dir: Path) -> bytes:
    """Resolve file:// URIs.

    Supports:
      - file://relative/path (relative to base_dir)
      - file:///C:/path/on/windows (Windows-style file URI)
      - file:///absolute/path (POSIX absolute)

    NOTE: This resolver intentionally does NOT support http(s) in v0.3.
    """
    if not ref.startswith("file://"):
        raise ValueError(f"Unsupported ref scheme for v0.3: {ref}")

    path_part = ref[len("file://") :]

    # Handle common Windows file URI form: file:///C:/...
    if path_part.startswith("/") and len(path_part) >= 3 and path_part[2] == ":":
        path_part = path_part.lstrip("/")

    p = Path(path_part)

    if not p.is_absolute():
        p = (base_dir / p).resolve()

    if not p.exists():
        raise FileNotFoundError(f"Evidence file not found: {p}")

    return p.read_bytes()


class EvidenceSystem:
    """Evidence verification engine (v0.3: SHA-256 hash evidence)."""

    def verify_all(self, proposal: Dict[str, Any], *, base_dir: Path) -> EvidenceReport:
        evidence_list = proposal.get("evidence") or []
        if not evidence_list:
            return EvidenceReport(
                ok=False,
                results=[],
                verified_ids=set(),
            )

        results: List[EvidenceResult] = []
        verified: Set[str] = set()

        for raw in evidence_list:
            ev_id = raw.get("id", "<missing id>")
            try:
                ev = EvidenceRef(**raw)

                if ev.type != "hash":
                    raise ValueError(f"Unsupported evidence type for v0.3: {ev.type}")

                data = _resolve_file_uri(ev.ref, base_dir=base_dir)
                actual = _compute_sha256(data)
                expected = ev.sha256.lower()

                if actual.lower() != expected:
                    results.append(
                        EvidenceResult(
                            id=ev.id,
                            ok=False,
                            message=f"sha256 mismatch (expected {expected}, got {actual})",
                        )
                    )
                    continue

                verified.add(ev.id)
                results.append(EvidenceResult(id=ev.id, ok=True, message="sha256 verified"))

            except Exception as e:
                results.append(EvidenceResult(id=str(ev_id), ok=False, message=str(e)))

        ok = all(r.ok for r in results) and len(results) > 0
        return EvidenceReport(ok=ok, results=results, verified_ids=verified)


def apply_verified_ids_to_provenance(proposal: Dict[str, Any], verified_ids: Set[str]) -> Dict[str, Any]:
    """Upgrade provenance trust levels in-memory based on verified evidence IDs.

    v0.3 behavior:
      - Evidence verification yields verified IDs.
      - If a provenance entry's id is verified, we upgrade it to 'trusted'.

    This makes 'trusted' an OUTPUT of verification rather than a label.
    """
    out = dict(proposal)
    prov = [dict(p) for p in (proposal.get("provenance") or [])]
    for p in prov:
        if p.get("id") in verified_ids:
            p["trust"] = "trusted"
    out["provenance"] = prov
    return out
