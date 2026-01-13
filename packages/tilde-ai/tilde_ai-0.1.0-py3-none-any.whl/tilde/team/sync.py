"""Team context synchronization for tilde.

Supports syncing team context from:
- Local files (for air-gapped environments)
- HTTP URLs (for shared team configs)
- Git repositories (for version-controlled configs)
"""

import hashlib
import json
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from pydantic import BaseModel, Field

from tilde.team.manager import TeamConfig, TeamManager


class SyncResult(BaseModel):
    """Result of a sync operation."""
    
    success: bool
    team_id: str
    source: str
    message: str
    changes: list[str] = []
    synced_at: datetime = Field(default_factory=datetime.now)


class TeamSync:
    """Handles team context synchronization from various sources."""
    
    def __init__(self, manager: TeamManager):
        self.manager = manager
        self.sync_log_path = manager.team_dir / "sync_log.json"
    
    def _load_sync_log(self) -> list[dict[str, Any]]:
        """Load sync history."""
        if not self.sync_log_path.exists():
            return []
        with open(self.sync_log_path) as f:
            return json.load(f)
    
    def _save_sync_log(self, log: list[dict[str, Any]]) -> None:
        """Save sync history."""
        self.sync_log_path.parent.mkdir(parents=True, exist_ok=True)
        # Keep last 50 entries
        log = log[-50:]
        with open(self.sync_log_path, "w") as f:
            json.dump(log, f, indent=2, default=str)
    
    def _log_sync(self, result: SyncResult) -> None:
        """Log a sync operation."""
        log = self._load_sync_log()
        log.append(result.model_dump(mode="json"))
        self._save_sync_log(log)
    
    def _compute_hash(self, config: TeamConfig) -> str:
        """Compute a hash of the config for change detection."""
        data = config.model_dump_json(exclude={"updated_at"})
        return hashlib.sha256(data.encode()).hexdigest()[:12]
    
    def sync_from_file(self, path: str | Path) -> SyncResult:
        """Sync team context from a local JSON/YAML file."""
        path = Path(path)
        
        if not path.exists():
            return SyncResult(
                success=False,
                team_id="",
                source=str(path),
                message=f"File not found: {path}",
            )
        
        try:
            with open(path) as f:
                if path.suffix in [".yaml", ".yml"]:
                    import yaml
                    data = yaml.safe_load(f)
                else:
                    data = json.load(f)
            
            config = TeamConfig.model_validate(data)
            
            # Check for changes
            existing = self.manager.get_team(config.team_id)
            changes = []
            
            if existing:
                old_hash = self._compute_hash(existing)
                new_hash = self._compute_hash(config)
                if old_hash == new_hash:
                    return SyncResult(
                        success=True,
                        team_id=config.team_id,
                        source=str(path),
                        message="No changes detected",
                    )
                changes.append(f"Updated from {old_hash} to {new_hash}")
            else:
                changes.append("New team created")
            
            self.manager.save_team(config)
            
            result = SyncResult(
                success=True,
                team_id=config.team_id,
                source=str(path),
                message=f"Synced team '{config.team_name}'",
                changes=changes,
            )
            self._log_sync(result)
            return result
            
        except Exception as e:
            return SyncResult(
                success=False,
                team_id="",
                source=str(path),
                message=f"Error: {e}",
            )
    
    def sync_from_url(self, url: str) -> SyncResult:
        """Sync team context from an HTTP(S) URL."""
        try:
            import urllib.request
            
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            config = TeamConfig.model_validate(data)
            
            existing = self.manager.get_team(config.team_id)
            changes = []
            
            if existing:
                old_hash = self._compute_hash(existing)
                new_hash = self._compute_hash(config)
                if old_hash == new_hash:
                    return SyncResult(
                        success=True,
                        team_id=config.team_id,
                        source=url,
                        message="No changes detected",
                    )
                changes.append(f"Updated from {old_hash} to {new_hash}")
            else:
                changes.append("New team created")
            
            self.manager.save_team(config)
            
            result = SyncResult(
                success=True,
                team_id=config.team_id,
                source=url,
                message=f"Synced team '{config.team_name}' from URL",
                changes=changes,
            )
            self._log_sync(result)
            return result
            
        except Exception as e:
            return SyncResult(
                success=False,
                team_id="",
                source=url,
                message=f"Error: {e}",
            )
    
    def sync_from_git(self, repo_url: str, file_path: str = "tilde-team.json", branch: str = "main") -> SyncResult:
        """Sync team context from a Git repository.
        
        Clones the repo to a temp directory and reads the config file.
        """
        try:
            import subprocess
            
            with tempfile.TemporaryDirectory() as tmpdir:
                # Shallow clone
                result = subprocess.run(
                    ["git", "clone", "--depth", "1", "--branch", branch, repo_url, tmpdir],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                
                if result.returncode != 0:
                    return SyncResult(
                        success=False,
                        team_id="",
                        source=repo_url,
                        message=f"Git clone failed: {result.stderr}",
                    )
                
                config_path = Path(tmpdir) / file_path
                if not config_path.exists():
                    return SyncResult(
                        success=False,
                        team_id="",
                        source=repo_url,
                        message=f"Config file not found: {file_path}",
                    )
                
                return self.sync_from_file(config_path)
                
        except subprocess.TimeoutExpired:
            return SyncResult(
                success=False,
                team_id="",
                source=repo_url,
                message="Git clone timed out",
            )
        except FileNotFoundError:
            return SyncResult(
                success=False,
                team_id="",
                source=repo_url,
                message="Git is not installed",
            )
        except Exception as e:
            return SyncResult(
                success=False,
                team_id="",
                source=repo_url,
                message=f"Error: {e}",
            )
    
    def auto_sync(self, source: str) -> SyncResult:
        """Auto-detect source type and sync.
        
        Supports:
        - Local file paths
        - HTTP(S) URLs
        - Git repository URLs (git://, *.git)
        """
        parsed = urlparse(source)
        
        if parsed.scheme in ["http", "https"]:
            if source.endswith(".git") or "github.com" in source or "gitlab.com" in source:
                return self.sync_from_git(source)
            return self.sync_from_url(source)
        elif parsed.scheme == "git" or source.endswith(".git"):
            return self.sync_from_git(source)
        else:
            return self.sync_from_file(source)
    
    def get_sync_history(self, team_id: str | None = None, limit: int = 10) -> list[SyncResult]:
        """Get sync history, optionally filtered by team."""
        log = self._load_sync_log()
        
        if team_id:
            log = [entry for entry in log if entry.get("team_id") == team_id]
        
        results = [SyncResult.model_validate(entry) for entry in log[-limit:]]
        return list(reversed(results))


def get_team_sync(manager: TeamManager | None = None) -> TeamSync:
    """Get a TeamSync instance."""
    if manager is None:
        from tilde.team.manager import get_team_manager
        manager = get_team_manager()
    return TeamSync(manager)
