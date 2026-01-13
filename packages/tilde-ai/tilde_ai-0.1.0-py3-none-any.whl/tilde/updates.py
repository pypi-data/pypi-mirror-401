"""Update queue and approval flow for tilde profiles."""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from tilde.storage import get_default_profile_path


class PendingUpdate(BaseModel):
    """A proposed profile update awaiting approval."""

    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:8])
    field_path: str  # e.g., "user_profile.tech_stack.preferences"
    action: str = "set"  # "set", "append", "remove"
    proposed_value: Any
    reason: str | None = None  # Why the agent is proposing this
    source_agent: str = "unknown"
    timestamp: datetime = Field(default_factory=datetime.now)
    confidence: float = 0.5  # 0-1, how confident the agent is

    def to_display_dict(self) -> dict[str, Any]:
        """Convert to a human-readable display format."""
        return {
            "id": self.id,
            "field": self.field_path,
            "action": self.action,
            "value": self.proposed_value,
            "reason": self.reason,
            "from": self.source_agent,
            "when": self.timestamp.isoformat(),
            "confidence": f"{self.confidence:.0%}",
        }


class UpdateLog(BaseModel):
    """A log entry for an applied or rejected update."""

    update: PendingUpdate
    status: str  # "approved", "rejected"
    applied_at: datetime = Field(default_factory=datetime.now)


class UpdateQueue:
    """Manages pending profile updates with approval flow."""

    def __init__(self, profile_path: Path | None = None):
        self.profile_path = profile_path or get_default_profile_path()
        self.pending_path = self.profile_path.parent / "pending_updates.json"
        self.log_path = self.profile_path.parent / "update_log.json"

    def _load_pending(self) -> list[PendingUpdate]:
        """Load pending updates from file."""
        if not self.pending_path.exists():
            return []
        
        with open(self.pending_path) as f:
            data = json.load(f)
        
        return [PendingUpdate.model_validate(item) for item in data]

    def _save_pending(self, updates: list[PendingUpdate]) -> None:
        """Save pending updates to file."""
        self.pending_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = [update.model_dump(mode="json") for update in updates]
        with open(self.pending_path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def _load_log(self) -> list[UpdateLog]:
        """Load update log from file."""
        if not self.log_path.exists():
            return []
        
        with open(self.log_path) as f:
            data = json.load(f)
        
        return [UpdateLog.model_validate(item) for item in data]

    def _save_log(self, logs: list[UpdateLog]) -> None:
        """Save update log to file."""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = [log.model_dump(mode="json") for log in logs]
        with open(self.log_path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def _append_log(self, update: PendingUpdate, status: str) -> None:
        """Append an entry to the update log."""
        logs = self._load_log()
        logs.append(UpdateLog(update=update, status=status))
        
        # Keep only last 100 entries
        if len(logs) > 100:
            logs = logs[-100:]
        
        self._save_log(logs)

    def propose(
        self,
        field_path: str,
        proposed_value: Any,
        action: str = "set",
        reason: str | None = None,
        source_agent: str = "unknown",
        confidence: float = 0.5,
    ) -> str:
        """Propose a profile update. Returns the update ID."""
        update = PendingUpdate(
            field_path=field_path,
            action=action,
            proposed_value=proposed_value,
            reason=reason,
            source_agent=source_agent,
            confidence=confidence,
        )
        
        pending = self._load_pending()
        pending.append(update)
        self._save_pending(pending)
        
        return update.id

    def list_pending(self) -> list[PendingUpdate]:
        """List all pending updates."""
        return self._load_pending()

    def get_pending(self, update_id: str) -> PendingUpdate | None:
        """Get a specific pending update by ID."""
        for update in self._load_pending():
            if update.id == update_id:
                return update
        return None

    def approve(self, update_id: str) -> PendingUpdate | None:
        """Approve and remove an update from the queue.
        
        Returns the approved update, or None if not found.
        The caller is responsible for actually applying the update.
        """
        pending = self._load_pending()
        approved = None
        
        for i, update in enumerate(pending):
            if update.id == update_id:
                approved = pending.pop(i)
                break
        
        if approved:
            self._save_pending(pending)
            self._append_log(approved, "approved")
        
        return approved

    def reject(self, update_id: str) -> PendingUpdate | None:
        """Reject and remove an update from the queue.
        
        Returns the rejected update, or None if not found.
        """
        pending = self._load_pending()
        rejected = None
        
        for i, update in enumerate(pending):
            if update.id == update_id:
                rejected = pending.pop(i)
                break
        
        if rejected:
            self._save_pending(pending)
            self._append_log(rejected, "rejected")
        
        return rejected

    def clear_all(self) -> int:
        """Clear all pending updates. Returns count cleared."""
        pending = self._load_pending()
        count = len(pending)
        
        for update in pending:
            self._append_log(update, "rejected")
        
        self._save_pending([])
        return count

    def get_log(self, limit: int = 20) -> list[UpdateLog]:
        """Get recent update log entries."""
        logs = self._load_log()
        return logs[-limit:]


def apply_update_to_profile(profile_dict: dict[str, Any], update: PendingUpdate) -> dict[str, Any]:
    """Apply an approved update to a profile dictionary.
    
    Supports:
    - "set": Replace the value at field_path
    - "append": Append to a list at field_path
    - "remove": Remove from a list at field_path
    """
    path_parts = update.field_path.split(".")
    
    # Navigate to the parent of the target field
    current = profile_dict
    for part in path_parts[:-1]:
        if part not in current:
            current[part] = {}
        current = current[part]
    
    final_key = path_parts[-1]
    
    if update.action == "set":
        current[final_key] = update.proposed_value
    
    elif update.action == "append":
        if final_key not in current:
            current[final_key] = []
        if isinstance(current[final_key], list):
            current[final_key].append(update.proposed_value)
    
    elif update.action == "remove":
        if final_key in current and isinstance(current[final_key], list):
            try:
                current[final_key].remove(update.proposed_value)
            except ValueError:
                pass  # Item not in list, ignore
    
    return profile_dict


def get_update_queue(profile_path: Path | None = None) -> UpdateQueue:
    """Get an UpdateQueue instance."""
    import os
    
    env_path = os.environ.get("TILDE_PROFILE")
    if env_path:
        profile_path = Path(env_path)
    
    return UpdateQueue(profile_path)
