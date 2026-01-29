"""Static analysis for Equinox module code."""

import ast
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class Issue:
    """A code issue found during analysis."""

    severity: str  # "error", "warning", "suggestion"
    message: str
    line: Optional[int] = None


async def equinox_checker(code: str) -> str:
    """Analyze Equinox module code and suggest fixes.

    Checks:
    - PyTree compliance (fields should be JAX arrays or have static=True)
    - Proper __init__ signature (should have key parameter)
    - __call__ signature (no batch dimension, optional key for dropout)
    - Common mistakes (mutable defaults, missing static=True)
    """
    issues: list[Issue] = []

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return f"Syntax error: {e}"

    # Find all class definitions
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            issues.extend(_check_class(node, code))

    if not issues:
        return "No issues found. Code looks good!"

    # Format output
    lines = ["## Equinox Code Analysis\n"]

    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]
    suggestions = [i for i in issues if i.severity == "suggestion"]

    if errors:
        lines.append("### Errors\n")
        for issue in errors:
            loc = f" (line {issue.line})" if issue.line else ""
            lines.append(f"- {issue.message}{loc}")
        lines.append("")

    if warnings:
        lines.append("### Warnings\n")
        for issue in warnings:
            loc = f" (line {issue.line})" if issue.line else ""
            lines.append(f"- {issue.message}{loc}")
        lines.append("")

    if suggestions:
        lines.append("### Suggestions\n")
        for issue in suggestions:
            loc = f" (line {issue.line})" if issue.line else ""
            lines.append(f"- {issue.message}{loc}")

    return "\n".join(lines)


def _check_class(node: ast.ClassDef, code: str) -> list[Issue]:
    """Check a class definition for Equinox patterns."""
    issues = []

    # Check if it looks like an Equinox module
    is_eqx_module = _is_equinox_module(node)
    if not is_eqx_module:
        return issues  # Skip non-Equinox classes

    # Check class-level annotations
    issues.extend(_check_annotations(node))

    # Check __init__ method
    init_method = _find_method(node, "__init__")
    if init_method:
        issues.extend(_check_init(init_method))

    # Check __call__ method
    call_method = _find_method(node, "__call__")
    if call_method:
        issues.extend(_check_call(call_method))

    return issues


def _is_equinox_module(node: ast.ClassDef) -> bool:
    """Check if class inherits from eqx.Module or equinox.Module."""
    for base in node.bases:
        base_name = _get_full_name(base)
        if base_name in ("eqx.Module", "equinox.Module", "Module"):
            return True
    return False


def _get_full_name(node: ast.expr) -> str:
    """Get full dotted name from an AST node."""
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return f"{_get_full_name(node.value)}.{node.attr}"
    return ""


def _find_method(node: ast.ClassDef, name: str) -> Optional[ast.FunctionDef]:
    """Find a method by name in a class."""
    for item in node.body:
        if isinstance(item, ast.FunctionDef) and item.name == name:
            return item
    return None


def _check_annotations(node: ast.ClassDef) -> list[Issue]:
    """Check class-level field annotations."""
    issues = []

    for item in node.body:
        if isinstance(item, ast.AnnAssign) and item.target:
            # Check if annotation includes field(static=True) for non-array types
            target_name = getattr(item.target, "id", "")
            annotation = item.annotation

            # Look for potential non-JAX types that should be static
            if _looks_like_hyperparameter(target_name, annotation):
                if not _has_static_field(item):
                    issues.append(
                        Issue(
                            severity="warning",
                            message=f"Field '{target_name}' looks like a hyperparameter. Consider using `field(static=True)` if it's not a JAX array.",
                            line=item.lineno,
                        )
                    )

            # Check for mutable defaults
            if item.value and _is_mutable_default(item.value):
                issues.append(
                    Issue(
                        severity="error",
                        message=f"Field '{target_name}' has a mutable default value. Use field(default_factory=...) instead.",
                        line=item.lineno,
                    )
                )

    return issues


def _looks_like_hyperparameter(name: str, annotation: Optional[ast.expr]) -> bool:
    """Check if a field looks like a hyperparameter based on name/type."""
    hp_names = {"num_heads", "hidden_size", "dropout_rate", "num_layers", "size", "dim"}
    if name in hp_names:
        return True

    # Check annotation for int, float, str, bool
    if annotation:
        ann_name = _get_full_name(annotation)
        if ann_name in ("int", "float", "str", "bool"):
            return True

    return False


def _has_static_field(node: ast.AnnAssign) -> bool:
    """Check if annotation uses field(static=True)."""
    if node.value and isinstance(node.value, ast.Call):
        func_name = _get_full_name(node.value.func)
        if "field" in func_name:
            for keyword in node.value.keywords:
                if keyword.arg == "static":
                    return True
    return False


def _is_mutable_default(node: ast.expr) -> bool:
    """Check if a default value is mutable (list, dict, set)."""
    return isinstance(node, (ast.List, ast.Dict, ast.Set))


def _check_init(node: ast.FunctionDef) -> list[Issue]:
    """Check __init__ method for Equinox patterns."""
    issues = []

    # Check for key parameter
    has_key = False
    for arg in node.args.args + node.args.kwonlyargs:
        if arg.arg == "key":
            has_key = True
            break

    if not has_key:
        issues.append(
            Issue(
                severity="suggestion",
                message="Consider adding a `key` parameter to __init__ for PRNG key handling. Equinox modules typically use explicit randomness.",
                line=node.lineno,
            )
        )

    return issues


def _check_call(node: ast.FunctionDef) -> list[Issue]:
    """Check __call__ method for Equinox patterns."""
    issues = []

    # Get parameter names (excluding self)
    params = [arg.arg for arg in node.args.args if arg.arg != "self"]

    # Check for batch dimension hint in docstring
    docstring = ast.get_docstring(node) or ""

    # Suggestion for key parameter if using dropout
    body_str = ast.unparse(node)
    if "dropout" in body_str.lower() or "Dropout" in body_str:
        has_key = "key" in params or any(
            arg.arg == "key" for arg in node.args.kwonlyargs
        )
        if not has_key:
            issues.append(
                Issue(
                    severity="warning",
                    message="__call__ uses dropout but doesn't have a `key` parameter. Add `*, key: Optional[PRNGKeyArray] = None` for stochastic layers.",
                    line=node.lineno,
                )
            )

    # Suggestion for shape comments
    if not any(comment in docstring for comment in ["[", "shape", "Shape"]):
        issues.append(
            Issue(
                severity="suggestion",
                message="Consider adding shape annotations in docstring or comments, e.g., `x: ArrayLike  # [seq, dim]`",
                line=node.lineno,
            )
        )

    return issues