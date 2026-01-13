from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, TYPE_CHECKING

from path_link.validation import Finding, Severity, ValidationResult

if TYPE_CHECKING:
    from path_link.model import _ProjectPathsBase


def _conflict_findings(conflict: set[str]) -> list[Finding]:
    return [
        Finding(
            severity=Severity.ERROR,
            code="CONFLICTING_KIND_RULES",
            field=k,
            message="Field listed as both must_be_dir and must_be_file",
        )
        for k in sorted(conflict)
    ]


def _missing_key_finding(key: str, is_required: bool) -> Finding:
    return Finding(
        severity=Severity.ERROR if is_required else Severity.WARNING,
        code="KEY_NOT_FOUND",
        field=key,
        message=f"Path key '{key}' not found in ProjectPaths model.",
    )


def _symlink_finding(key: str, path: Path, allow_symlinks: bool) -> Finding | None:
    if allow_symlinks or not path.is_symlink():
        return None
    return Finding(
        severity=Severity.ERROR,
        code="SYMLINK_BLOCKED",
        field=key,
        path=str(path),
        message="Symlinks not permitted",
    )


def _existence_findings(
    key: str,
    path: Path,
    exists: bool,
    is_required: bool,
    is_optional: bool,
) -> list[Finding]:
    if is_required and not exists:
        return [
            Finding(
                severity=Severity.ERROR,
                code="MISSING_REQUIRED",
                field=key,
                path=str(path),
                message="Required path missing",
            )
        ]
    if not exists and is_optional:
        return [
            Finding(
                severity=Severity.WARNING,
                code="MISSING_OPTIONAL",
                field=key,
                path=str(path),
                message="Optional path missing",
            )
        ]
    return []


def _kind_findings(
    key: str,
    path: Path,
    must_be_dir: bool,
    must_be_file: bool,
) -> list[Finding]:
    findings: list[Finding] = []
    if must_be_dir and not path.is_dir():
        findings.append(
            Finding(
                severity=Severity.ERROR,
                code="NOT_A_DIRECTORY",
                field=key,
                path=str(path),
                message="Expected directory",
            )
        )
    if must_be_file and not path.is_file():
        findings.append(
            Finding(
                severity=Severity.ERROR,
                code="NOT_A_FILE",
                field=key,
                path=str(path),
                message="Expected file",
            )
        )
    return findings


@dataclass
class StrictPathValidator:
    """
    Validates path existence, type (file/directory), and symlinks based on configured rules.
    """

    required: Iterable[str]
    must_be_dir: Iterable[str] = ()
    must_be_file: Iterable[str] = ()
    allow_symlinks: bool = False

    def validate(self, p: "_ProjectPathsBase") -> ValidationResult:
        """
        Validates paths against the configured rules.

        Args:
            p: The ProjectPaths instance to validate.

        Returns:
            A ValidationResult containing all findings.
        """
        vr = ValidationResult()
        all_paths = p.to_dict()

        req_set = set(self.required)
        dir_set = set(self.must_be_dir)
        file_set = set(self.must_be_file)

        # Configuration conflict guard
        conflict = dir_set & file_set
        if conflict:
            vr.add(*_conflict_findings(conflict))
            return vr

        keys_to_check = req_set | dir_set | file_set

        for k in keys_to_check:
            if k not in all_paths:
                vr.add(_missing_key_finding(k, k in req_set))
                continue

            path = Path(all_paths[k])

            symlink_finding = _symlink_finding(k, path, self.allow_symlinks)
            if symlink_finding:
                vr.add(symlink_finding)

            exists = path.exists()

            vr.add(
                *_existence_findings(
                    k,
                    path,
                    exists,
                    k in req_set,
                    k in dir_set or k in file_set,
                )
            )

            if exists:
                vr.add(*_kind_findings(k, path, k in dir_set, k in file_set))
        return vr
