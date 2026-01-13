"""Pydantic models for tilde profile schema.

This schema follows a minimal-core + extensibility approach:
- Core fields are typed for IDE completion and validation
- All models accept extra fields via ConfigDict(extra="allow")
- Users can add custom fields like language, github, timezone, etc.
"""

from pydantic import BaseModel, ConfigDict


class Identity(BaseModel):
    """User identity information.
    
    Core fields are defined, but you can add any extra fields like:
    - language: "English, Mandarin"
    - location: "San Francisco"
    - github: "username"
    - timezone: "America/Los_Angeles"
    """
    model_config = ConfigDict(extra="allow")

    name: str = ""
    role: str = ""
    years_experience: int | None = None


class TechStack(BaseModel):
    """Technical preferences and environment."""
    model_config = ConfigDict(extra="allow")

    languages: list[str] = []
    preferences: list[str] = []
    environment: str | None = None


class KnowledgeSource(BaseModel):
    """A source of knowledge (book, document, course, article, etc.)."""
    model_config = ConfigDict(extra="allow")

    title: str
    source_type: str = "book"  # book, document, course, article, podcast, video
    insights: list[str] = []
    topics: list[str] = []
    url: str | None = None


class Knowledge(BaseModel):
    """Domain expertise and learned knowledge."""
    model_config = ConfigDict(extra="allow")

    domains: dict[str, str] = {}
    sources: list[KnowledgeSource] = []


class Skill(BaseModel):
    """A skill with optional visibility controls.
    
    Visibility options:
    - "public": Shared with AI agents (default)
    - "private": Hidden from agents, only visible to you
    - "team": Shared within team context only
    """
    model_config = ConfigDict(extra="allow")

    name: str
    description: str | None = None
    visibility: str = "public"  # public, private, team
    tags: list[str] = []


class Experience(BaseModel):
    """Work experience entry."""
    model_config = ConfigDict(extra="allow")

    company: str
    role: str
    start_date: str | None = None
    end_date: str | None = None  # None = current
    highlights: list[str] = []
    technologies: list[str] = []


class Education(BaseModel):
    """Education entry."""
    model_config = ConfigDict(extra="allow")

    institution: str
    degree: str | None = None
    field: str | None = None
    graduation_year: int | None = None
    highlights: list[str] = []


class Project(BaseModel):
    """Project entry."""
    model_config = ConfigDict(extra="allow")

    name: str
    description: str | None = None
    url: str | None = None
    technologies: list[str] = []
    highlights: list[str] = []


class Publication(BaseModel):
    """Academic publication."""
    model_config = ConfigDict(extra="allow")

    title: str
    venue: str | None = None  # journal/conference
    year: int | None = None
    url: str | None = None
    authors: list[str] = []


class UserProfile(BaseModel):
    """Complete user profile with extensible fields."""
    model_config = ConfigDict(extra="allow")

    identity: Identity = Identity()
    tech_stack: TechStack = TechStack()
    knowledge: Knowledge = Knowledge()
    skills: list[Skill] = []
    experience: list[Experience] = []
    education: list[Education] = []
    projects: list[Project] = []
    publications: list[Publication] = []


class TeamContext(BaseModel):
    """Team-level coding standards and patterns."""
    model_config = ConfigDict(extra="allow")

    organization: str = ""
    coding_standards: str | None = None
    architecture_patterns: str | None = None
    do_not_use: list[str] = []


class TildeProfile(BaseModel):
    """Root profile schema with versioning."""
    model_config = ConfigDict(extra="allow")

    schema_version: str = "1.0.0"
    user_profile: UserProfile = UserProfile()
    team_context: TeamContext | None = None
