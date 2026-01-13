from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, TYPE_CHECKING

from path_link.validation import Finding, Severity, ValidationResult

if TYPE_CHECKING:
    from path_link.model import _ProjectPathsBase


def _resolve_base_dir(
    all_paths: dict[str, Path], base_dir_key: str
) -> tuple[Path | None, Path | None, list[Finding]]:
    if base_dir_key not in all_paths:
        return (
            None,
            None,
            [
                Finding(
                    severity=Severity.ERROR,
                    code="SANDBOX_BASE_MISSING",
                    field=base_dir_key,
                    message=(
                        f"Sandbox base directory key '{base_dir_key}' not found in ProjectPaths."
                    ),
                )
            ],
        )

    base_dir = Path(all_paths[base_dir_key])
    try:
        base_dir_resolved = base_dir.resolve()
    except (OSError, RuntimeError) as e:
        return (
            None,
            None,
            [
                Finding(
                    severity=Severity.ERROR,
                    code="SANDBOX_BASE_UNRESOLVABLE",
                    field=base_dir_key,
                    path=str(base_dir),
                    message=f"Cannot resolve base directory: {e}",
                )
            ],
        )

    return base_dir, base_dir_resolved, []


def _keys_to_check(
    all_paths: dict[str, Path], check_paths: Iterable[str], base_dir_key: str
) -> set[str]:
    if check_paths:
        return set(check_paths)
    return set(all_paths.keys()) - {base_dir_key}


def _validate_path_entry(
    *,
    key: str,
    path: Path,
    base_dir: Path,
    base_dir_resolved: Path,
    allow_absolute: bool,
    strict_mode: bool,
) -> list[Finding]:
    path = Path(path)
    path_str = str(path)

    if strict_mode and ".." in path.parts:
        return [
            Finding(
                severity=Severity.ERROR,
                code="PATH_TRAVERSAL_ATTEMPT",
                field=key,
                path=path_str,
                message="Path contains '..' traversal pattern (blocked in strict mode)",
            )
        ]

    if path.is_absolute() and not allow_absolute:
        return [
            Finding(
                severity=Severity.ERROR,
                code="ABSOLUTE_PATH_BLOCKED",
                field=key,
                path=path_str,
                message="Absolute paths not allowed (set allow_absolute=True to permit)",
            )
        ]

    try:
        full_path = path if path.is_absolute() else base_dir / path
        path_resolved = full_path.resolve()
    except (OSError, RuntimeError) as e:
        return [
            Finding(
                severity=Severity.WARNING,
                code="PATH_UNRESOLVABLE",
                field=key,
                path=path_str,
                message=f"Cannot resolve path: {e}",
            )
        ]

    if full_path.is_symlink():
        try:
            full_path.resolve(strict=True)
        except FileNotFoundError:
            pass
        except (OSError, RuntimeError) as e:
            return [
                Finding(
                    severity=Severity.WARNING,
                    code="PATH_UNRESOLVABLE",
                    field=key,
                    path=path_str,
                    message=f"Cannot resolve path: {e}",
                )
            ]

    try:
        path_resolved.relative_to(base_dir_resolved)
    except ValueError:
        return [
            Finding(
                severity=Severity.ERROR,
                code="PATH_ESCAPES_SANDBOX",
                field=key,
                path=path_str,
                message=f"Path escapes sandbox (resolves outside {base_dir_resolved})",
            )
        ]

    return []


@dataclass
class SandboxPathValidator:
    """
    Validates that paths stay within a base directory sandbox.

    This is a security-focused validator that prevents path traversal attacks
    and ensures all paths remain within the project's base directory.

    Features:
    - Detects '..' path escape attempts
    - Validates paths stay within base_dir
    - Optionally allows absolute paths (with validation)
    - Configurable strict mode for maximum security
    """

    base_dir_key: str = "base_dir"
    """The key in ProjectPaths that represents the base directory."""

    check_paths: Iterable[str] = ()
    """Specific path keys to check. If empty, checks all paths."""

    allow_absolute: bool = False
    """Allow absolute paths that are within base_dir."""

    strict_mode: bool = True
    """In strict mode, block all attempts at path traversal, even if they resolve safely."""

    def validate(self, p: "_ProjectPathsBase") -> ValidationResult:
        """
        Validates that all paths stay within the base directory sandbox.

        Args:
            p: The ProjectPaths instance to validate.

        Returns:
            A ValidationResult containing all findings.
        """
        vr = ValidationResult()
        all_paths = p.to_dict()

        base_dir, base_dir_resolved, base_findings = _resolve_base_dir(
            all_paths, self.base_dir_key
        )
        if base_findings:
            vr.add(*base_findings)
            return vr

        keys_to_check = _keys_to_check(all_paths, self.check_paths, self.base_dir_key)

        for key in sorted(keys_to_check):
            if key not in all_paths:
                continue  # Skip missing keys - that's StrictPathValidator's job

            findings = _validate_path_entry(
                key=key,
                path=Path(all_paths[key]),
                base_dir=base_dir,
                base_dir_resolved=base_dir_resolved,
                allow_absolute=self.allow_absolute,
                strict_mode=self.strict_mode,
            )
            vr.add(*findings)

        return vr
