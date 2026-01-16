from __future__ import annotations

import argparse
import json
from pathlib import Path
from importlib import resources

from jsonschema import validate as js_validate, ValidationError

from .verifier import ActionProposal
from .evidence import EvidenceSystem, apply_verified_ids_to_provenance


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"File not found: {path}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"Invalid JSON in {path}: {e}")


def load_packaged_schema() -> dict:
    schema_text = (
        resources.files("pic_standard")
        .joinpath("schemas/proposal_schema.json")
        .read_text(encoding="utf-8")
    )
    return json.loads(schema_text)


def cmd_schema(proposal_path: Path) -> int:
    proposal = load_json(proposal_path)
    schema = load_packaged_schema()

    try:
        js_validate(instance=proposal, schema=schema)
        print("✅ Schema valid")
        return 0
    except ValidationError as e:
        print("❌ Schema invalid")
        print(str(e))
        return 2


def cmd_evidence_verify(proposal_path: Path) -> int:
    # Always validate schema first (consistent UX)
    code = cmd_schema(proposal_path)
    if code != 0:
        return code

    proposal = load_json(proposal_path)

    es = EvidenceSystem()
    report = es.verify_all(proposal, base_dir=proposal_path.parent)

    if not report.results:
        print("❌ Evidence verification failed")
        print("No evidence entries found in proposal (expected 'evidence': [...]).")
        return 4

    for r in report.results:
        if r.ok:
            print(f"✅ Evidence {r.id}: {r.message}")
        else:
            print(f"❌ Evidence {r.id}: {r.message}")

    if report.ok:
        print("✅ Evidence verification passed")
        return 0

    print("❌ Evidence verification failed")
    return 4


def cmd_verify(proposal_path: Path, *, verify_evidence: bool = False) -> int:
    code = cmd_schema(proposal_path)
    if code != 0:
        return code

    proposal = load_json(proposal_path)

    # Optional evidence verification (v0.3)
    if verify_evidence:
        es = EvidenceSystem()
        report = es.verify_all(proposal, base_dir=proposal_path.parent)

        if not report.results:
            print("❌ Evidence verification failed")
            print("No evidence entries found in proposal (expected 'evidence': [...]).")
            return 4

        if not report.ok:
            print("❌ Evidence verification failed")
            for r in report.results:
                if not r.ok:
                    print(f"- {r.id}: {r.message}")
            return 4

        # Upgrade provenance trust based on verified evidence IDs
        proposal = apply_verified_ids_to_provenance(proposal, report.verified_ids)

    try:
        ActionProposal(**proposal)
        print("✅ Verifier passed")
        return 0
    except Exception as e:
        print("❌ Verifier failed")
        print(str(e))
        return 3


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pic-cli", description="PIC Standard CLI utilities")
    sub = p.add_subparsers(dest="command", required=True)

    s1 = sub.add_parser("schema", help="Validate proposal against JSON Schema")
    s1.add_argument("proposal", type=Path)

    s2 = sub.add_parser("verify", help="Validate proposal against schema + verifier")
    s2.add_argument("proposal", type=Path)
    s2.add_argument(
        "--verify-evidence",
        action="store_true",
        help="Verify evidence (v0.3: sha256) and upgrade provenance to TRUSTED based on verified IDs before running verifier.",
    )

    s3 = sub.add_parser("evidence-verify", help="Verify evidence only (v0.3: sha256)")
    s3.add_argument("proposal", type=Path)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "schema":
        return cmd_schema(args.proposal)
    if args.command == "evidence-verify":
        return cmd_evidence_verify(args.proposal)
    if args.command == "verify":
        return cmd_verify(args.proposal, verify_evidence=getattr(args, "verify_evidence", False))

    raise SystemExit("Unknown command")


if __name__ == "__main__":
    raise SystemExit(main())

