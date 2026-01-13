"""Memory - Project state storage.

Stores and retrieves project knowledge: decisions, patterns, findings, context.
Persists to JSON files with future support for semantic search.

See docs/control_plane_spec.md Section 3.3 for details.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json


@dataclass
class MemoryEntry:
    """A single memory entry."""

    id: str  # e.g., "dec_001", "pat_003"
    type: str  # "decision", "pattern", "finding", "context"
    timestamp: datetime
    project: str
    title: str
    content: str
    tags: list[str] = field(default_factory=list)
    source: str = "discussion"  # "discussion", "code", "analysis", "review"
    embedding: list[float] | None = None  # For semantic search (Phase 2+)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "type": self.type,
            "timestamp": self.timestamp.isoformat(),
            "project": self.project,
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
            "source": self.source,
            "embedding": self.embedding,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MemoryEntry":
        """Create from dictionary."""
        data = data.copy()
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)


class Memory:
    """Project memory storage.

    Usage:
        memory = Memory("memory/")
        entry_id = memory.store(entry)
        results = memory.search("routing", entry_type="decision")
    """

    def __init__(self, base_path: str = "memory/"):
        self.base_path = Path(base_path)
        self._index: dict[str, dict] = {}  # id -> metadata
        self._ensure_directories()
        self._load_index()

    def _ensure_directories(self) -> None:
        """Create memory directory structure if needed."""
        self.base_path.mkdir(parents=True, exist_ok=True)
        for subdir in ["decisions", "patterns", "findings", "context"]:
            (self.base_path / subdir).mkdir(parents=True, exist_ok=True)

    def _load_index(self) -> None:
        """Load the index file.
        """
        index_path = self.base_path / "index.json"
        if not index_path.exists():
            self._index = {}
            return
        with open(index_path) as f:
            self._index = json.load(f)

    def _save_index(self) -> None:
        """Save the index file.
        """
        index_path = self.base_path / "index.json"
        with open(index_path, "w") as f:
            json.dump(self._index, f, indent=2)

    def store(self, entry: MemoryEntry) -> str:
        """Store an entry, return its ID.

        Args:
            entry: The memory entry to store

        Returns:
            The entry ID

        """
        entry_type = entry.type
        prefix_map = {
            "decision": "dec_",
            "pattern": "pat_",
            "finding": "find_",
            "context": "ctx_",
        }
        if entry_type not in prefix_map:
            raise ValueError(f"Invalid entry type: {entry_type}")
        if not entry.id.startswith(prefix_map[entry_type]):
            raise ValueError(
                f"Entry id '{entry.id}' does not match type '{entry_type}'"
            )
        if "/" in entry.id or ".." in entry.id:
            raise ValueError("Entry id contains invalid path characters")

        subdir_map = {
            "decision": "decisions",
            "pattern": "patterns",
            "finding": "findings",
            "context": "context",
        }
        subdir = subdir_map[entry_type]
        rel_path = f"{subdir}/{entry.id}.json"
        path = self.base_path / rel_path

        with open(path, "w") as f:
            json.dump(entry.to_dict(), f, indent=2)

        self._index[entry.id] = {
            "type": entry.type,
            "path": rel_path,
            "project": entry.project,
            "title": entry.title,
            "tags": entry.tags,
            "timestamp": entry.timestamp.isoformat(),
        }
        self._save_index()
        return entry.id

    def get(self, entry_id: str) -> MemoryEntry | None:
        """Retrieve an entry by ID.
        """
        meta = self._index.get(entry_id)
        if meta is None:
            # Fallback: scan directories if index is missing the entry.
            for subdir in ["decisions", "patterns", "findings", "context"]:
                path = self.base_path / subdir / f"{entry_id}.json"
                if path.exists():
                    with open(path) as f:
                        entry = MemoryEntry.from_dict(json.load(f))
                    self._index[entry_id] = {
                        "type": entry.type,
                        "path": f"{subdir}/{entry_id}.json",
                        "project": entry.project,
                        "title": entry.title,
                        "tags": entry.tags,
                        "timestamp": entry.timestamp.isoformat(),
                    }
                    self._save_index()
                    return entry
            return None

        path = self.base_path / meta["path"]
        if not path.exists():
            return None
        with open(path) as f:
            return MemoryEntry.from_dict(json.load(f))

    def search(
        self, query: str, entry_type: str | None = None, limit: int = 10
    ) -> list[MemoryEntry]:
        """Search entries by text match.

        Args:
            query: Search query string
            entry_type: Optional filter by type
            limit: Maximum results to return

        """
        query_lower = query.lower()
        results: list[MemoryEntry] = []

        for entry_id, meta in self._index.items():
            if entry_type and meta.get("type") != entry_type:
                continue
            path = self.base_path / meta["path"]
            if not path.exists():
                continue
            with open(path) as f:
                entry = MemoryEntry.from_dict(json.load(f))

            haystack = " ".join(
                [entry.title, entry.content, " ".join(entry.tags)]
            ).lower()
            if query_lower in haystack:
                results.append(entry)
                if len(results) >= limit:
                    break

        results.sort(key=lambda e: e.timestamp, reverse=True)
        return results[:limit]

    def list_by_type(self, entry_type: str) -> list[MemoryEntry]:
        """List all entries of a given type.
        """
        entries = []
        for entry_id, meta in self._index.items():
            if meta.get("type") != entry_type:
                continue
            path = self.base_path / meta["path"]
            if not path.exists():
                continue
            with open(path) as f:
                entries.append(MemoryEntry.from_dict(json.load(f)))
        entries.sort(key=lambda e: e.timestamp, reverse=True)
        return entries

    def get_recent(self, limit: int = 10) -> list[MemoryEntry]:
        """Get most recent entries.
        """
        entries = []
        for entry_id, meta in self._index.items():
            path = self.base_path / meta["path"]
            if not path.exists():
                continue
            with open(path) as f:
                entries.append(MemoryEntry.from_dict(json.load(f)))
        entries.sort(key=lambda e: e.timestamp, reverse=True)
        return entries[:limit]
