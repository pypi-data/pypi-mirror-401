"""CLI for tilde profile management."""

import subprocess
import sys
from pathlib import Path

import typer
from rich import print as rprint
from rich.console import Console
from rich.syntax import Syntax

from tilde.schema import TildeProfile
from tilde.storage import get_storage

app = typer.Typer(
    name="tilde",
    help="Local-first MCP profile server for AI agents.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def init(
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing profile"),
) -> None:
    """Initialize a new tilde profile."""
    storage = get_storage()

    if storage.exists() and not force:
        rprint(f"[yellow]Profile already exists at {storage.path}[/yellow]")
        rprint("Use --force to overwrite.")
        raise typer.Exit(1)

    # Create default profile
    profile = TildeProfile()
    storage.save(profile)

    rprint(f"[green]✓[/green] Created profile at [cyan]{storage.path}[/cyan]")
    rprint("\nEdit your profile with:")
    rprint(f"  [dim]tilde edit[/dim]")


@app.command()
def show(
    section: str = typer.Argument(None, help="Section to show: identity, tech_stack, domains, team, skills"),
    full: bool = typer.Option(False, "--full", "-f", help="Show full content without truncation"),
) -> None:
    """Display the current profile."""
    storage = get_storage()

    if not storage.exists():
        rprint("[red]No profile found.[/red] Run [cyan]tilde init[/cyan] first.")
        raise typer.Exit(1)

    profile = storage.load()

    # Get the relevant data
    if section is None:
        data = profile.model_dump(exclude_none=True)
    elif section == "identity":
        data = profile.user_profile.identity.model_dump(exclude_none=True)
    elif section == "tech_stack":
        data = profile.user_profile.tech_stack.model_dump(exclude_none=True)
    elif section == "domains":
        data = profile.user_profile.knowledge.model_dump(exclude_none=True)
    elif section == "skills":
        data = {"skills": [s.model_dump(exclude_none=True) for s in profile.user_profile.skills]}
    elif section == "team":
        if profile.team_context:
            data = profile.team_context.model_dump(exclude_none=True)
        else:
            data = {}
    else:
        rprint(f"[red]Unknown section: {section}[/red]")
        rprint("Valid sections: identity, tech_stack, domains, skills, team")
        raise typer.Exit(1)

    # Truncate large fields unless --full is specified
    if not full:
        data = _truncate_for_display(data)

    # Pretty print as YAML-like output
    import yaml

    yaml_str = yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)
    syntax = Syntax(yaml_str, "yaml", theme="monokai", line_numbers=False)
    console.print(syntax)


def _truncate_for_display(data: dict, max_len: int = 100) -> dict:
    """Truncate large string fields for display."""
    # Fields that should be truncated when too long
    truncate_fields = {'content', 'scripts', 'references', 'assets', 'templates', 'files'}
    
    def truncate(obj):
        if isinstance(obj, dict):
            result = {}
            for k, v in obj.items():
                if k in truncate_fields:
                    if isinstance(v, str) and len(v) > max_len:
                        result[k] = v[:max_len] + f"... ({len(v)} chars)"
                    elif isinstance(v, dict):
                        # For scripts/references/assets dicts, just show keys
                        result[k] = f"[{len(v)} files: {', '.join(list(v.keys())[:3])}{'...' if len(v) > 3 else ''}]"
                    else:
                        result[k] = v
                else:
                    result[k] = truncate(v)
            return result
        elif isinstance(obj, list):
            return [truncate(item) for item in obj]
        else:
            return obj
    
    return truncate(data)


@app.command()
def edit() -> None:
    """Open the profile in your default editor."""
    storage = get_storage()

    if not storage.exists():
        rprint("[yellow]No profile found. Creating one...[/yellow]")
        profile = TildeProfile()
        storage.save(profile)

    # Get editor from environment
    import os

    editor = os.environ.get("EDITOR", "vim")

    rprint(f"Opening {storage.path} in {editor}...")
    subprocess.run([editor, str(storage.path)])


@app.command()
def export(
    format: str = typer.Option("json", "--format", "-f", help="Export format: json or yaml"),
) -> None:
    """Export the profile to stdout."""
    storage = get_storage()

    if not storage.exists():
        rprint("[red]No profile found.[/red]", file=sys.stderr)
        raise typer.Exit(1)

    profile = storage.load()

    if format == "json":
        print(profile.model_dump_json(indent=2, exclude_none=True))
    elif format == "yaml":
        import yaml

        data = profile.model_dump(exclude_none=True)
        print(yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False))
    else:
        rprint(f"[red]Unknown format: {format}[/red]", file=sys.stderr)
        raise typer.Exit(1)


@app.command()
def path() -> None:
    """Show the profile path."""
    storage = get_storage()
    print(storage.path)


@app.command()
def ingest(
    document_path: str = typer.Argument(..., help="Path to document (PDF, EPUB, TXT, MD)"),
    topic: str = typer.Option(None, "--topic", "-t", help="Topic hint for extraction"),
    doc_type: str = typer.Option(None, "--type", help="Document type: book, resume, paper, notes"),
    model: str = typer.Option(None, "--model", "-m", help="LLM model (default: from config)"),
    auto_approve: float = typer.Option(None, "--auto-approve", help="Auto-approve updates above this confidence (0-1)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be extracted without saving"),
) -> None:
    """Ingest a document and extract profile updates.
    
    Processes a book, paper, or document to extract insights that can be added
    to your profile. Updates are queued for approval unless --auto-approve is set.
    
    Use --type resume for resumes/CVs to extract experience, education, skills, etc.
    Use --type skill for Anthropic SKILL.md files to import agent skills.
    
    Requires GOOGLE_API_KEY environment variable (or OPENAI_API_KEY as fallback).
    Configure default model with TILDE_LLM_MODEL environment variable.
    """
    from rich.progress import Progress, SpinnerColumn, TextColumn

    from tilde.ingest.loader import load_document
    from tilde.updates import get_update_queue

    # Load document
    rprint(f"[dim]Loading document:[/dim] {document_path}")
    try:
        doc = load_document(document_path)
    except FileNotFoundError:
        rprint(f"[red]File not found:[/red] {document_path}")
        raise typer.Exit(1)
    except ImportError as e:
        rprint(f"[red]Missing dependency:[/red] {e}")
        raise typer.Exit(1)
    except ValueError as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    rprint(f"[dim]Document loaded:[/dim] {doc.title} ({len(doc.content):,} chars)")

    # Extract updates - use resume extractor if type is resume
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        if doc_type == "resume":
            progress.add_task("Extracting resume data...", total=None)
            from tilde.ingest.resume_extractor import extract_from_resume
            try:
                updates = extract_from_resume(doc, model)
            except RuntimeError as e:
                rprint(f"[red]Error:[/red] {e}")
                raise typer.Exit(1)
        elif doc_type == "skill":
            progress.add_task("Extracting skill metadata...", total=None)
            from tilde.ingest.skill_extractor import extract_from_skill
            updates = extract_from_skill(doc)
        else:
            progress.add_task("Extracting profile insights...", total=None)
            from tilde.ingest.extractor import extract_profile_updates
            try:
                updates = extract_profile_updates(doc, topic, model)
            except RuntimeError as e:
                rprint(f"[red]Error:[/red] {e}")
                raise typer.Exit(1)

    if not updates:
        rprint("[yellow]No profile updates could be extracted from this document.[/yellow]")
        return

    rprint(f"\n[green]Found {len(updates)} potential updates:[/green]\n")

    # Display updates
    from rich.table import Table

    table = Table()
    table.add_column("Field", style="green")
    table.add_column("Action")
    table.add_column("Value")
    table.add_column("Confidence")

    for u in updates:
        value_str = str(u.proposed_value)
        if len(value_str) > 50:
            value_str = value_str[:47] + "..."
        table.add_row(
            u.field_path,
            u.action,
            value_str,
            f"{u.confidence:.0%}",
        )

    console.print(table)

    if dry_run:
        rprint("\n[dim]Dry run - no updates saved.[/dim]")
        return

    # Queue updates
    queue = get_update_queue()
    approved_count = 0
    
    for update in updates:
        update_id = queue.propose(
            field_path=update.field_path,
            proposed_value=update.proposed_value,
            action=update.action,
            reason=update.reason,
            source_agent=update.source_agent,
            confidence=update.confidence,
        )
        
        if auto_approve is not None and update.confidence >= auto_approve:
            from tilde.updates import apply_update_to_profile
            
            queue.approve(update_id)
            storage = get_storage()
            profile = storage.load()
            profile_dict = profile.model_dump()
            updated_dict = apply_update_to_profile(profile_dict, update)
            updated_profile = TildeProfile.model_validate(updated_dict)
            storage.save(updated_profile)
            approved_count += 1

    pending_count = len(updates) - approved_count
    
    if approved_count > 0:
        rprint(f"\n[green]✓ Auto-approved {approved_count} high-confidence updates[/green]")
    
    if pending_count > 0:
        rprint(f"[cyan]→ {pending_count} updates pending approval[/cyan]")
        rprint("[dim]Run[/dim] tilde pending [dim]to review[/dim]")


@app.command()
def serve() -> None:
    """Start the MCP server (for debugging)."""
    from tilde.server import main as server_main

    server_main()


@app.command()
def config(
    save: bool = typer.Option(False, "--save", "-s", help="Save current settings to config file"),
    set_value: list[str] = typer.Option(None, "--set", help="Set a config value (format: key=value)"),
    show_path: bool = typer.Option(False, "--path", "-p", help="Show config file path only"),
) -> None:
    """Show or modify tilde configuration.
    
    Configuration is loaded from ~/.tilde/config.yaml and can be overridden
    via environment variables.
    
    Examples:
        tilde config                    # Show current config
        tilde config --save             # Save current settings to file
        tilde config --set llm_model=gemini-1.5-pro
        tilde config --set llm_model=gemini-1.5-pro --save
    
    Environment variables (override file settings):
        GOOGLE_API_KEY: Google/Gemini API key (primary)
        OPENAI_API_KEY: OpenAI API key (fallback)
        TILDE_LLM_MODEL: Override LLM model
        TILDE_EMBEDDING_MODEL: Override embedding model
        TILDE_STORAGE: Storage backend (yaml, sqlite, mem0)
    """
    from rich.panel import Panel
    from rich.table import Table

    from tilde.config import (
        CONFIG_FILE_PATH,
        get_config,
        load_config_file,
        reset_config,
        save_config,
    )

    # Just show path if requested
    if show_path:
        print(CONFIG_FILE_PATH)
        return

    # Reset cache to pick up any changes
    reset_config()
    
    # Apply --set values if provided
    if set_value:
        file_config = load_config_file()
        for item in set_value:
            if "=" not in item:
                rprint(f"[red]Invalid format:[/red] {item}")
                rprint("[dim]Use: --set key=value[/dim]")
                raise typer.Exit(1)
            key, value = item.split("=", 1)
            
            # Validate key
            valid_keys = ["llm_model", "llm_temperature", "embedding_model", 
                         "embedding_dimensions", "storage_backend"]
            if key not in valid_keys:
                rprint(f"[red]Unknown config key:[/red] {key}")
                rprint(f"[dim]Valid keys: {', '.join(valid_keys)}[/dim]")
                raise typer.Exit(1)
            
            # Convert types
            if key in ["llm_temperature"]:
                value = float(value)
            elif key in ["embedding_dimensions"]:
                value = int(value)
            
            file_config[key] = value
            rprint(f"[green]✓[/green] Set {key} = {value}")
        
        # Save if --set was used (even without --save)
        if save or set_value:
            from tilde.config import TildeConfig
            
            cfg = TildeConfig(**file_config)
            saved_path = save_config(cfg)
            rprint(f"[green]✓[/green] Saved to [cyan]{saved_path}[/cyan]")
            reset_config()
            return

    # Get current config
    try:
        cfg = get_config()
        provider = cfg.provider
        api_key_status = "[green]✓ Set[/green]"
    except RuntimeError:
        from tilde.config import TildeConfig
        cfg = TildeConfig()
        provider = "[red]Not configured[/red]"
        api_key_status = "[red]✗ Missing[/red]"

    # Check if config file exists
    config_file_exists = CONFIG_FILE_PATH.exists()
    config_file_status = "[green]exists[/green]" if config_file_exists else "[dim]not created[/dim]"

    # Build configuration table
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Key", style="cyan")
    table.add_column("Value")

    table.add_row("Provider", provider)
    table.add_row("API Key", api_key_status)
    table.add_row("", "")
    table.add_row("LLM Model", cfg.llm_model)
    table.add_row("LLM Temperature", str(cfg.llm_temperature))
    table.add_row("Embedding Model", cfg.embedding_model)
    table.add_row("Embedding Dimensions", str(cfg.embedding_dimensions))
    table.add_row("", "")
    
    # Storage info
    storage = get_storage()
    table.add_row("Storage Backend", cfg.storage_backend)
    table.add_row("Storage Path", str(storage.path))
    table.add_row("", "")
    table.add_row("Config File", str(CONFIG_FILE_PATH))
    table.add_row("Config File Status", config_file_status)

    panel = Panel(
        table,
        title="[bold]tilde Configuration[/bold]",
        border_style="blue",
    )
    console.print(panel)

    # Show save hint if no config file
    if not config_file_exists:
        rprint("\n[dim]Save current settings with:[/dim] tilde config --save")

    # Show environment variable hints if API key is missing
    if provider == "[red]Not configured[/red]":
        rprint("\n[yellow]⚠ No API key configured.[/yellow]")
        rprint("[dim]Set one of these environment variables:[/dim]")
        rprint("  export GOOGLE_API_KEY='your-key'  [dim]# Primary[/dim]")
        rprint("  export OPENAI_API_KEY='your-key'  [dim]# Fallback[/dim]")
    
    # Handle --save without --set
    if save and not set_value:
        saved_path = save_config(cfg)
        rprint(f"\n[green]✓[/green] Saved configuration to [cyan]{saved_path}[/cyan]")


@app.command()
def pending() -> None:
    """List pending profile updates from agents."""
    from rich.table import Table

    from tilde.updates import get_update_queue

    queue = get_update_queue()
    updates = queue.list_pending()

    if not updates:
        rprint("[dim]No pending updates.[/dim]")
        return

    table = Table(title="Pending Updates")
    table.add_column("ID", style="cyan")
    table.add_column("Field", style="green")
    table.add_column("Action")
    table.add_column("Value")
    table.add_column("Reason", style="dim")
    table.add_column("Confidence")

    for u in updates:
        value_str = str(u.proposed_value)
        if len(value_str) > 30:
            value_str = value_str[:27] + "..."
        
        table.add_row(
            u.id,
            u.field_path,
            u.action,
            value_str,
            u.reason or "",
            f"{u.confidence:.0%}",
        )

    console.print(table)
    rprint("\n[dim]Use[/dim] tilde approve <id> [dim]or[/dim] tilde reject <id>")


@app.command()
def approve(
    update_ids: list[str] = typer.Argument(None, help="ID(s) of update(s) to approve"),
    all_updates: bool = typer.Option(False, "--all", "-a", help="Approve all pending updates"),
    exclude_id: str = typer.Option(None, "--except", "-e", help="Exclude an ID when using --all"),
) -> None:
    """Approve pending update(s) and apply to your profile.
    
    Examples:
        tilde approve abc123              # Approve one
        tilde approve abc123 def456       # Approve multiple
        tilde approve --all               # Approve all
        tilde approve --all --except abc  # Approve all except one
    """
    from tilde.updates import apply_update_to_profile, get_update_queue

    queue = get_update_queue()

    # Validate arguments
    if not all_updates and not update_ids:
        rprint("[red]Provide update ID(s) or use --all[/red]")
        raise typer.Exit(1)
    
    if exclude_id and not all_updates:
        rprint("[red]--except can only be used with --all[/red]")
        raise typer.Exit(1)

    storage = get_storage()
    
    if all_updates:
        updates = queue.list_pending()
        if not updates:
            rprint("[dim]No pending updates.[/dim]")
            return

        # Validate excluded ID
        exclude_update = None
        if exclude_id:
            exclude_update = next((u for u in updates if u.id == exclude_id), None)
            if not exclude_update:
                rprint(f"[red]Update '{exclude_id}' not found.[/red]")
                raise typer.Exit(1)

        approved_count = 0
        for update in updates:
            if exclude_id and update.id == exclude_id:
                continue
            approved = queue.approve(update.id)
            if approved:
                profile = storage.load()
                profile_dict = profile.model_dump()
                updated_dict = apply_update_to_profile(profile_dict, approved)
                updated_profile = TildeProfile.model_validate(updated_dict)
                storage.save(updated_profile)
                approved_count += 1

        rprint(f"[green]✓[/green] Approved {approved_count} updates")
        if exclude_update:
            rprint(f"[dim]Excluded:[/dim] [cyan]{exclude_id}[/cyan] ({exclude_update.field_path})")
    else:
        # Approve specific IDs
        for update_id in update_ids:
            update = queue.approve(update_id)
            if not update:
                rprint(f"[red]Update '{update_id}' not found.[/red]")
                continue

            profile = storage.load()
            profile_dict = profile.model_dump()
            updated_dict = apply_update_to_profile(profile_dict, update)
            updated_profile = TildeProfile.model_validate(updated_dict)
            storage.save(updated_profile)

            rprint(f"[green]✓[/green] Approved [cyan]{update_id}[/cyan] ({update.field_path})")


@app.command()
def reject(
    update_ids: list[str] = typer.Argument(None, help="ID(s) of update(s) to reject"),
    all_updates: bool = typer.Option(False, "--all", "-a", help="Reject all pending updates"),
    exclude_id: str = typer.Option(None, "--except", "-e", help="Exclude an ID when using --all"),
) -> None:
    """Reject pending update(s).
    
    Examples:
        tilde reject abc123              # Reject one
        tilde reject abc123 def456       # Reject multiple
        tilde reject --all               # Reject all
        tilde reject --all --except abc  # Reject all except one
    """
    from tilde.updates import get_update_queue

    queue = get_update_queue()

    # Validate arguments
    if not all_updates and not update_ids:
        rprint("[red]Provide update ID(s) or use --all[/red]")
        raise typer.Exit(1)
    
    if exclude_id and not all_updates:
        rprint("[red]--except can only be used with --all[/red]")
        raise typer.Exit(1)

    if all_updates:
        updates = queue.list_pending()
        if not updates:
            rprint("[dim]No pending updates.[/dim]")
            return

        # Validate excluded ID
        exclude_update = None
        if exclude_id:
            exclude_update = next((u for u in updates if u.id == exclude_id), None)
            if not exclude_update:
                rprint(f"[red]Update '{exclude_id}' not found.[/red]")
                raise typer.Exit(1)

        rejected_count = 0
        for update in updates:
            if exclude_id and update.id == exclude_id:
                continue
            if queue.reject(update.id):
                rejected_count += 1

        rprint(f"[yellow]✗[/yellow] Rejected {rejected_count} updates")
        if exclude_update:
            rprint(f"[dim]Kept:[/dim] [cyan]{exclude_id}[/cyan] ({exclude_update.field_path})")
    else:
        # Reject specific IDs
        for update_id in update_ids:
            update = queue.reject(update_id)
            if not update:
                rprint(f"[red]Update '{update_id}' not found.[/red]")
                continue
            rprint(f"[yellow]✗[/yellow] Rejected [cyan]{update_id}[/cyan] ({update.field_path})")


@app.command()
def log(
    limit: int = typer.Option(10, "--limit", "-n", help="Number of entries to show"),
) -> None:
    """Show recent update history."""
    from rich.table import Table

    from tilde.updates import get_update_queue

    queue = get_update_queue()
    entries = queue.get_log(limit)

    if not entries:
        rprint("[dim]No update history.[/dim]")
        return

    table = Table(title="Update History")
    table.add_column("Time", style="dim")
    table.add_column("Status")
    table.add_column("Field", style="green")
    table.add_column("Value")
    table.add_column("Agent", style="dim")

    for entry in reversed(entries):
        u = entry.update
        value_str = str(u.proposed_value)
        if len(value_str) > 25:
            value_str = value_str[:22] + "..."
        
        status_style = "green" if entry.status == "approved" else "red"
        
        table.add_row(
            entry.applied_at.strftime("%m/%d %H:%M"),
            f"[{status_style}]{entry.status}[/{status_style}]",
            u.field_path,
            value_str,
            u.source_agent,
        )

    console.print(table)


# =============================================================================
# Skills Commands
# =============================================================================

skills_app = typer.Typer(help="Import and export Anthropic skills.")
app.add_typer(skills_app, name="skills")


@skills_app.command("import")
def skills_import(
    directory: str = typer.Argument(..., help="Directory containing skills (each skill in subfolder with SKILL.md)"),
    name: list[str] = typer.Option(None, "--name", "-n", help="Import only specific skill(s) by name"),
    visibility: str = typer.Option("public", "--visibility", "-v", help="Visibility: public, private, team"),
    no_bundle: bool = typer.Option(False, "--no-bundle", help="Don't bundle scripts/references/assets"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be imported without saving"),
) -> None:
    """Import Anthropic skills from a directory.
    
    Scans the directory for skill folders containing SKILL.md files.
    Skills are imported directly to your profile, deduplicating by name.
    
    Examples:
        tilde skills import /path/to/skills              # Import all
        tilde skills import /path/to/skills -n mcp-builder  # Import one
        tilde skills import ./skills -n docx -n pdf      # Import specific
        tilde skills import ./my-skills --visibility private
    """
    from pathlib import Path

    from rich.table import Table

    from tilde.ingest.skill_extractor import import_skills_from_directory
    from tilde.schema import Skill

    directory_path = Path(directory)
    if not directory_path.exists():
        rprint(f"[red]Directory not found:[/red] {directory}")
        raise typer.Exit(1)

    rprint(f"[dim]Scanning for skills in:[/dim] {directory}")
    
    skills = import_skills_from_directory(
        directory_path,
        visibility=visibility,
        bundle_resources=not no_bundle,
    )

    if not skills:
        rprint("[yellow]No valid skills found in directory.[/yellow]")
        return

    # Filter by name if specified
    if name:
        name_set = set(name)
        skills = [s for s in skills if s['name'] in name_set]
        if not skills:
            rprint(f"[yellow]No skills matching:[/yellow] {', '.join(name)}")
            return

    rprint(f"\n[green]Found {len(skills)} skills:[/green]\n")

    # Display skills table
    table = Table()
    table.add_column("Name", style="cyan")
    table.add_column("Description")
    table.add_column("Bundled Resources")

    for skill in skills:
        desc = skill.get('description', '')
        if len(desc) > 50:
            desc = desc[:47] + "..."
        
        # Count all bundled resources
        resource_parts = []
        if skill.get('scripts'):
            resource_parts.append(f"{len(skill['scripts'])} scripts")
        if skill.get('references'):
            resource_parts.append(f"{len(skill['references'])} refs")
        if skill.get('templates'):
            resource_parts.append(f"{len(skill['templates'])} templates")
        if skill.get('files'):
            resource_parts.append(f"{len(skill['files'])} files")
        if skill.get('assets'):
            resource_parts.append(f"{len(skill['assets'])} assets")
        
        resources_str = ", ".join(resource_parts) if resource_parts else "-"
        
        table.add_row(skill['name'], desc, resources_str)

    console.print(table)

    if dry_run:
        rprint("\n[dim]Dry run - no skills imported.[/dim]")
        return

    # Load profile and deduplicate
    storage = get_storage()
    
    if not storage.exists():
        rprint("[yellow]No profile found. Creating one...[/yellow]")
        from tilde.schema import TildeProfile
        profile = TildeProfile()
    else:
        profile = storage.load()

    # Get existing skill names
    existing_names = {s.name for s in profile.user_profile.skills}
    
    imported_count = 0
    updated_count = 0
    
    for skill_data in skills:
        skill_name = skill_data['name']
        
        # Build full skill dict with extra fields for pydantic
        skill_dict = {
            'name': skill_name,
            'description': skill_data.get('description'),
            'visibility': visibility,
            'tags': skill_data.get('tags', []),
            'source_type': 'anthropic-skill',
            'source_path': skill_data.get('source_path', ''),
        }
        
        # Add bundled resources as extra fields
        if skill_data.get('content'):
            skill_dict['content'] = skill_data['content']
        if skill_data.get('scripts'):
            skill_dict['scripts'] = skill_data['scripts']
        if skill_data.get('references'):
            skill_dict['references'] = skill_data['references']
        if skill_data.get('assets'):
            skill_dict['assets'] = skill_data['assets']
        if skill_data.get('templates'):
            skill_dict['templates'] = skill_data['templates']
        if skill_data.get('files'):
            skill_dict['files'] = skill_data['files']
        
        # Create Skill object with all fields
        skill_obj = Skill.model_validate(skill_dict)
        
        if skill_name in existing_names:
            # Update existing skill (find and replace)
            for i, existing in enumerate(profile.user_profile.skills):
                if existing.name == skill_name:
                    profile.user_profile.skills[i] = skill_obj
                    updated_count += 1
                    break
        else:
            profile.user_profile.skills.append(skill_obj)
            existing_names.add(skill_name)
            imported_count += 1

    storage.save(profile)

    if imported_count > 0:
        rprint(f"\n[green]✓[/green] Imported {imported_count} new skills")
    if updated_count > 0:
        rprint(f"[cyan]↻[/cyan] Updated {updated_count} existing skills")


@skills_app.command("export")
def skills_export(
    output_dir: str = typer.Argument(..., help="Output directory for skills"),
    visibility: str = typer.Option(None, "--visibility", "-v", help="Filter by visibility: public, private, team"),
    name: str = typer.Option(None, "--name", "-n", help="Export only a specific skill by name"),
) -> None:
    """Export profile skills to Anthropic SKILL.md format.
    
    Creates a directory structure with one folder per skill, containing
    SKILL.md and any bundled scripts/references/assets.
    
    Examples:
        tilde skills export ./my-exported-skills
        tilde skills export ./public-only --visibility public
        tilde skills export ./single --name code-review-assistant
    """
    from pathlib import Path

    from tilde.ingest.skill_extractor import export_skill_to_directory

    output_path = Path(output_dir)

    storage = get_storage()
    
    if not storage.exists():
        rprint("[red]No profile found.[/red] Run [cyan]tilde init[/cyan] first.")
        raise typer.Exit(1)

    profile = storage.load()
    skills = profile.user_profile.skills

    if not skills:
        rprint("[yellow]No skills in profile to export.[/yellow]")
        return

    # Filter by visibility
    if visibility:
        skills = [s for s in skills if s.visibility == visibility]
        if not skills:
            rprint(f"[yellow]No skills with visibility '{visibility}'.[/yellow]")
            return

    # Filter by name
    if name:
        skills = [s for s in skills if s.name == name]
        if not skills:
            rprint(f"[red]Skill '{name}' not found.[/red]")
            raise typer.Exit(1)

    rprint(f"[dim]Exporting {len(skills)} skills to:[/dim] {output_dir}")
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    exported = []
    for skill in skills:
        # Convert Skill model to dict for export
        skill_dict = skill.model_dump()
        skill_path = export_skill_to_directory(skill_dict, output_path)
        exported.append((skill.name, skill_path))
    
    rprint(f"\n[green]✓[/green] Exported {len(exported)} skills:\n")
    for skill_name, skill_path in exported:
        rprint(f"  [cyan]{skill_name}[/cyan] → {skill_path}")


@skills_app.command("list")
def skills_list(
    visibility: str = typer.Option(None, "--visibility", "-v", help="Filter by visibility"),
) -> None:
    """List all skills in your profile."""
    from rich.table import Table

    storage = get_storage()
    
    if not storage.exists():
        rprint("[red]No profile found.[/red] Run [cyan]tilde init[/cyan] first.")
        raise typer.Exit(1)

    profile = storage.load()
    skills = profile.user_profile.skills

    if not skills:
        rprint("[dim]No skills in profile.[/dim]")
        rprint("[dim]Import skills with:[/dim] tilde skills import <directory>")
        return

    # Filter by visibility if specified
    if visibility:
        skills = [s for s in skills if s.visibility == visibility]
        if not skills:
            rprint(f"[yellow]No skills with visibility '{visibility}'.[/yellow]")
            return

    table = Table(title=f"Skills ({len(skills)})")
    table.add_column("Name", style="cyan")
    table.add_column("Description")
    table.add_column("Visibility")
    table.add_column("Tags")

    for skill in skills:
        desc = skill.description or ""
        if len(desc) > 40:
            desc = desc[:37] + "..."
        tags = ", ".join(skill.tags[:3]) if skill.tags else ""
        if len(skill.tags) > 3:
            tags += f" (+{len(skill.tags) - 3})"
        table.add_row(
            skill.name,
            desc,
            skill.visibility,
            tags,
        )

    console.print(table)


@skills_app.command("delete")
def skills_delete(
    names: list[str] = typer.Argument(None, help="Name(s) of skill(s) to delete"),
    all_skills: bool = typer.Option(False, "--all", "-a", help="Delete all skills"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
) -> None:
    """Delete skill(s) from your profile.
    
    Examples:
        tilde skills delete mcp-builder
        tilde skills delete docx pdf xlsx
        tilde skills delete --all
    """
    storage = get_storage()
    
    if not storage.exists():
        rprint("[red]No profile found.[/red] Run [cyan]tilde init[/cyan] first.")
        raise typer.Exit(1)

    # Validate arguments
    if not all_skills and not names:
        rprint("[red]Provide skill name(s) or use --all[/red]")
        raise typer.Exit(1)

    profile = storage.load()
    skills = profile.user_profile.skills

    if not skills:
        rprint("[dim]No skills in profile.[/dim]")
        return

    if all_skills:
        to_delete = list(skills)
    else:
        # Find skills to delete
        skill_names = {s.name for s in skills}
        to_delete = [s for s in skills if s.name in names]
        
        # Check for unknown names
        unknown = set(names) - skill_names
        if unknown:
            rprint(f"[red]Skills not found:[/red] {', '.join(unknown)}")
            if not to_delete:
                raise typer.Exit(1)

    if not to_delete:
        rprint("[yellow]No skills to delete.[/yellow]")
        return

    # Confirmation
    if not force:
        rprint(f"[yellow]Will delete {len(to_delete)} skill(s):[/yellow]")
        for skill in to_delete:
            rprint(f"  • {skill.name}")
        confirm = typer.confirm("Continue?")
        if not confirm:
            rprint("[dim]Cancelled.[/dim]")
            return

    # Delete skills
    delete_names = {s.name for s in to_delete}
    profile.user_profile.skills = [s for s in skills if s.name not in delete_names]
    storage.save(profile)

    rprint(f"[yellow]✗[/yellow] Deleted {len(to_delete)} skill(s)")


# =============================================================================
# Team Commands
# =============================================================================

team_app = typer.Typer(help="Manage team context.")
app.add_typer(team_app, name="team")


@team_app.command("create")
def team_create(
    team_id: str = typer.Argument(..., help="Unique team identifier"),
    name: str = typer.Option(..., "--name", "-n", help="Team display name"),
    org: str = typer.Option(None, "--org", "-o", help="Organization name"),
) -> None:
    """Create a new team configuration."""
    from tilde.team.manager import get_team_manager

    manager = get_team_manager()
    
    try:
        config = manager.create_team(team_id, name, org)
        rprint(f"[green]✓[/green] Created team [cyan]{team_id}[/cyan]")
        rprint(f"  [dim]Name:[/dim] {config.team_name}")
        if config.organization:
            rprint(f"  [dim]Organization:[/dim] {config.organization}")
        rprint(f"\n[dim]Activate with:[/dim] tilde team activate {team_id}")
    except ValueError as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@team_app.command("list")
def team_list() -> None:
    """List all available teams."""
    from rich.table import Table

    from tilde.team.manager import get_team_manager

    manager = get_team_manager()
    teams = manager.list_teams()
    active_id = manager.get_active_team_id()

    if not teams:
        rprint("[dim]No teams configured.[/dim]")
        rprint("[dim]Create one with:[/dim] tilde team create <id> --name 'Team Name'")
        return

    table = Table(title="Teams")
    table.add_column("ID", style="cyan")
    table.add_column("Name")
    table.add_column("Organization", style="dim")
    table.add_column("Active")

    for team_id in teams:
        config = manager.get_team(team_id)
        if config:
            is_active = "✓" if team_id == active_id else ""
            table.add_row(
                team_id,
                config.team_name,
                config.organization or "",
                f"[green]{is_active}[/green]",
            )

    console.print(table)


@team_app.command("show")
def team_show(
    team_id: str = typer.Argument(None, help="Team ID (default: active team)"),
) -> None:
    """Show team configuration."""
    import yaml

    from tilde.team.manager import get_team_manager

    manager = get_team_manager()
    
    if team_id is None:
        team_id = manager.get_active_team_id()
        if not team_id:
            rprint("[yellow]No active team. Specify a team ID or activate one.[/yellow]")
            raise typer.Exit(1)

    config = manager.get_team(team_id)
    if not config:
        rprint(f"[red]Team '{team_id}' not found.[/red]")
        raise typer.Exit(1)

    data = config.model_dump(exclude_none=True)
    yaml_str = yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)
    syntax = Syntax(yaml_str, "yaml", theme="monokai", line_numbers=False)
    console.print(syntax)


@team_app.command("activate")
def team_activate(
    team_id: str = typer.Argument(..., help="Team ID to activate"),
) -> None:
    """Activate a team context."""
    from tilde.team.manager import get_team_manager

    manager = get_team_manager()
    
    try:
        config = manager.activate_team(team_id)
        rprint(f"[green]✓[/green] Activated team [cyan]{team_id}[/cyan]")
        rprint(f"  [dim]Team context will be included in profile responses.[/dim]")
    except ValueError as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@team_app.command("deactivate")
def team_deactivate() -> None:
    """Deactivate the current team context."""
    from tilde.team.manager import get_team_manager

    manager = get_team_manager()
    active = manager.get_active_team_id()
    
    if not active:
        rprint("[yellow]No team is currently active.[/yellow]")
        return
    
    manager.deactivate_team()
    rprint(f"[yellow]✗[/yellow] Deactivated team [cyan]{active}[/cyan]")


@team_app.command("sync")
def team_sync(
    source: str = typer.Argument(..., help="Source: file path, URL, or git repo"),
    activate: bool = typer.Option(False, "--activate", "-a", help="Activate the team after syncing"),
) -> None:
    """Sync team configuration from a source.
    
    Supports local files, HTTP URLs, and git repositories.
    """
    from tilde.team.sync import get_team_sync

    sync = get_team_sync()
    result = sync.auto_sync(source)

    if result.success:
        rprint(f"[green]✓[/green] {result.message}")
        if result.changes:
            for change in result.changes:
                rprint(f"  [dim]•[/dim] {change}")
        
        if activate and result.team_id:
            from tilde.team.manager import get_team_manager
            manager = get_team_manager()
            manager.activate_team(result.team_id)
            rprint(f"[green]✓[/green] Activated team [cyan]{result.team_id}[/cyan]")
    else:
        rprint(f"[red]✗[/red] {result.message}")
        raise typer.Exit(1)


@team_app.command("edit")
def team_edit(
    team_id: str = typer.Argument(None, help="Team ID (default: active team)"),
) -> None:
    """Edit team configuration in your default editor."""
    import os
    import subprocess

    from tilde.team.manager import get_team_manager

    manager = get_team_manager()
    
    if team_id is None:
        team_id = manager.get_active_team_id()
        if not team_id:
            rprint("[yellow]No active team. Specify a team ID.[/yellow]")
            raise typer.Exit(1)

    config = manager.get_team(team_id)
    if not config:
        rprint(f"[red]Team '{team_id}' not found.[/red]")
        raise typer.Exit(1)

    path = manager._get_team_path(team_id)
    editor = os.environ.get("EDITOR", "vim")
    
    rprint(f"Opening {path} in {editor}...")
    subprocess.run([editor, str(path)])


if __name__ == "__main__":
    app()
