from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import date
from enum import Enum


class ProjectInfo(BaseModel):
    name: str = Field(..., description="Project name")
    description: str = Field(..., description="Brief project description")
    domain: str = Field(..., description="Research domain (e.g., quantum, biology, ml, physics, chemistry, materials, computer_science, other)")


class Author(BaseModel):
    name: str = Field(..., description="Author name")
    affiliation: str = Field(..., description="Institutional affiliation (or 'independent')")
    orcid: Optional[str] = Field(None, description="ORCID identifier")
    background: str = Field(..., description="Academic background / credentials")
    ai_role: str = Field(..., description="Role of AI in the research process (e.g., cognitive_prosthesis, co_pilot, autonomous_agent)")


class Evidence(BaseModel):
    git_commit: Optional[str] = Field(None, description="Git commit hash")
    job_ids: List[str] = Field(default_factory=list, description="Related job IDs")
    data_links: List[str] = Field(default_factory=list, description="Links to data repositories")
    code_links: List[str] = Field(default_factory=list, description="Links to code repositories")


class Metrics(BaseModel):
    z_score: Optional[float] = Field(None, description="Z-score for the event")
    shots: Optional[int] = Field(None, ge=0, description="Number of measurement shots")
    backend: Optional[str] = Field(None, description="Quantum backend used")
    job_ids: List[str] = Field(default_factory=list, description="Job IDs from quantum processor")
    z_score_combined: Optional[float] = Field(None, description="Combined Z-score (Fisher method)")


class Event(BaseModel):
    id: str = Field(..., pattern=r"^T([0-9]+|n)$|^(pivot|control|submission|publication|milestone)$", description="Event identifier (T0, T1, T2, Tn, pivot, control, submission, publication, milestone)")
    event_type: str = Field(..., description="Event type", alias="type")
    event_date: date = Field(..., description="Event date (ISO 8601)", alias="date")
    description: str = Field(..., description="Human-readable description of the event")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")
    metrics: Optional[Dict[str, Any]] = Field(None, description="Quantitative metrics for the event (arbitrary key-value pairs)")
    evidence: Optional[Dict[str, Any]] = Field(None, description="Supporting evidence for the event")


class ResearchTimeline(BaseModel):
    project: dict = Field(..., description="Project information")
    author: dict = Field(..., description="Author information")
    events: List[dict] = Field(..., min_length=1, description="Timeline events")
    created_at: date = Field(default_factory=date.today, description="Timeline creation date")
    updated_at: date = Field(default_factory=date.today, description="Last update date")
    version: str = Field(default="1.0", description="Timeline schema version")


if __name__ == "__main__":
    import json
    timeline = {
        "project": {
            "name": "PASM DTC Discovery",
            "description": "Observation of Classical Prethermal DTC on IBM Heron",
            "domain": "quantum"
        },
        "author": {
            "name": "N47Lab",
            "affiliation": "independent",
            "orcid": "https://orcid.org/0009-0008-9201-6080",
            "background": "without academic degrees",
            "ai_role": "cognitive_prosthesis"
        },
        "events": [
            {
                "id": "T0",
                "type": "T0",
                "date": "2026-06-06",
                "description": "First AI interaction: setup, theory, protocol design",
                "tags": ["setup", "theory", "protocol_design"],
                "evidence": {
                    "data_links": [".opencode log"]
                }
            },
            {
                "id": "T1",
                "type": "T1",
                "date": "2026-07-31",
                "description": "First commit: 14 QPU experiments, Z>50σ",
                "tags": ["commit", "qpu", "baseline"],
                "metrics": {"z_score_combined": 50.0},
                "evidence": {
                    "git_commit": "c3ddc4a",
                    "job_ids": []
                }
            }
        ]
    }
    print("Schema validation passed!")
    import json
    print(json.dumps({
        "project": {
            "name": "PASM DTC Discovery",
            "description": "Observation of Classical Prethermal DTC on IBM Heron",
            "domain": "quantum"
        },
        "author": {
            "name": "N47Lab",
            "affiliation": "independent",
            "orcid": "https://orcid.org/0009-0008-9201-6080",
            "background": "without academic degrees",
            "ai_role": "cognitive_prosthesis"
        },
        "events": [
            {
                "id": "T0",
                "type": "T0",
                "date": "2026-06-06",
                "description": "First AI interaction: setup, theory, protocol design",
                "tags": ["setup", "theory", "protocol_design"],
                "evidence": {
                    "data_links": [".opencode log"]
                }
            },
            {
                "id": "T1",
                "type": "T1",
                "date": "2026-07-31",
                "description": "First commit: 14 QPU experiments, Z>50σ",
                "tags": ["commit", "qpu", "baseline"],
                "metrics": {"z_score_combined": 50.0},
                "evidence": {
                    "git_commit": "c3ddc4a",
                    "job_ids": []
                }
            }
        ]
    }, indent=2))