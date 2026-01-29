"""Get documentation content for specific sections."""

import logging
from typing import Union

from equinox_mcp.docs_source import DocsSource

logger = logging.getLogger(__name__)


async def get_documentation(
    docs_source: DocsSource,
    section: Union[str, list[str]],
) -> str:
    """Retrieve documentation for requested sections.

    Args:
        docs_source: The documentation source
        section: Section name(s) or path(s) to retrieve.
                 Can be a single string or list of strings.
                 Examples: "attention", "api/nn/attention", ["module", "pattern"]

    Returns:
        Combined documentation content
    """
    # Normalize to list
    if isinstance(section, str):
        sections = [section]
    else:
        sections = section

    results = []
    available_sections = await docs_source.list_sections()
    section_map = {s["path"]: s for s in available_sections}
    title_map = {s["title"].lower(): s for s in available_sections}

    for sec in sections:
        try:
            # Try to resolve section name to path
            path = _resolve_section_path(sec, section_map, title_map)

            if path:
                content = await docs_source.get_file(path)
                results.append(f"## {sec}\n\n{content}")
            else:
                results.append(f"## {sec}\n\nSection not found: {sec}")

        except FileNotFoundError:
            results.append(f"## {sec}\n\nSection not found: {sec}")
        except Exception as e:
            logger.exception(f"Error fetching section {sec}")
            results.append(f"## {sec}\n\nError fetching section: {e}")

    return "\n\n---\n\n".join(results)


def _resolve_section_path(
    query: str,
    section_map: dict,
    title_map: dict,
) -> str | None:
    """Resolve a section query to a file path.

    Tries multiple matching strategies:
    1. Exact path match
    2. Partial path match (e.g., "attention" -> "api/nn/attention")
    3. Title match (case-insensitive)
    """
    query_lower = query.lower().strip()

    # 1. Exact path match
    if query in section_map:
        return query

    # 2. Partial path match - find paths containing the query
    for path in section_map:
        if query_lower in path.lower():
            return path

    # 3. Title match
    if query_lower in title_map:
        return title_map[query_lower]["path"]

    # 4. Fuzzy title match - check if query is substring of title
    for title, info in title_map.items():
        if query_lower in title:
            return info["path"]

    return None
