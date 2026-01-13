"""Tests for tilde updates module."""

import tempfile
from pathlib import Path

import pytest

from tilde.schema import TildeProfile
from tilde.updates import (
    PendingUpdate,
    UpdateQueue,
    apply_update_to_profile,
)


@pytest.fixture
def temp_profile_dir():
    """Create a temporary directory for profile and updates."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def update_queue(temp_profile_dir: Path) -> UpdateQueue:
    """Create an UpdateQueue with temporary storage."""
    profile_path = temp_profile_dir / "profile.yaml"
    return UpdateQueue(profile_path)


def test_propose_creates_update(update_queue: UpdateQueue):
    """Test proposing an update."""
    update_id = update_queue.propose(
        field_path="user_profile.identity.name",
        proposed_value="Allen",
        reason="User mentioned their name",
        source_agent="test",
        confidence=0.9,
    )
    
    assert len(update_id) == 8
    assert len(update_queue.list_pending()) == 1


def test_list_pending_returns_all(update_queue: UpdateQueue):
    """Test listing all pending updates."""
    update_queue.propose("field1", "value1", reason="test")
    update_queue.propose("field2", "value2", reason="test")
    update_queue.propose("field3", "value3", reason="test")
    
    pending = update_queue.list_pending()
    assert len(pending) == 3


def test_approve_removes_from_pending(update_queue: UpdateQueue):
    """Test approving an update removes it from pending."""
    update_id = update_queue.propose("field", "value", reason="test")
    
    approved = update_queue.approve(update_id)
    
    assert approved is not None
    assert approved.id == update_id
    assert len(update_queue.list_pending()) == 0


def test_approve_logs_entry(update_queue: UpdateQueue):
    """Test approving an update creates a log entry."""
    update_id = update_queue.propose("field", "value", reason="test")
    
    update_queue.approve(update_id)
    
    logs = update_queue.get_log()
    assert len(logs) == 1
    assert logs[0].status == "approved"


def test_reject_removes_from_pending(update_queue: UpdateQueue):
    """Test rejecting an update removes it from pending."""
    update_id = update_queue.propose("field", "value", reason="test")
    
    rejected = update_queue.reject(update_id)
    
    assert rejected is not None
    assert rejected.id == update_id
    assert len(update_queue.list_pending()) == 0


def test_reject_logs_entry(update_queue: UpdateQueue):
    """Test rejecting an update creates a log entry."""
    update_id = update_queue.propose("field", "value", reason="test")
    
    update_queue.reject(update_id)
    
    logs = update_queue.get_log()
    assert len(logs) == 1
    assert logs[0].status == "rejected"


def test_approve_nonexistent_returns_none(update_queue: UpdateQueue):
    """Test approving nonexistent update returns None."""
    result = update_queue.approve("nonexistent")
    assert result is None


def test_get_pending_by_id(update_queue: UpdateQueue):
    """Test getting a specific pending update."""
    update_id = update_queue.propose("field", "value", reason="test")
    
    update = update_queue.get_pending(update_id)
    
    assert update is not None
    assert update.id == update_id


def test_clear_all(update_queue: UpdateQueue):
    """Test clearing all pending updates."""
    update_queue.propose("field1", "value1", reason="test")
    update_queue.propose("field2", "value2", reason="test")
    
    count = update_queue.clear_all()
    
    assert count == 2
    assert len(update_queue.list_pending()) == 0
    # All should be logged as rejected
    assert len(update_queue.get_log()) == 2


# Tests for apply_update_to_profile


def test_apply_set_simple_field():
    """Test setting a simple field."""
    profile = {"user_profile": {"identity": {"name": ""}}}
    update = PendingUpdate(
        field_path="user_profile.identity.name",
        proposed_value="Allen",
        reason="test",
    )
    
    result = apply_update_to_profile(profile, update)
    
    assert result["user_profile"]["identity"]["name"] == "Allen"


def test_apply_set_nested_field():
    """Test setting a nested field that doesn't exist."""
    profile = {"user_profile": {}}
    update = PendingUpdate(
        field_path="user_profile.domain_knowledge.domains.finance",
        proposed_value="Expert in trading",
        reason="test",
    )
    
    result = apply_update_to_profile(profile, update)
    
    assert result["user_profile"]["domain_knowledge"]["domains"]["finance"] == "Expert in trading"


def test_apply_append_to_list():
    """Test appending to a list."""
    profile = {"user_profile": {"tech_stack": {"languages": ["Python"]}}}
    update = PendingUpdate(
        field_path="user_profile.tech_stack.languages",
        action="append",
        proposed_value="TypeScript",
        reason="test",
    )
    
    result = apply_update_to_profile(profile, update)
    
    assert "TypeScript" in result["user_profile"]["tech_stack"]["languages"]
    assert "Python" in result["user_profile"]["tech_stack"]["languages"]


def test_apply_remove_from_list():
    """Test removing from a list."""
    profile = {"user_profile": {"tech_stack": {"languages": ["Python", "Java"]}}}
    update = PendingUpdate(
        field_path="user_profile.tech_stack.languages",
        action="remove",
        proposed_value="Java",
        reason="test",
    )
    
    result = apply_update_to_profile(profile, update)
    
    assert "Java" not in result["user_profile"]["tech_stack"]["languages"]
    assert "Python" in result["user_profile"]["tech_stack"]["languages"]


def test_apply_remove_nonexistent_is_safe():
    """Test removing a nonexistent item doesn't error."""
    profile = {"user_profile": {"tech_stack": {"languages": ["Python"]}}}
    update = PendingUpdate(
        field_path="user_profile.tech_stack.languages",
        action="remove",
        proposed_value="Rust",
        reason="test",
    )
    
    # Should not raise
    result = apply_update_to_profile(profile, update)
    
    assert result["user_profile"]["tech_stack"]["languages"] == ["Python"]


def test_pending_update_display_dict():
    """Test the display format for pending updates."""
    update = PendingUpdate(
        field_path="user_profile.identity.role",
        proposed_value="Senior Engineer",
        reason="User mentioned their role",
        source_agent="claude",
        confidence=0.85,
    )
    
    display = update.to_display_dict()
    
    assert display["id"] == update.id
    assert display["field"] == "user_profile.identity.role"
    assert display["confidence"] == "85%"
    assert display["from"] == "claude"
