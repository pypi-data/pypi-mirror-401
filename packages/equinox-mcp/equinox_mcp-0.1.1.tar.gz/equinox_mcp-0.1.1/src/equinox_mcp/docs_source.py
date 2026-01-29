"""Documentation source handling - local filesystem or GitHub."""

import json
import os
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

import httpx
import yaml

logger = logging.getLogger(__name__)

# GitHub raw content base URL
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/patrick-kidger/equinox/main/docs"

# Default cache settings
DEFAULT_CACHE_DIR = Path.home() / ".cache" / "equinox-mcp"
DEFAULT_CACHE_TTL_HOURS = 24


class DocsSource:
    """Handles documentation fetching from local files or GitHub."""

    def __init__(self):
        # Check for local path first
        self.local_path = os.environ.get("EQUINOX_DOCS_PATH")
        self.cache_dir = Path(
            os.environ.get("EQUINOX_MCP_CACHE_DIR", DEFAULT_CACHE_DIR)
        )
        self.cache_ttl = timedelta(
            hours=int(os.environ.get("EQUINOX_MCP_CACHE_TTL", DEFAULT_CACHE_TTL_HOURS))
        )
        self.no_cache = os.environ.get("EQUINOX_MCP_NO_CACHE", "0") == "1"

        if self.local_path:
            self.local_path = Path(self.local_path)
            if not self.local_path.exists():
                logger.warning(
                    f"EQUINOX_DOCS_PATH={self.local_path} does not exist, falling back to GitHub"
                )
                self.local_path = None

        self.source_type = "local" if self.local_path else "github"
        logger.info(f"DocsSource initialized: {self.source_type}")

        # Ensure cache directory exists
        if not self.local_path:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Cache for sections metadata
        self._sections_cache: Optional[list[dict]] = None

    async def get_file(self, path: str) -> str:
        """Get a documentation file by path.

        Args:
            path: Relative path like 'api/nn/attention.md' or 'pattern.md'

        Returns:
            File content as string
        """
        # Ensure .md extension
        if not path.endswith(".md"):
            path = f"{path}.md"

        if self.local_path:
            return self._read_local(path)
        else:
            return await self._fetch_github(path)

    def _read_local(self, path: str) -> str:
        """Read from local filesystem."""
        file_path = self.local_path / path
        if not file_path.exists():
            raise FileNotFoundError(f"Doc not found: {file_path}")
        return file_path.read_text()

    async def _fetch_github(self, path: str) -> str:
        """Fetch from GitHub with caching."""
        # Check cache first
        cached = self._get_cached(path)
        if cached is not None:
            logger.debug(f"Cache hit: {path}")
            return cached

        # Fetch from GitHub
        url = f"{GITHUB_RAW_BASE}/{path}"
        logger.info(f"Fetching: {url}")

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            content = response.text

        # Cache the result
        self._set_cached(path, content)
        return content

    def _get_cached(self, path: str) -> Optional[str]:
        """Get cached content if valid."""
        if self.no_cache:
            return None

        cache_file = self.cache_dir / "docs" / path
        meta_file = self.cache_dir / "meta.json"

        if not cache_file.exists():
            return None

        # Check TTL
        if meta_file.exists():
            meta = json.loads(meta_file.read_text())
            cached_at = datetime.fromisoformat(meta.get("fetched_at", "2000-01-01"))
            if datetime.now() - cached_at > self.cache_ttl:
                logger.debug(f"Cache expired: {path}")
                return None

        return cache_file.read_text()

    def _set_cached(self, path: str, content: str):
        """Cache content to disk."""
        if self.no_cache:
            return

        cache_file = self.cache_dir / "docs" / path
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(content)

        # Update metadata
        meta_file = self.cache_dir / "meta.json"
        meta = {"fetched_at": datetime.now().isoformat()}
        meta_file.write_text(json.dumps(meta, indent=2))

    async def list_sections(self) -> list[dict]:
        """List all documentation sections.

        Returns:
            List of dicts with 'title', 'path', and 'use_cases' keys
        """
        if self._sections_cache is not None:
            return self._sections_cache

        sections = []

        if self.local_path:
            sections = self._scan_local_sections()
        else:
            sections = await self._fetch_sections_from_github()

        self._sections_cache = sections
        return sections

    def _scan_local_sections(self) -> list[dict]:
        """Scan local docs directory for sections."""
        sections = []

        for md_file in self.local_path.rglob("*.md"):
            rel_path = md_file.relative_to(self.local_path)
            # Skip hidden files and index
            if rel_path.name.startswith(".") or rel_path.name == "index.md":
                continue

            title = self._extract_title(md_file.read_text())
            use_cases = self._infer_use_cases(str(rel_path), title)

            sections.append(
                {
                    "title": title,
                    "path": str(rel_path).replace(".md", ""),
                    "use_cases": use_cases,
                }
            )

        return sorted(sections, key=lambda x: x["path"])

    async def _fetch_sections_from_github(self) -> list[dict]:
        """Fetch section list from GitHub.

        We'll try to get mkdocs.yml first for structure, then fall back to
        a hardcoded list of known sections.
        """
        try:
            mkdocs_content = await self._fetch_github("../mkdocs.yml")
            return self._parse_mkdocs_nav(mkdocs_content)
        except Exception as e:
            logger.warning(f"Could not fetch mkdocs.yml: {e}, using fallback")
            return self._get_fallback_sections()

    def _parse_mkdocs_nav(self, mkdocs_content: str) -> list[dict]:
        """Parse mkdocs.yml to extract navigation structure."""
        try:
            config = yaml.safe_load(mkdocs_content)
            nav = config.get("nav", [])
            return self._flatten_nav(nav)
        except Exception as e:
            logger.warning(f"Could not parse mkdocs.yml: {e}")
            return self._get_fallback_sections()

    def _flatten_nav(self, nav: list, prefix: str = "") -> list[dict]:
        """Flatten mkdocs nav structure into section list."""
        sections = []

        for item in nav:
            if isinstance(item, str):
                # Simple page reference
                sections.append(
                    {
                        "title": self._path_to_title(item),
                        "path": item.replace(".md", ""),
                        "use_cases": self._infer_use_cases(item, ""),
                    }
                )
            elif isinstance(item, dict):
                for title, value in item.items():
                    if isinstance(value, str):
                        # Named page
                        sections.append(
                            {
                                "title": title,
                                "path": value.replace(".md", ""),
                                "use_cases": self._infer_use_cases(value, title),
                            }
                        )
                    elif isinstance(value, list):
                        # Nested section
                        sections.extend(self._flatten_nav(value, title))

        return sections

    def _get_fallback_sections(self) -> list[dict]:
        """Fallback list of known Equinox doc sections."""
        return [
            {"title": "All of Equinox", "path": "all-of-equinox", "use_cases": "overview, getting started"},
            {"title": "FAQ", "path": "faq", "use_cases": "common questions, troubleshooting"},
            {"title": "Patterns", "path": "pattern", "use_cases": "best practices, design patterns"},
            {"title": "Tricks", "path": "tricks", "use_cases": "tips, advanced usage"},
            {"title": "Module", "path": "api/module/module", "use_cases": "always, base class, pytree"},
            {"title": "Advanced Fields", "path": "api/module/advanced_fields", "use_cases": "static fields, metadata"},
            {"title": "Attention", "path": "api/nn/attention", "use_cases": "transformers, attention, multihead"},
            {"title": "Linear", "path": "api/nn/linear", "use_cases": "dense, linear layers"},
            {"title": "MLP", "path": "api/nn/mlp", "use_cases": "feedforward, mlp"},
            {"title": "Conv", "path": "api/nn/conv", "use_cases": "convolution, cnn"},
            {"title": "Embedding", "path": "api/nn/embedding", "use_cases": "embeddings, rope, positional"},
            {"title": "Normalisation", "path": "api/nn/normalisation", "use_cases": "layernorm, rmsnorm, batchnorm"},
            {"title": "Dropout", "path": "api/nn/dropout", "use_cases": "regularization, dropout"},
            {"title": "Pool", "path": "api/nn/pool", "use_cases": "pooling, maxpool, avgpool"},
            {"title": "RNN", "path": "api/nn/rnn", "use_cases": "recurrent, lstm, gru"},
            {"title": "Sequential", "path": "api/nn/sequential", "use_cases": "composition, sequential"},
            {"title": "Shared", "path": "api/nn/shared", "use_cases": "parameter sharing"},
            {"title": "Stateful", "path": "api/nn/stateful", "use_cases": "stateful layers, batchnorm state"},
            {"title": "Transformations", "path": "api/transformations", "use_cases": "filter, partition, combine"},
            {"title": "Serialisation", "path": "api/serialisation", "use_cases": "save, load, checkpointing"},
            {"title": "Pretty Printing", "path": "api/pretty-printing", "use_cases": "debug, visualization"},
        ]

    def _extract_title(self, content: str) -> str:
        """Extract title from markdown content."""
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
        return "Untitled"

    def _path_to_title(self, path: str) -> str:
        """Convert path to title."""
        name = Path(path).stem
        return name.replace("-", " ").replace("_", " ").title()

    def _infer_use_cases(self, path: str, title: str) -> str:
        """Infer use cases from path and title."""
        keywords = []

        # From path
        path_lower = path.lower()
        if "nn" in path_lower:
            keywords.append("neural networks")
        if "attention" in path_lower:
            keywords.extend(["transformers", "attention"])
        if "conv" in path_lower:
            keywords.extend(["cnn", "convolution"])
        if "rnn" in path_lower or "lstm" in path_lower or "gru" in path_lower:
            keywords.extend(["recurrent", "sequence"])
        if "norm" in path_lower:
            keywords.append("normalization")
        if "module" in path_lower:
            keywords.extend(["always", "base class"])

        # From title
        title_lower = title.lower()
        if "pattern" in title_lower:
            keywords.append("best practices")
        if "faq" in title_lower:
            keywords.append("troubleshooting")

        return ", ".join(keywords) if keywords else "general"
