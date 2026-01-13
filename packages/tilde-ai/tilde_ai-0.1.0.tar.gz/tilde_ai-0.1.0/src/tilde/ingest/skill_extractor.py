"""Anthropic SKILL.md extraction for tilde.

Extracts metadata from Anthropic Claude Skills (SKILL.md format) and converts
them into tilde profile skill entries.

SKILL.md format:
---
name: skill-name
description: What the skill does
---
Markdown body with instructions...

Supports bundling of:
- scripts/ - Python scripts and utilities
- references/ or reference/ - Documentation files
- assets/ - Template files and resources
"""

import re
from pathlib import Path
from typing import Any

import yaml

from tilde.ingest.loader import Document
from tilde.updates import PendingUpdate


def parse_yaml_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter from markdown content.
    
    Args:
        content: The full markdown content
        
    Returns:
        Tuple of (frontmatter dict, body content)
    """
    # Match YAML frontmatter delimited by ---
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    
    if not match:
        return {}, content
    
    frontmatter_str = match.group(1)
    body = match.group(2)
    
    try:
        frontmatter = yaml.safe_load(frontmatter_str) or {}
    except yaml.YAMLError:
        return {}, content
    
    return frontmatter, body


def validate_skill_name(name: str) -> bool:
    """Validate skill name against Anthropic conventions.
    
    Rules:
    - Lowercase only
    - Numbers and hyphens allowed
    - Max 64 characters
    - No reserved words (anthropic, claude)
    """
    if not name:
        return False
    if len(name) > 64:
        return False
    if not re.match(r'^[a-z0-9-]+$', name):
        return False
    if any(word in name.lower() for word in ['anthropic', 'claude']):
        return False
    return True


def bundle_skill_resources(skill_dir: Path) -> dict[str, dict[str, str]]:
    """Bundle all resources from a skill directory.
    
    Args:
        skill_dir: Path to the skill directory containing SKILL.md
        
    Returns:
        Dictionary with resource type keys containing filename -> content mappings.
        Includes: scripts/, references/, assets/, templates/, and root files.
    """
    resources: dict[str, dict[str, str]] = {
        'scripts': {},
        'references': {},
        'assets': {},
        'templates': {},
        'files': {},  # Root-level files (LICENSE.txt, etc.)
    }
    
    # Known subdirectory mappings
    dir_mappings = {
        'scripts': 'scripts',
        'references': 'references',
        'reference': 'references',  # Handle both spellings
        'assets': 'assets',
        'templates': 'templates',
    }
    
    # Bundle known subdirectories
    for dir_name, resource_key in dir_mappings.items():
        subdir = skill_dir / dir_name
        if subdir.exists() and subdir.is_dir():
            for f in subdir.rglob('*'):
                if f.is_file() and not f.name.startswith('.'):
                    try:
                        rel_path = str(f.relative_to(subdir))
                        resources[resource_key][rel_path] = f.read_text(encoding='utf-8')
                    except UnicodeDecodeError:
                        # Skip binary files
                        pass
    
    # Bundle root-level files (excluding SKILL.md)
    for f in skill_dir.iterdir():
        if f.is_file() and not f.name.startswith('.'):
            # Skip SKILL.md variants
            if f.name.lower() == 'skill.md':
                continue
            try:
                resources['files'][f.name] = f.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                # Skip binary files
                pass
    
    return resources


def extract_skill_metadata(content: str, source_path: str) -> dict[str, Any] | None:
    """Extract skill metadata from SKILL.md content.
    
    Args:
        content: The SKILL.md file content
        source_path: Path to the source file (for context)
        
    Returns:
        Dictionary with skill metadata, or None if not a valid skill
    """
    frontmatter, body = parse_yaml_frontmatter(content)
    
    # Require name and description
    name = frontmatter.get('name')
    description = frontmatter.get('description')
    
    if not name or not description:
        return None
    
    # Build skill metadata
    skill_data = {
        'name': name,
        'description': description,
        'content': body.strip(),  # Full markdown body content
        'source_type': 'anthropic-skill',
        'source_path': source_path,
    }
    
    # Optional fields
    if 'tags' in frontmatter:
        skill_data['tags'] = frontmatter['tags']
    
    if 'requires' in frontmatter:
        skill_data['requires'] = frontmatter['requires']
    
    # Extract summary from first paragraph of body if short enough
    if body.strip():
        first_para = body.strip().split('\n\n')[0]
        if len(first_para) < 200:
            skill_data['summary'] = first_para
    
    return skill_data


def extract_from_skill(
    document: Document,
    visibility: str = "public",
) -> list[PendingUpdate]:
    """Extract profile updates from an Anthropic SKILL.md file.
    
    Args:
        document: The loaded skill document
        visibility: Visibility setting for the skill (public/private/team)
        
    Returns:
        List of PendingUpdate objects ready to be added to the approval queue
    """
    updates: list[PendingUpdate] = []
    
    skill_data = extract_skill_metadata(document.content, document.source)
    
    if not skill_data:
        return updates
    
    # Validate skill name
    name = skill_data['name']
    if not validate_skill_name(name):
        # Still allow but warn via lower confidence
        confidence = 0.5
    else:
        confidence = 0.9
    
    # Build the skill entry for the profile
    skill_entry = {
        'name': skill_data['name'],
        'description': skill_data.get('description'),
        'content': skill_data.get('content'),  # Full markdown body
        'visibility': visibility,
        'tags': skill_data.get('tags', []),
        'source_type': 'anthropic-skill',
    }
    
    # Add the skill to the profile
    update = PendingUpdate(
        field_path="user_profile.skills",
        action="append",
        proposed_value=skill_entry,
        reason=f"Imported from Anthropic skill: {document.source}",
        source_agent="tilde-ingest",
        confidence=confidence,
    )
    updates.append(update)
    
    return updates


def find_skill_files(directory: str | Path) -> list[Path]:
    """Find all SKILL.md files in a directory tree.
    
    Args:
        directory: Root directory to search
        
    Returns:
        List of paths to SKILL.md files (one per parent directory)
    """
    directory = Path(directory)
    skill_files = []
    
    # Look for SKILL.md files (case-insensitive)
    for pattern in ['SKILL.md', 'skill.md', 'Skill.md']:
        skill_files.extend(directory.rglob(pattern))
    
    # Deduplicate by parent directory (handles case-insensitive filesystems)
    seen_parents: set[Path] = set()
    unique_files = []
    for f in sorted(skill_files):
        if f.parent not in seen_parents:
            seen_parents.add(f.parent)
            unique_files.append(f)
    
    return unique_files


def import_skill_from_directory(
    skill_dir: Path,
    visibility: str = "public",
    bundle_resources: bool = True,
) -> dict[str, Any] | None:
    """Import a skill from a directory containing SKILL.md.
    
    Args:
        skill_dir: Path to skill directory (should contain SKILL.md)
        visibility: Visibility setting for the skill
        bundle_resources: Whether to bundle scripts/references/assets
        
    Returns:
        Skill entry dictionary ready to add to profile, or None if invalid
    """
    skill_md = skill_dir / 'SKILL.md'
    if not skill_md.exists():
        # Try lowercase
        skill_md = skill_dir / 'skill.md'
    if not skill_md.exists():
        return None
    
    content = skill_md.read_text(encoding='utf-8')
    skill_data = extract_skill_metadata(content, str(skill_md))
    
    if not skill_data:
        return None
    
    # Build the skill entry for the profile
    skill_entry = {
        'name': skill_data['name'],
        'description': skill_data.get('description'),
        'content': skill_data.get('content'),
        'visibility': visibility,
        'tags': skill_data.get('tags', []),
        'source_type': 'anthropic-skill',
        'source_path': str(skill_dir),
    }
    
    # Bundle resources if requested
    if bundle_resources:
        resources = bundle_skill_resources(skill_dir)
        # Only add non-empty resource dicts
        if resources['scripts']:
            skill_entry['scripts'] = resources['scripts']
        if resources['references']:
            skill_entry['references'] = resources['references']
        if resources['assets']:
            skill_entry['assets'] = resources['assets']
        if resources['templates']:
            skill_entry['templates'] = resources['templates']
        if resources['files']:
            skill_entry['files'] = resources['files']
    
    return skill_entry


def import_skills_from_directory(
    root_dir: str | Path,
    visibility: str = "public",
    bundle_resources: bool = True,
) -> list[dict[str, Any]]:
    """Import all skills from a directory tree.
    
    Searches for directories containing SKILL.md files and imports each one.
    
    Args:
        root_dir: Root directory to search for skills
        visibility: Default visibility for imported skills
        bundle_resources: Whether to bundle scripts/references/assets
        
    Returns:
        List of skill entry dictionaries
    """
    root_dir = Path(root_dir)
    skills = []
    
    skill_files = find_skill_files(root_dir)
    
    for skill_file in skill_files:
        skill_dir = skill_file.parent
        skill_entry = import_skill_from_directory(
            skill_dir, visibility, bundle_resources
        )
        if skill_entry:
            skills.append(skill_entry)
    
    return skills


def export_skill_to_md(skill: dict[str, Any]) -> str:
    """Export a skill entry to SKILL.md format.
    
    Args:
        skill: Skill dictionary from profile
        
    Returns:
        SKILL.md content string
    """
    # Build frontmatter
    frontmatter = {
        'name': skill.get('name', 'unnamed-skill'),
        'description': skill.get('description', 'No description'),
    }
    
    if skill.get('tags'):
        frontmatter['tags'] = skill['tags']
    
    # Convert to YAML
    yaml_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    # Build content
    body = skill.get('content', '')
    
    return f"---\n{yaml_str}---\n{body}\n"


def export_skill_to_directory(skill: dict[str, Any], output_dir: Path) -> Path:
    """Export a skill to a directory with SKILL.md and bundled resources.
    
    Args:
        skill: Skill dictionary from profile
        output_dir: Parent directory for the skill folder
        
    Returns:
        Path to the created skill directory
    """
    name = skill.get('name', 'unnamed-skill')
    skill_dir = output_dir / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    # Write SKILL.md
    skill_md = skill_dir / 'SKILL.md'
    skill_md.write_text(export_skill_to_md(skill), encoding='utf-8')
    
    # Write bundled scripts
    if skill.get('scripts'):
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        for filename, content in skill['scripts'].items():
            (scripts_dir / filename).write_text(content, encoding='utf-8')
    
    # Write bundled references
    if skill.get('references'):
        ref_dir = skill_dir / 'references'
        ref_dir.mkdir(exist_ok=True)
        for filename, content in skill['references'].items():
            (ref_dir / filename).write_text(content, encoding='utf-8')
    
    # Write bundled assets
    if skill.get('assets'):
        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        for rel_path, content in skill['assets'].items():
            asset_path = assets_dir / rel_path
            asset_path.parent.mkdir(parents=True, exist_ok=True)
            asset_path.write_text(content, encoding='utf-8')
    
    # Write bundled templates
    if skill.get('templates'):
        templates_dir = skill_dir / 'templates'
        templates_dir.mkdir(exist_ok=True)
        for rel_path, content in skill['templates'].items():
            template_path = templates_dir / rel_path
            template_path.parent.mkdir(parents=True, exist_ok=True)
            template_path.write_text(content, encoding='utf-8')
    
    # Write root-level files (LICENSE.txt, etc.)
    if skill.get('files'):
        for filename, content in skill['files'].items():
            (skill_dir / filename).write_text(content, encoding='utf-8')
    
    return skill_dir
