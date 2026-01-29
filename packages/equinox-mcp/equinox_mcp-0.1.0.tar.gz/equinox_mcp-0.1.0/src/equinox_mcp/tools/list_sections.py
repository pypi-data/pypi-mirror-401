"""List available documentation sections."""

from equinox_mcp.docs_source import DocsSource


async def list_sections(docs_source: DocsSource) -> str:
    """List all available documentation sections.

    Returns formatted list with title, use_cases, and path for each section.
    """
    sections = await docs_source.list_sections()

    lines = []
    for section in sections:
        title = section.get("title", "Untitled")
        path = section.get("path", "")
        use_cases = section.get("use_cases", "general")

        lines.append(f"* title: {title}, use_cases: {use_cases}, path: {path}")

    return "\n".join(lines)
