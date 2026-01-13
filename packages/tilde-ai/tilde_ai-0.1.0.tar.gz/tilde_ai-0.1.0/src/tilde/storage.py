"""Storage backends for tilde profiles."""

import json
import os
import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol

import yaml

from tilde.schema import TildeProfile


def get_default_profile_path() -> Path:
    """Get the default profile path (~/.tilde/profile.yaml)."""
    return Path.home() / ".tilde" / "profile.yaml"


class StorageBackend(Protocol):
    """Protocol for storage backends."""

    def load(self) -> TildeProfile:
        """Load the profile from storage."""
        ...

    def save(self, profile: TildeProfile) -> None:
        """Save the profile to storage."""
        ...

    def exists(self) -> bool:
        """Check if the profile exists."""
        ...


class YAMLStorage:
    """YAML file storage backend for human-readable profiles."""

    def __init__(self, path: Path | None = None):
        self.path = path or get_default_profile_path()

    def load(self) -> TildeProfile:
        """Load profile from YAML file."""
        if not self.exists():
            return TildeProfile()

        with open(self.path) as f:
            data = yaml.safe_load(f)

        if data is None:
            return TildeProfile()

        return TildeProfile.model_validate(data)

    def save(self, profile: TildeProfile) -> None:
        """Save profile to YAML file."""
        # Ensure directory exists
        self.path.parent.mkdir(parents=True, exist_ok=True)

        # Convert to dict, excluding None values for cleaner YAML
        data = profile.model_dump(exclude_none=True)

        with open(self.path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    def exists(self) -> bool:
        """Check if the profile file exists."""
        return self.path.exists()


class SQLiteStorage:
    """SQLite storage backend with query capabilities."""

    def __init__(self, path: Path | None = None):
        if path is None:
            path = Path.home() / ".tilde" / "tilde.db"
        self.path = path
        self._init_db()

    def _init_db(self) -> None:
        """Initialize the database schema."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.path) as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS profiles (
                    id INTEGER PRIMARY KEY,
                    data JSON NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                
                CREATE TABLE IF NOT EXISTS profile_fields (
                    id INTEGER PRIMARY KEY,
                    field_path TEXT NOT NULL,
                    field_value TEXT,
                    field_type TEXT,
                    updated_at TEXT NOT NULL
                );
                
                CREATE INDEX IF NOT EXISTS idx_field_path ON profile_fields(field_path);
                
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY,
                    content TEXT NOT NULL,
                    source TEXT,
                    category TEXT,
                    created_at TEXT NOT NULL
                );
                
                CREATE INDEX IF NOT EXISTS idx_category ON memories(category);
            """)

    def load(self) -> TildeProfile:
        """Load profile from SQLite."""
        with sqlite3.connect(self.path) as conn:
            cursor = conn.execute(
                "SELECT data FROM profiles ORDER BY id DESC LIMIT 1"
            )
            row = cursor.fetchone()
            
            if row is None:
                return TildeProfile()
            
            data = json.loads(row[0])
            return TildeProfile.model_validate(data)

    def save(self, profile: TildeProfile) -> None:
        """Save profile to SQLite."""
        data = profile.model_dump(exclude_none=True)
        now = datetime.now().isoformat()
        
        with sqlite3.connect(self.path) as conn:
            # Check if profile exists
            cursor = conn.execute("SELECT id FROM profiles LIMIT 1")
            row = cursor.fetchone()
            
            if row:
                conn.execute(
                    "UPDATE profiles SET data = ?, updated_at = ? WHERE id = ?",
                    (json.dumps(data), now, row[0])
                )
            else:
                conn.execute(
                    "INSERT INTO profiles (data, created_at, updated_at) VALUES (?, ?, ?)",
                    (json.dumps(data), now, now)
                )
            
            # Update searchable fields index
            self._index_fields(conn, data, now)

    def _index_fields(self, conn: sqlite3.Connection, data: dict[str, Any], timestamp: str) -> None:
        """Index profile fields for fast queries."""
        conn.execute("DELETE FROM profile_fields")
        
        def index_dict(d: dict[str, Any], prefix: str = "") -> None:
            for key, value in d.items():
                path = f"{prefix}.{key}" if prefix else key
                
                if isinstance(value, dict):
                    index_dict(value, path)
                elif isinstance(value, list):
                    for i, item in enumerate(value):
                        if isinstance(item, dict):
                            index_dict(item, f"{path}[{i}]")
                        else:
                            conn.execute(
                                "INSERT INTO profile_fields (field_path, field_value, field_type, updated_at) VALUES (?, ?, ?, ?)",
                                (f"{path}[{i}]", str(item), type(item).__name__, timestamp)
                            )
                else:
                    conn.execute(
                        "INSERT INTO profile_fields (field_path, field_value, field_type, updated_at) VALUES (?, ?, ?, ?)",
                        (path, str(value) if value else None, type(value).__name__, timestamp)
                    )
        
        index_dict(data)

    def exists(self) -> bool:
        """Check if the profile exists."""
        if not self.path.exists():
            return False
        
        with sqlite3.connect(self.path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM profiles")
            return cursor.fetchone()[0] > 0

    def query(self, field_pattern: str) -> list[tuple[str, str]]:
        """Query profile fields by pattern (supports SQL LIKE wildcards).
        
        Example:
            storage.query("user_profile.tech_stack.%")
            storage.query("%languages%")
        """
        with sqlite3.connect(self.path) as conn:
            cursor = conn.execute(
                "SELECT field_path, field_value FROM profile_fields WHERE field_path LIKE ?",
                (field_pattern,)
            )
            return cursor.fetchall()

    def add_memory(self, content: str, source: str | None = None, category: str | None = None) -> int:
        """Add a memory/note to the database."""
        now = datetime.now().isoformat()
        
        with sqlite3.connect(self.path) as conn:
            cursor = conn.execute(
                "INSERT INTO memories (content, source, category, created_at) VALUES (?, ?, ?, ?)",
                (content, source, category, now)
            )
            return cursor.lastrowid or 0

    def search_memories(self, query: str, category: str | None = None, limit: int = 10) -> list[dict[str, Any]]:
        """Search memories by content (basic text search)."""
        with sqlite3.connect(self.path) as conn:
            if category:
                cursor = conn.execute(
                    "SELECT id, content, source, category, created_at FROM memories WHERE content LIKE ? AND category = ? ORDER BY created_at DESC LIMIT ?",
                    (f"%{query}%", category, limit)
                )
            else:
                cursor = conn.execute(
                    "SELECT id, content, source, category, created_at FROM memories WHERE content LIKE ? ORDER BY created_at DESC LIMIT ?",
                    (f"%{query}%", limit)
                )
            
            return [
                {"id": row[0], "content": row[1], "source": row[2], "category": row[3], "created_at": row[4]}
                for row in cursor.fetchall()
            ]


class Mem0Storage:
    """Mem0-backed storage with semantic search capabilities.
    
    Requires: pip install mem0ai
    Uses Google embeddings by default (via GOOGLE_API_KEY).
    Falls back to OpenAI if OPENAI_API_KEY is set instead.
    """

    def __init__(self, user_id: str = "default", path: Path | None = None):
        try:
            from mem0 import Memory
        except ImportError:
            raise ImportError(
                "mem0ai is required for Mem0Storage. Install with: uv add mem0ai"
            )
        
        from tilde.config import get_config
        
        tilde_config = get_config()
        
        self.user_id = user_id
        self.path = path or Path.home() / ".tilde"
        self.path.mkdir(parents=True, exist_ok=True)
        
        # Build Mem0 config with embedder from tilde config
        config: dict[str, Any] = {
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "collection_name": "tilde_memories",
                    "path": str(self.path / "qdrant_data"),
                }
            }
        }
        
        # Configure embedder based on available API key
        if tilde_config.provider == "google":
            config["embedder"] = {
                "provider": "google",
                "config": {
                    "model": tilde_config.embedding_model,
                    "api_key": tilde_config.google_api_key,
                }
            }
        else:
            # OpenAI fallback
            config["embedder"] = {
                "provider": "openai",
                "config": {
                    "model": "text-embedding-3-small",
                    "api_key": tilde_config.openai_api_key,
                }
            }
        
        self._memory = Memory.from_config(config)
        self._yaml_storage = YAMLStorage(self.path / "profile.yaml")

    def load(self) -> TildeProfile:
        """Load profile (falls back to YAML for structured data)."""
        return self._yaml_storage.load()

    def save(self, profile: TildeProfile) -> None:
        """Save profile and sync key info to Mem0."""
        self._yaml_storage.save(profile)
        
        # Sync identity and preferences to Mem0 for semantic search
        identity = profile.user_profile.identity
        if identity.name:
            self._memory.add(
                f"User's name is {identity.name}",
                user_id=self.user_id,
                metadata={"category": "identity"}
            )
        if identity.role:
            self._memory.add(
                f"User's role is {identity.role}",
                user_id=self.user_id,
                metadata={"category": "identity"}
            )
        
        # Sync tech preferences
        for pref in profile.user_profile.tech_stack.preferences:
            self._memory.add(
                pref,
                user_id=self.user_id,
                metadata={"category": "tech_preference"}
            )
        
        # Sync domain knowledge
        for domain, knowledge in profile.user_profile.domain_knowledge.domains.items():
            self._memory.add(
                f"Domain expertise in {domain}: {knowledge}",
                user_id=self.user_id,
                metadata={"category": "domain", "domain": domain}
            )

    def exists(self) -> bool:
        """Check if profile exists."""
        return self._yaml_storage.exists()

    def add(self, content: str, category: str | None = None) -> dict[str, Any]:
        """Add a memory to Mem0."""
        metadata = {"category": category} if category else {}
        result = self._memory.add(content, user_id=self.user_id, metadata=metadata)
        return result

    def search(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        """Semantic search across all memories."""
        results = self._memory.search(query, user_id=self.user_id, limit=limit)
        return results

    def get_all(self) -> list[dict[str, Any]]:
        """Get all memories for the user."""
        return self._memory.get_all(user_id=self.user_id)


def get_storage(
    path: Path | None = None,
    backend: str | None = None,
) -> YAMLStorage | SQLiteStorage | Mem0Storage:
    """Get a storage backend instance.
    
    Args:
        path: Custom path for storage
        backend: One of "yaml", "sqlite", "mem0". Default: from TILDE_STORAGE env or "yaml"
    
    Environment variables:
        TILDE_PROFILE: Custom path for profile storage
        TILDE_STORAGE: Storage backend (yaml, sqlite, mem0)
    """
    # Check environment variables
    env_path = os.environ.get("TILDE_PROFILE")
    if env_path:
        path = Path(env_path)
    
    backend = backend or os.environ.get("TILDE_STORAGE", "yaml").lower()
    
    if backend == "sqlite":
        db_path = path.with_suffix(".db") if path else None
        return SQLiteStorage(db_path)
    elif backend == "mem0":
        return Mem0Storage(path=path.parent if path else None)
    else:
        return YAMLStorage(path)

