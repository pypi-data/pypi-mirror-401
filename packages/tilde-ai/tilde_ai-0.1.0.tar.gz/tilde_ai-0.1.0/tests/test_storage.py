"""Tests for tilde storage."""

import tempfile
from pathlib import Path

import pytest
import yaml

from tilde.schema import Identity, TildeProfile, UserProfile
from tilde.storage import YAMLStorage


@pytest.fixture
def temp_profile_path():
    """Create a temporary profile path."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir) / "profile.yaml"


def test_yaml_storage_save_and_load(temp_profile_path: Path):
    """Test saving and loading a profile."""
    storage = YAMLStorage(temp_profile_path)

    # Create and save profile
    profile = TildeProfile(
        user_profile=UserProfile(
            identity=Identity(name="Allen", role="SWE", years_experience=12)
        )
    )
    storage.save(profile)

    # Verify file exists
    assert temp_profile_path.exists()

    # Load and verify
    loaded = storage.load()
    assert loaded.user_profile.identity.name == "Allen"
    assert loaded.user_profile.identity.years_experience == 12


def test_yaml_storage_creates_directory(temp_profile_path: Path):
    """Test that save creates parent directories."""
    nested_path = temp_profile_path.parent / "nested" / "dir" / "profile.yaml"
    storage = YAMLStorage(nested_path)

    profile = TildeProfile()
    storage.save(profile)

    assert nested_path.exists()


def test_yaml_storage_load_nonexistent(temp_profile_path: Path):
    """Test loading from nonexistent file returns default profile."""
    storage = YAMLStorage(temp_profile_path)

    profile = storage.load()
    assert profile.schema_version == "1.0.0"
    assert profile.user_profile.identity.name == ""


def test_yaml_storage_exists(temp_profile_path: Path):
    """Test exists() method."""
    storage = YAMLStorage(temp_profile_path)

    assert not storage.exists()

    storage.save(TildeProfile())
    assert storage.exists()


def test_yaml_storage_human_readable(temp_profile_path: Path):
    """Test that saved YAML is human-readable."""
    storage = YAMLStorage(temp_profile_path)

    profile = TildeProfile(
        user_profile=UserProfile(
            identity=Identity(name="Allen")
        )
    )
    storage.save(profile)

    # Read raw file content
    content = temp_profile_path.read_text()

    # Should be readable YAML, not minified
    assert "name: Allen" in content
    assert "schema_version:" in content

    # Should parse as YAML
    data = yaml.safe_load(content)
    assert data["user_profile"]["identity"]["name"] == "Allen"


# =============================================================================
# SQLite Storage Tests
# =============================================================================


@pytest.fixture
def temp_db_path():
    """Create a temporary database path."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir) / "tilde.db"


def test_sqlite_storage_save_and_load(temp_db_path: Path):
    """Test saving and loading a profile with SQLite."""
    from tilde.storage import SQLiteStorage

    storage = SQLiteStorage(temp_db_path)

    profile = TildeProfile(
        user_profile=UserProfile(
            identity=Identity(name="Allen", role="SWE", years_experience=12)
        )
    )
    storage.save(profile)

    loaded = storage.load()
    assert loaded.user_profile.identity.name == "Allen"
    assert loaded.user_profile.identity.years_experience == 12


def test_sqlite_storage_exists(temp_db_path: Path):
    """Test exists() method for SQLite."""
    from tilde.storage import SQLiteStorage

    storage = SQLiteStorage(temp_db_path)
    assert not storage.exists()

    storage.save(TildeProfile())
    assert storage.exists()


def test_sqlite_storage_query(temp_db_path: Path):
    """Test querying profile fields."""
    from tilde.schema import TechStack
    from tilde.storage import SQLiteStorage

    storage = SQLiteStorage(temp_db_path)

    profile = TildeProfile(
        user_profile=UserProfile(
            identity=Identity(name="Allen"),
            tech_stack=TechStack(languages=["Python", "TypeScript"]),
        )
    )
    storage.save(profile)

    # Query languages
    results = storage.query("%languages%")
    assert len(results) >= 2
    values = [r[1] for r in results]
    assert "Python" in values
    assert "TypeScript" in values


def test_sqlite_storage_add_memory(temp_db_path: Path):
    """Test adding memories to SQLite."""
    from tilde.storage import SQLiteStorage

    storage = SQLiteStorage(temp_db_path)
    storage.save(TildeProfile())

    memory_id = storage.add_memory(
        "User prefers vim keybindings",
        source="conversation",
        category="preferences"
    )
    assert memory_id > 0


def test_sqlite_storage_search_memories(temp_db_path: Path):
    """Test searching memories."""
    from tilde.storage import SQLiteStorage

    storage = SQLiteStorage(temp_db_path)
    storage.save(TildeProfile())

    storage.add_memory("Prefers async/await patterns", category="coding")
    storage.add_memory("Uses Vim keybindings", category="editor")
    storage.add_memory("Likes async generators", category="coding")

    results = storage.search_memories("async")
    assert len(results) == 2

    results = storage.search_memories("async", category="coding")
    assert len(results) == 2


def test_sqlite_storage_update_profile(temp_db_path: Path):
    """Test updating an existing profile."""
    from tilde.storage import SQLiteStorage

    storage = SQLiteStorage(temp_db_path)

    profile1 = TildeProfile(
        user_profile=UserProfile(identity=Identity(name="Allen"))
    )
    storage.save(profile1)

    profile2 = TildeProfile(
        user_profile=UserProfile(identity=Identity(name="Updated", role="Engineer"))
    )
    storage.save(profile2)

    loaded = storage.load()
    assert loaded.user_profile.identity.name == "Updated"
    assert loaded.user_profile.identity.role == "Engineer"


def test_get_storage_backend_selection(temp_profile_path: Path):
    """Test get_storage with different backends."""
    import os
    from tilde.storage import get_storage, YAMLStorage, SQLiteStorage

    # Default should be YAML
    storage = get_storage(temp_profile_path)
    assert isinstance(storage, YAMLStorage)

    # SQLite via argument
    storage = get_storage(temp_profile_path, backend="sqlite")
    assert isinstance(storage, SQLiteStorage)

    # Via environment variable
    old_env = os.environ.get("TILDE_STORAGE")
    try:
        os.environ["TILDE_STORAGE"] = "sqlite"
        storage = get_storage(temp_profile_path)
        assert isinstance(storage, SQLiteStorage)
    finally:
        if old_env:
            os.environ["TILDE_STORAGE"] = old_env
        else:
            os.environ.pop("TILDE_STORAGE", None)

