"""Tests for team management."""

import json
import tempfile
from pathlib import Path

import pytest

from tilde.team.manager import TeamConfig, TeamManager


@pytest.fixture
def temp_dir():
    """Create a temporary directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def manager(temp_dir: Path) -> TeamManager:
    """Create a TeamManager with temporary storage."""
    return TeamManager(temp_dir / "profile.yaml")


def test_create_team(manager: TeamManager):
    """Test creating a new team."""
    config = manager.create_team(
        team_id="my-team",
        team_name="My Team",
        organization="ACME Corp",
    )
    
    assert config.team_id == "my-team"
    assert config.team_name == "My Team"
    assert config.organization == "ACME Corp"


def test_create_duplicate_team_fails(manager: TeamManager):
    """Test creating duplicate team raises error."""
    manager.create_team("my-team", "Team 1")
    
    with pytest.raises(ValueError):
        manager.create_team("my-team", "Team 2")


def test_get_team(manager: TeamManager):
    """Test retrieving a team."""
    manager.create_team("test", "Test Team")
    
    config = manager.get_team("test")
    
    assert config is not None
    assert config.team_name == "Test Team"


def test_get_nonexistent_team(manager: TeamManager):
    """Test getting nonexistent team returns None."""
    config = manager.get_team("nonexistent")
    assert config is None


def test_list_teams(manager: TeamManager):
    """Test listing all teams."""
    manager.create_team("team1", "Team 1")
    manager.create_team("team2", "Team 2")
    
    teams = manager.list_teams()
    
    assert "team1" in teams
    assert "team2" in teams
    assert len(teams) == 2


def test_delete_team(manager: TeamManager):
    """Test deleting a team."""
    manager.create_team("to-delete", "Delete Me")
    assert manager.get_team("to-delete") is not None
    
    result = manager.delete_team("to-delete")
    
    assert result is True
    assert manager.get_team("to-delete") is None


def test_delete_nonexistent_team(manager: TeamManager):
    """Test deleting nonexistent team returns False."""
    result = manager.delete_team("nonexistent")
    assert result is False


def test_activate_team(manager: TeamManager):
    """Test activating a team."""
    manager.create_team("active", "Active Team")
    
    config = manager.activate_team("active")
    
    assert config.team_id == "active"
    assert manager.get_active_team_id() == "active"


def test_activate_nonexistent_team_fails(manager: TeamManager):
    """Test activating nonexistent team raises error."""
    with pytest.raises(ValueError):
        manager.activate_team("nonexistent")


def test_get_active_team(manager: TeamManager):
    """Test getting active team configuration."""
    manager.create_team("test", "Test Team")
    manager.activate_team("test")
    
    config = manager.get_active_team()
    
    assert config is not None
    assert config.team_id == "test"


def test_deactivate_team(manager: TeamManager):
    """Test deactivating a team."""
    manager.create_team("test", "Test")
    manager.activate_team("test")
    assert manager.get_active_team_id() is not None
    
    manager.deactivate_team()
    
    assert manager.get_active_team_id() is None


def test_save_team_updates_timestamp(manager: TeamManager):
    """Test saving team updates the timestamp."""
    from datetime import datetime
    
    config = manager.create_team("test", "Test")
    old_time = config.updated_at
    
    # Wait a tiny bit and save again
    config.coding_standards = "PEP8"
    manager.save_team(config)
    
    loaded = manager.get_team("test")
    assert loaded is not None
    assert loaded.coding_standards == "PEP8"


def test_merge_team_context(manager: TeamManager):
    """Test merging team context into profile."""
    manager.create_team(
        "test",
        "Test Team",
        organization="ACME",
        coding_standards="PEP8 strict",
        do_not_use=["eval", "exec"],
    )
    manager.activate_team("test")
    
    profile = {"user_profile": {}, "team_context": None}
    
    merged = manager.merge_team_context(profile)
    
    assert merged["team_context"]["organization"] == "ACME"
    assert merged["team_context"]["coding_standards"] == "PEP8 strict"
    assert "eval" in merged["team_context"]["do_not_use"]


def test_merge_team_context_no_active(manager: TeamManager):
    """Test merging returns unchanged profile when no active team."""
    profile = {"user_profile": {}, "team_context": None}
    
    merged = manager.merge_team_context(profile)
    
    assert merged["team_context"] is None


def test_team_config_with_all_fields():
    """Test TeamConfig with all fields populated."""
    config = TeamConfig(
        team_id="full-team",
        team_name="Full Team",
        organization="Big Corp",
        coding_standards="Strict TypeScript, no any",
        architecture_patterns="Microservices, event-driven",
        do_not_use=["jQuery", "var keyword"],
        preferred_tools=["VSCode", "Docker"],
        conventions={"naming": "camelCase", "commits": "conventional"},
        onboarding_notes="Read the wiki first",
    )
    
    assert len(config.do_not_use) == 2
    assert config.conventions["naming"] == "camelCase"
