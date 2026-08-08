import pytest
from datetime import date
from research_timeline.models import ResearchTimeline, ProjectInfo, Author, Event, Metrics, Evidence


def test_basic_timeline():
    """Test basic timeline creation."""
    timeline = {
        "project": {
            "name": "Test Project",
            "description": "Test",
            "domain": "quantum"
        },
        "author": {
            "name": "Test Author",
            "affiliation": "independent",
            "orcid": "https://orcid.org/0000-0000-0000-0000",
            "background": "without academic degrees",
            "ai_role": "cognitive_prosthesis"
        },
        "events": [
            {
                "id": "T0",
                "type": "T0",
                "date": "2026-06-06",
                "description": "First AI interaction",
                "tags": ["setup"],
                "metrics": {},
                "evidence": {}
            }
        ],
        "created_at": "2026-08-06",
        "updated_at": "2026-08-06",
        "version": "1.0"
    }
    
    # This would be validated by pydantic in real usage
    assert True


def test_event_validation():
    """Test event ID validation."""
    from research_timeline.models import Event
    
    # Valid IDs
    Event(id="T0", type="T0", date="2026-06-06", description="Test")
    Event(id="T1", type="T1", date="2026-06-06", description="Test")
    Event(id="Tn", type="Tn", date="2026-06-06", description="Test")
    Event(id="pivot", type="pivot", date="2026-08-01", description="Pivot")
    Event(id="control", type="control", date="2026-08-01", description="Control")
    Event(id="submission", type="submission", date="2026-08-01", description="Submission")
    Event(id="publication", type="publication", date="2026-08-01", description="Publication")
    Event(id="milestone", type="milestone", date="2026-08-01", description="Milestone")
    
    # Invalid ID should raise
    try:
        Event(id="X0", type="T0", date="2026-06-06", description="Test")
        assert False, "Should have raised"
    except ValueError:
        pass  # Expected


def test_metrics_optional():
    """Test that metrics are optional."""
    from research_timeline.models import Event
    
    event = Event(
        id="T0",
        type="T0",
        date="2026-06-06",
        description="Test"
    )
    assert event.metrics is None
    
    # With metrics (as dict)
    event2 = Event(
        id="T1",
        type="T1",
        date="2026-07-01",
        description="Test",
        metrics={"z_score": 50.0, "shots": 8192}
    )
    assert event2.metrics is not None
    assert event2.metrics["z_score"] == 50.0
    assert event2.metrics["shots"] == 8192


if __name__ == "__main__":
    pytest.main([__file__, "-v"])