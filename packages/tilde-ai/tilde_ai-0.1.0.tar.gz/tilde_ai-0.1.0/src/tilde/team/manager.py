"""Team context manager for tilde."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from tilde.storage import get_default_profile_path


class TeamMember(BaseModel):
    """A team member's minimal info."""
    
    name: str
    role: str | None = None
    joined_at: datetime = Field(default_factory=datetime.now)


class TeamConfig(BaseModel):
    """Team configuration and context."""
    
    # Team identity
    team_id: str
    team_name: str
    organization: str | None = None
    
    # Coding standards
    coding_standards: str | None = None
    architecture_patterns: str | None = None
    do_not_use: list[str] = []
    preferred_tools: list[str] = []
    
    # Documentation
    conventions: dict[str, str] = {}  # e.g., {"naming": "snake_case", "commits": "conventional"}
    onboarding_notes: str | None = None
    
    # Metadata
    version: str = "1.0.0"
    updated_at: datetime = Field(default_factory=datetime.now)
    updated_by: str | None = None
    
    # Access control
    read_only_fields: list[str] = []  # Fields that members can't override locally


class TeamManager:
    """Manages team context and synchronization."""
    
    def __init__(self, profile_path: Path | None = None):
        self.profile_path = profile_path or get_default_profile_path()
        self.team_dir = self.profile_path.parent / "teams"
        self.active_team_file = self.profile_path.parent / "active_team.json"
    
    def _get_team_path(self, team_id: str) -> Path:
        """Get the path to a team's config file."""
        return self.team_dir / f"{team_id}.json"
    
    def list_teams(self) -> list[str]:
        """List all available team IDs."""
        if not self.team_dir.exists():
            return []
        return [f.stem for f in self.team_dir.glob("*.json")]
    
    def get_team(self, team_id: str) -> TeamConfig | None:
        """Get a team's configuration."""
        path = self._get_team_path(team_id)
        if not path.exists():
            return None
        
        with open(path) as f:
            data = json.load(f)
        
        return TeamConfig.model_validate(data)
    
    def save_team(self, config: TeamConfig) -> None:
        """Save a team's configuration."""
        self.team_dir.mkdir(parents=True, exist_ok=True)
        path = self._get_team_path(config.team_id)
        
        config.updated_at = datetime.now()
        
        with open(path, "w") as f:
            json.dump(config.model_dump(mode="json"), f, indent=2, default=str)
    
    def create_team(
        self,
        team_id: str,
        team_name: str,
        organization: str | None = None,
        **kwargs: Any,
    ) -> TeamConfig:
        """Create a new team configuration."""
        if self.get_team(team_id):
            raise ValueError(f"Team '{team_id}' already exists")
        
        config = TeamConfig(
            team_id=team_id,
            team_name=team_name,
            organization=organization,
            **kwargs,
        )
        self.save_team(config)
        return config
    
    def delete_team(self, team_id: str) -> bool:
        """Delete a team configuration."""
        path = self._get_team_path(team_id)
        if path.exists():
            path.unlink()
            # Deactivate if this was the active team
            if self.get_active_team_id() == team_id:
                self.deactivate_team()
            return True
        return False
    
    def get_active_team_id(self) -> str | None:
        """Get the currently active team ID."""
        if not self.active_team_file.exists():
            return None
        
        with open(self.active_team_file) as f:
            data = json.load(f)
        
        return data.get("team_id")
    
    def get_active_team(self) -> TeamConfig | None:
        """Get the currently active team configuration."""
        team_id = self.get_active_team_id()
        if team_id:
            return self.get_team(team_id)
        return None
    
    def activate_team(self, team_id: str) -> TeamConfig:
        """Set a team as the active team."""
        config = self.get_team(team_id)
        if not config:
            raise ValueError(f"Team '{team_id}' not found")
        
        self.active_team_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.active_team_file, "w") as f:
            json.dump({"team_id": team_id, "activated_at": datetime.now().isoformat()}, f)
        
        return config
    
    def deactivate_team(self) -> None:
        """Deactivate the current team."""
        if self.active_team_file.exists():
            self.active_team_file.unlink()
    
    def merge_team_context(self, profile_dict: dict[str, Any]) -> dict[str, Any]:
        """Merge active team context into a profile dictionary.
        
        Team context overrides personal team_context fields.
        """
        team = self.get_active_team()
        if not team:
            return profile_dict
        
        # Create team_context from TeamConfig
        team_context = {
            "organization": team.organization or team.team_name,
            "coding_standards": team.coding_standards,
            "architecture_patterns": team.architecture_patterns,
            "do_not_use": team.do_not_use,
        }
        
        # Remove None values
        team_context = {k: v for k, v in team_context.items() if v is not None}
        
        profile_dict["team_context"] = team_context
        return profile_dict


def get_team_manager(profile_path: Path | None = None) -> TeamManager:
    """Get a TeamManager instance."""
    import os
    
    env_path = os.environ.get("TILDE_PROFILE")
    if env_path:
        profile_path = Path(env_path)
    
    return TeamManager(profile_path)
