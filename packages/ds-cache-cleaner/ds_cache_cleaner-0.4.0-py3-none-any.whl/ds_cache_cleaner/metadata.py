"""Metadata management for cache entries.

This module provides a standardized format for cache metadata that libraries
can use to provide richer information about their cached data.

Structure inside each cache directory:
    ds-cache-cleaner/
    ├── lock                    # Lock file for concurrent access
    ├── information.json        # Basic info about the cache and its parts
    └── part_<name>.json        # Entries for each part (e.g., part_models.json)

Schema for information.json:
{
    "version": 1,
    "library": "huggingface-hub",
    "description": "HuggingFace Hub cache",
    "parts": [
        {"name": "models", "description": "Downloaded model files"},
        {"name": "datasets", "description": "Downloaded dataset files"}
    ]
}

Schema for part_<name>.json:
{
    "version": 1,
    "entries": [
        {
            "path": "models--bert-base-uncased",
            "description": "BERT base uncased model",
            "created": "2024-01-15T10:30:00Z",
            "last_access": "2024-03-20T14:22:00Z",
            "size": 438123456,
            "metadata": {}  # Optional library-specific metadata
        }
    ]
}
"""

import dataclasses
import fcntl
import json
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, cast

from pydantic import TypeAdapter

from ds_cache_cleaner.utils import get_directory_size

METADATA_DIR = "ds-cache-cleaner"
LOCK_FILE = "lock"
INFO_FILE = "information.json"
PART_PREFIX = "part_"
CURRENT_VERSION = 1

# Base field names for EntryMetadata (used for subclass field detection)
_ENTRY_BASE_FIELDS = frozenset(
    {"path", "description", "created", "last_access", "size", "metadata"}
)


def _get_extra_fields(cls: type) -> set[str]:
    """Get field names that are not in the base EntryMetadata class."""
    if not dataclasses.is_dataclass(cls):
        return set()
    return {f.name for f in dataclasses.fields(cls)} - _ENTRY_BASE_FIELDS


@dataclass
class PartInfo:
    """Information about a cache part."""

    name: str
    description: str = ""


@dataclass
class CacheInfo:
    """Information about a cache."""

    version: int = CURRENT_VERSION
    library: str = ""
    description: str = ""
    parts: list[PartInfo] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "version": self.version,
            "library": self.library,
            "description": self.description,
            "parts": [
                {"name": p.name, "description": p.description} for p in self.parts
            ],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CacheInfo":
        """Create from dictionary."""
        return cast("CacheInfo", _CacheInfoAdapter.validate_python(data))


@dataclass
class EntryMetadata:
    """Metadata for a single cache entry."""

    path: str
    description: str = ""
    created: datetime | None = None
    last_access: datetime | None = None
    size: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization.

        Extra fields from subclasses are stored in the metadata dict.
        """
        result: dict[str, Any] = {"path": self.path}
        if self.description:
            result["description"] = self.description
        if self.created:
            result["created"] = self.created.isoformat()
        if self.last_access:
            result["last_access"] = self.last_access.isoformat()
        if self.size is not None:
            result["size"] = self.size

        # Merge extra fields from subclasses into metadata
        extra_fields = _get_extra_fields(type(self))
        merged_metadata = dict(self.metadata)
        for field_name in extra_fields:
            value = getattr(self, field_name)
            if value not in (None, "", [], {}):
                merged_metadata[field_name] = value

        if merged_metadata:
            result["metadata"] = merged_metadata
        return result

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
        entry_type: type["EntryMetadata"] | None = None,
    ) -> "EntryMetadata":
        """Create from dictionary.

        Args:
            data: Dictionary with entry data.
            entry_type: Optional subclass to instantiate. If provided, extra fields
                       are extracted from the metadata dict and passed to constructor.
        """
        target_cls = entry_type or cls
        adapter = TypeAdapter(target_cls)

        if entry_type is not None and entry_type is not EntryMetadata:
            # Extract extra fields from metadata for subclass
            extra_fields = _get_extra_fields(entry_type)
            if extra_fields and "metadata" in data:
                data = data.copy()
                metadata = dict(data.get("metadata", {}))
                for field_name in extra_fields:
                    if field_name in metadata:
                        data[field_name] = metadata.pop(field_name)
                data["metadata"] = metadata

        return cast("EntryMetadata", adapter.validate_python(data))


@dataclass
class PartData:
    """Data for a cache part."""

    version: int = CURRENT_VERSION
    entries: list[EntryMetadata] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "version": self.version,
            "entries": [e.to_dict() for e in self.entries],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PartData":
        """Create from dictionary."""
        return cast("PartData", _PartDataAdapter.validate_python(data))


# TypeAdapters for validation during deserialization
_CacheInfoAdapter: TypeAdapter[CacheInfo] = TypeAdapter(CacheInfo)
_EntryMetadataAdapter: TypeAdapter[EntryMetadata] = TypeAdapter(EntryMetadata)
_PartDataAdapter: TypeAdapter[PartData] = TypeAdapter(PartData)


class MetadataManager:
    """Manages cache metadata for a specific cache directory."""

    def __init__(self, cache_path: Path) -> None:
        """Initialize the metadata manager.

        Args:
            cache_path: Path to the cache directory
        """
        self.cache_path = cache_path
        self.metadata_dir = cache_path / METADATA_DIR
        self.lock_path = self.metadata_dir / LOCK_FILE
        self.info_path = self.metadata_dir / INFO_FILE

    @property
    def exists(self) -> bool:
        """Check if metadata exists for this cache."""
        return self.info_path.exists()

    def _ensure_dir(self) -> None:
        """Ensure the metadata directory exists."""
        self.metadata_dir.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def lock(self, exclusive: bool = False) -> Iterator[None]:
        """Acquire a lock on the metadata directory.

        Args:
            exclusive: If True, acquire an exclusive (write) lock.
                      If False, acquire a shared (read) lock.
        """
        self._ensure_dir()
        lock_file = open(self.lock_path, "w")
        try:
            if exclusive:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
            else:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_SH)
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
            lock_file.close()

    def _read_info_unlocked(self) -> CacheInfo | None:
        """Read the cache information file without acquiring lock (internal use)."""
        if not self.info_path.exists():
            return None
        data = json.loads(self.info_path.read_text())
        return CacheInfo.from_dict(data)

    def _write_info_unlocked(self, info: CacheInfo) -> None:
        """Write the cache information file without acquiring lock (internal use)."""
        self._ensure_dir()
        self.info_path.write_text(json.dumps(info.to_dict(), indent=2))

    def read_info(self) -> CacheInfo | None:
        """Read the cache information file.

        Returns:
            CacheInfo if the file exists, None otherwise.
        """
        with self.lock(exclusive=False):
            return self._read_info_unlocked()

    def write_info(self, info: CacheInfo) -> None:
        """Write the cache information file.

        Args:
            info: The cache information to write.
        """
        with self.lock(exclusive=True):
            self._write_info_unlocked(info)

    def _part_path(self, part_name: str) -> Path:
        """Get the path to a part file."""
        return self.metadata_dir / f"{PART_PREFIX}{part_name}.json"

    def _read_part_unlocked(self, part_name: str) -> PartData | None:
        """Read a part data file without acquiring lock (internal use)."""
        part_path = self._part_path(part_name)
        if not part_path.exists():
            return None
        data = json.loads(part_path.read_text())
        return PartData.from_dict(data)

    def _write_part_unlocked(self, part_name: str, part_data: PartData) -> None:
        """Write a part data file without acquiring lock (internal use)."""
        self._ensure_dir()
        part_path = self._part_path(part_name)
        part_path.write_text(json.dumps(part_data.to_dict(), indent=2))

    def read_part(self, part_name: str) -> PartData | None:
        """Read a part data file.

        Args:
            part_name: Name of the part (e.g., "models", "datasets").

        Returns:
            PartData if the file exists, None otherwise.
        """
        with self.lock(exclusive=False):
            return self._read_part_unlocked(part_name)

    def write_part(self, part_name: str, part_data: PartData) -> None:
        """Write a part data file.

        Args:
            part_name: Name of the part.
            part_data: The part data to write.
        """
        with self.lock(exclusive=True):
            self._write_part_unlocked(part_name, part_data)

    def get_all_parts(self) -> dict[str, PartData]:
        """Read all part files.

        Returns:
            Dictionary mapping part names to their data.
        """
        result: dict[str, PartData] = {}
        if not self.metadata_dir.exists():
            return result

        with self.lock(exclusive=False):
            for path in self.metadata_dir.glob(f"{PART_PREFIX}*.json"):
                part_name = path.stem[len(PART_PREFIX) :]
                data = json.loads(path.read_text())
                result[part_name] = PartData.from_dict(data)

        return result

    def update_entry_access(self, part_name: str, entry_path: str) -> None:
        """Update the last access time for an entry.

        Args:
            part_name: Name of the part containing the entry.
            entry_path: Relative path of the entry.
        """
        with self.lock(exclusive=True):
            part_data = self._read_part_unlocked(part_name)
            if part_data is None:
                return

            for entry in part_data.entries:
                if entry.path == entry_path:
                    entry.last_access = datetime.now()
                    break

            self._write_part_unlocked(part_name, part_data)

    def remove_entry(self, part_name: str, entry_path: str) -> bool:
        """Remove an entry from the metadata.

        Args:
            part_name: Name of the part containing the entry.
            entry_path: Relative path of the entry.

        Returns:
            True if the entry was removed, False if not found.
        """
        with self.lock(exclusive=True):
            part_data = self._read_part_unlocked(part_name)
            if part_data is None:
                return False

            original_count = len(part_data.entries)
            part_data.entries = [e for e in part_data.entries if e.path != entry_path]

            if len(part_data.entries) < original_count:
                self._write_part_unlocked(part_name, part_data)
                return True

            return False

    def add_entry(
        self,
        part_name: str,
        entry: EntryMetadata,
        update_if_exists: bool = True,
    ) -> None:
        """Add or update an entry in the metadata.

        Args:
            part_name: Name of the part.
            entry: The entry metadata.
            update_if_exists: If True, update existing entry; if False, skip.
        """
        with self.lock(exclusive=True):
            part_data = self._read_part_unlocked(part_name)
            if part_data is None:
                part_data = PartData()

            # Check if entry exists
            for i, existing in enumerate(part_data.entries):
                if existing.path == entry.path:
                    if update_if_exists:
                        part_data.entries[i] = entry
                    self._write_part_unlocked(part_name, part_data)
                    return

            # Add new entry
            part_data.entries.append(entry)
            self._write_part_unlocked(part_name, part_data)


class PartAccessor:
    """Accessor for a specific part in the registry.

    Provides a convenient interface to work with entries in a part:
        registry.parts.models.register(entry)
        registry.parts.models.get("bert-base")
        registry.parts.models.list()
    """

    def __init__(self, registry: "CacheRegistry", part_name: str) -> None:
        self._registry = registry
        self._part_name = part_name

    def register(
        self,
        path: "EntryMetadata | str",
        description: str = "",
        size: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Register an entry in this part.

        Args:
            path: Either an EntryMetadata instance or a path string.
            description: Human-readable description (ignored if path is instance).
            size: Size in bytes (ignored if path is instance).
            metadata: Additional metadata (ignored if path is instance).
        """
        self._registry.register_entry(
            self._part_name, path, description, size, metadata
        )

    def get(self, path: str) -> "EntryMetadata | None":
        """Get an entry by path."""
        return self._registry.get_entry(self._part_name, path)

    def get_entry(self, path: str) -> "EntryMetadata | None":
        """Get an entry by path (alias for get)."""
        return self._registry.get_entry(self._part_name, path)

    def list(self) -> list["EntryMetadata"]:
        """List all entries in this part."""
        return self._registry.list_entries(self._part_name)

    def touch(self, path: str) -> None:
        """Update the last access time for an entry."""
        self._registry.touch(self._part_name, path)

    def remove(self, path: str) -> bool:
        """Remove an entry from this part."""
        return self._registry.remove(self._part_name, path)

    def update_size(self, path: str, size: int) -> None:
        """Update the size of an entry."""
        self._registry.update_size(self._part_name, path, size)


class PartsAccessor:
    """Dynamic accessor for registry parts.

    Allows attribute-style access to parts:
        registry.parts.models.register(entry)
        registry.parts.datasets.list()
    """

    def __init__(self, registry: "CacheRegistry") -> None:
        self._registry = registry
        self._cache: dict[str, PartAccessor] = {}

    def __getattr__(self, name: str) -> PartAccessor:
        if name.startswith("_"):
            raise AttributeError(name)
        if name not in self._cache:
            self._cache[name] = PartAccessor(self._registry, name)
        return self._cache[name]


class CacheRegistry:
    """High-level API for libraries to register and update their cache entries.

    This provides a simple interface for ML libraries to integrate with
    ds-cache-cleaner.

    Example usage by a library:
        ```python
        from ds_cache_cleaner.metadata import CacheRegistry

        # Initialize once for your library
        registry = CacheRegistry(
            cache_path=Path("~/.cache/mylib").expanduser(),
            library="mylib",
            description="My ML Library cache",
        )

        # Register a part (e.g., models, datasets)
        registry.register_part("models", "Downloaded model weights")

        # When downloading/accessing a model
        registry.register_entry(
            part="models",
            path="bert-base",
            description="BERT base model",
            size=438_000_000,
        )

        # When accessing an existing entry
        registry.touch("models", "bert-base")

        # When deleting an entry
        registry.remove("models", "bert-base")
        ```
    """

    def __init__(
        self,
        cache_path: Path | str,
        library: str,
        description: str = "",
        entry_types: dict[str, type[EntryMetadata]] | None = None,
    ) -> None:
        """Initialize the cache registry.

        Args:
            cache_path: Path to the cache directory.
            library: Name of the library (e.g., "huggingface-hub").
            description: Human-readable description of the cache.
            entry_types: Optional mapping of part names to custom EntryMetadata
                        subclasses. When set, get_entry() and list_entries()
                        return instances of the custom type.
        """
        if isinstance(cache_path, str):
            cache_path = Path(cache_path)
        self.cache_path = cache_path.expanduser()
        self.library = library
        self.description = description
        self._manager = MetadataManager(self.cache_path)
        self._initialized = False
        self._entry_types: dict[str, type[EntryMetadata]] = entry_types or {}
        self._parts_accessor: PartsAccessor | None = None

    @property
    def parts(self) -> PartsAccessor:
        """Access parts via attribute-style notation.

        Example:
            registry.parts.models.register(entry)
            registry.parts.models.get("bert-base")
            registry.parts.datasets.list()
        """
        if self._parts_accessor is None:
            self._parts_accessor = PartsAccessor(self)
        return self._parts_accessor

    def _ensure_initialized(self) -> None:
        """Ensure the cache info is initialized."""
        if self._initialized:
            return

        with self._manager.lock(exclusive=True):
            info = self._manager._read_info_unlocked()
            if info is None:
                info = CacheInfo(
                    library=self.library,
                    description=self.description,
                    parts=[],
                )
                self._manager._write_info_unlocked(info)
        self._initialized = True

    def register_part(self, name: str, description: str = "") -> None:
        """Register a new part in the cache.

        Args:
            name: Name of the part (e.g., "models", "datasets").
            description: Human-readable description.
        """
        self._ensure_initialized()

        with self._manager.lock(exclusive=True):
            info = self._manager._read_info_unlocked()
            if info is None:
                info = CacheInfo(library=self.library, description=self.description)

            # Check if part already exists
            for part in info.parts:
                if part.name == name:
                    part.description = description
                    self._manager._write_info_unlocked(info)
                    return

            info.parts.append(PartInfo(name=name, description=description))
            self._manager._write_info_unlocked(info)

            # Initialize empty part file if it doesn't exist
            if self._manager._read_part_unlocked(name) is None:
                self._manager._write_part_unlocked(name, PartData())

    def register_entry(
        self,
        part: str,
        path: EntryMetadata | str,
        description: str = "",
        size: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Register a new cache entry or update an existing one.

        Can be called with an EntryMetadata instance (or subclass):
            registry.register_entry("models", ModelEntry(path="x", ...))

        Or with individual parameters (backward compatible):
            registry.register_entry("models", "x", description="...", size=100)

        Args:
            part: Name of the part this entry belongs to.
            path: Either an EntryMetadata instance or a path string.
            description: Human-readable description (ignored if path is instance).
            size: Size in bytes. If None, computed from filesystem.
            metadata: Additional metadata (ignored if path is instance).
        """
        self._ensure_initialized()

        if isinstance(path, EntryMetadata):
            entry_obj = path
            now = datetime.now()
            if entry_obj.created is None:
                entry_obj.created = now
            if entry_obj.last_access is None:
                entry_obj.last_access = now
        else:
            now = datetime.now()
            entry_obj = EntryMetadata(
                path=path,
                description=description,
                created=now,
                last_access=now,
                size=size,
                metadata=metadata or {},
            )

        # Compute size from filesystem if not provided
        if entry_obj.size is None:
            full_path = self.cache_path / entry_obj.path
            entry_obj.size = get_directory_size(full_path)

        self._manager.add_entry(part, entry_obj, update_if_exists=True)

    def touch(self, part: str, path: str) -> None:
        """Update the last access time for an entry.

        This should be called when accessing/using an existing cache entry.

        Args:
            part: Name of the part.
            path: Relative path of the entry.
        """
        self._manager.update_entry_access(part, path)

    def remove(self, part: str, path: str) -> bool:
        """Remove an entry from the metadata.

        This should be called when deleting a cache entry.
        Note: This only removes the metadata, not the actual files.

        Args:
            part: Name of the part.
            path: Relative path of the entry.

        Returns:
            True if the entry was removed, False if not found.
        """
        return self._manager.remove_entry(part, path)

    def update_size(self, part: str, path: str, size: int) -> None:
        """Update the size of an entry.

        Args:
            part: Name of the part.
            path: Relative path of the entry.
            size: New size in bytes.
        """
        with self._manager.lock(exclusive=True):
            part_data = self._manager._read_part_unlocked(part)
            if part_data is None:
                return

            for entry in part_data.entries:
                if entry.path == path:
                    entry.size = size
                    self._manager._write_part_unlocked(part, part_data)
                    return

    def get_entry(self, part: str, path: str) -> EntryMetadata | None:
        """Get metadata for a specific entry.

        If an entry_type was registered for this part, the returned entry
        will be an instance of that type.

        Args:
            part: Name of the part.
            path: Relative path of the entry.

        Returns:
            EntryMetadata (or subclass) if found, None otherwise.
        """
        part_data = self._manager.read_part(part)
        if part_data is None:
            return None

        entry_type = self._entry_types.get(part, EntryMetadata)
        for entry in part_data.entries:
            if entry.path == path:
                if entry_type is not EntryMetadata:
                    return EntryMetadata.from_dict(entry.to_dict(), entry_type)
                return entry
        return None

    def list_entries(self, part: str) -> list[EntryMetadata]:
        """List all entries in a part.

        If an entry_type was registered for this part, the returned entries
        will be instances of that type.

        Args:
            part: Name of the part.

        Returns:
            List of entry metadata (or subclass instances).
        """
        part_data = self._manager.read_part(part)
        if part_data is None:
            return []

        entry_type = self._entry_types.get(part, EntryMetadata)
        if entry_type is EntryMetadata:
            return part_data.entries

        return [
            EntryMetadata.from_dict(e.to_dict(), entry_type) for e in part_data.entries
        ]

    def list_parts(self) -> list[PartInfo]:
        """List all parts in the cache.

        Returns:
            List of part information.
        """
        info = self._manager.read_info()
        if info is None:
            return []
        return info.parts
