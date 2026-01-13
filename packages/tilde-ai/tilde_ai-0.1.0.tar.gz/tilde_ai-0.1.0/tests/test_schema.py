"""Tests for tilde schema."""

from tilde.schema import (
    Identity,
    Knowledge,
    KnowledgeSource,
    Skill,
    TeamContext,
    TechStack,
    TildeProfile,
    UserProfile,
)


def test_identity_defaults():
    """Test Identity has sensible defaults."""
    identity = Identity()
    assert identity.name == ""
    assert identity.role == ""
    assert identity.years_experience is None


def test_identity_with_values():
    """Test Identity with provided values."""
    identity = Identity(name="Allen", role="Senior SWE", years_experience=12)
    assert identity.name == "Allen"
    assert identity.role == "Senior SWE"
    assert identity.years_experience == 12


def test_tech_stack_defaults():
    """Test TechStack has sensible defaults."""
    tech = TechStack()
    assert tech.languages == []
    assert tech.preferences == []
    assert tech.environment is None


def test_knowledge_source():
    """Test KnowledgeSource model."""
    source = KnowledgeSource(
        title="Designing Data-Intensive Applications",
        source_type="book",
        insights=["Prefer append-only logs", "Understand CAP theorem"],
    )
    assert source.title == "Designing Data-Intensive Applications"
    assert source.source_type == "book"
    assert len(source.insights) == 2


def test_knowledge():
    """Test Knowledge with all fields."""
    knowledge = Knowledge(
        domains={"finance": "Technical indicators"},
        sources=[KnowledgeSource(title="DDIA", source_type="book")],
    )
    assert len(knowledge.sources) == 1
    assert knowledge.domains["finance"] == "Technical indicators"


def test_full_profile():
    """Test complete TildeProfile."""
    profile = TildeProfile(
        schema_version="1.0.0",
        user_profile=UserProfile(
            identity=Identity(name="Allen", role="SWE"),
            tech_stack=TechStack(languages=["Python"]),
        ),
        team_context=TeamContext(organization="MyStartup"),
    )
    assert profile.schema_version == "1.0.0"
    assert profile.user_profile.identity.name == "Allen"
    assert profile.team_context is not None
    assert profile.team_context.organization == "MyStartup"


def test_profile_json_serialization():
    """Test profile can be serialized to JSON."""
    profile = TildeProfile(
        user_profile=UserProfile(
            identity=Identity(name="Test"),
        )
    )
    json_str = profile.model_dump_json()
    assert "Test" in json_str


def test_profile_from_dict():
    """Test profile can be created from dict (YAML loading)."""
    data = {
        "schema_version": "1.0.0",
        "user_profile": {
            "identity": {"name": "Allen", "role": "SWE"},
            "tech_stack": {"languages": ["Python", "TypeScript"]},
            "knowledge": {
                "sources": [{"title": "DDIA", "source_type": "book", "insights": ["Log-based"]}]
            },
        },
    }
    profile = TildeProfile.model_validate(data)
    assert profile.user_profile.identity.name == "Allen"
    assert len(profile.user_profile.knowledge.sources) == 1


# =============================================================================
# Skill tests
# =============================================================================


def test_skill_model():
    """Test Skill model with all fields."""
    skill = Skill(
        name="Prompt Engineering",
        description="Crafting effective prompts for LLMs",
        visibility="public",
        tags=["AI", "LLM"],
    )
    assert skill.name == "Prompt Engineering"
    assert skill.description == "Crafting effective prompts for LLMs"
    assert skill.visibility == "public"
    assert len(skill.tags) == 2


def test_skill_defaults():
    """Test Skill model with just required fields."""
    skill = Skill(name="Python")
    assert skill.name == "Python"
    assert skill.description is None
    assert skill.visibility == "public"
    assert skill.tags == []


def test_skill_visibility_options():
    """Test different visibility settings for skills."""
    public_skill = Skill(name="Public", visibility="public")
    private_skill = Skill(name="Private", visibility="private")
    team_skill = Skill(name="Team", visibility="team")

    assert public_skill.visibility == "public"
    assert private_skill.visibility == "private"
    assert team_skill.visibility == "team"


# =============================================================================
# Knowledge source types
# =============================================================================


def test_knowledge_source_types():
    """Test KnowledgeSource with different source types."""
    book = KnowledgeSource(title="DDIA", source_type="book")
    doc = KnowledgeSource(title="LangChain Docs", source_type="document", url="https://docs.langchain.com")
    course = KnowledgeSource(title="ML Course", source_type="course")

    assert book.source_type == "book"
    assert doc.source_type == "document"
    assert doc.url == "https://docs.langchain.com"
    assert course.source_type == "course"


# =============================================================================
# Extensibility tests
# =============================================================================


def test_identity_extra_fields():
    """Test Identity accepts arbitrary extra fields."""
    identity = Identity(
        name="Allen",
        language="English, Mandarin",  # extra field
        github="topskychen",  # extra field
        timezone="America/Los_Angeles",  # extra field
    )
    assert identity.name == "Allen"
    assert identity.language == "English, Mandarin"
    assert identity.github == "topskychen"
    assert identity.timezone == "America/Los_Angeles"


def test_extra_fields_serialization():
    """Test extra fields round-trip through serialization."""
    profile = TildeProfile(
        user_profile=UserProfile(
            identity=Identity(name="Test", custom_field="custom_value"),
        )
    )
    data = profile.model_dump()
    assert data["user_profile"]["identity"]["custom_field"] == "custom_value"

    # Reload from dict
    reloaded = TildeProfile.model_validate(data)
    assert reloaded.user_profile.identity.custom_field == "custom_value"


def test_profile_with_skills():
    """Test complete profile with skills."""
    profile = TildeProfile(
        user_profile=UserProfile(
            identity=Identity(name="Allen"),
            skills=[
                Skill(name="Python", visibility="public"),
                Skill(name="Trading", visibility="private"),
            ],
        )
    )
    assert len(profile.user_profile.skills) == 2
    public_skills = [s for s in profile.user_profile.skills if s.visibility == "public"]
    assert len(public_skills) == 1
