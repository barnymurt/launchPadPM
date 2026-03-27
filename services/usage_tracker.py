"""
Usage tracking service for skill telemetry.
Logs skill usage to data/skill-usage.json for analytics.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
from threading import Lock

DATA_DIR = Path("data")
USAGE_FILE = DATA_DIR / "skill-usage.json"

_usage_lock = Lock()

def _ensure_data_dir():
    """Ensure data directory exists."""
    DATA_DIR.mkdir(exist_ok=True)

def _load_usage() -> dict:
    """Load existing usage data from JSON file."""
    _ensure_data_dir()
    if not USAGE_FILE.exists():
        return {"skills": {}, "sessions": [], "last_updated": None}
    
    try:
        with open(USAGE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"skills": {}, "sessions": [], "last_updated": None}

def _save_usage(data: dict):
    """Save usage data to JSON file."""
    _ensure_data_dir()
    data["last_updated"] = datetime.utcnow().isoformat()
    with open(USAGE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def track_skill_usage(
    skill_name: str,
    agent_name: Optional[str] = None,
    user_id: Optional[str] = None,
    duration_ms: Optional[int] = None,
    success: bool = True,
    error: Optional[str] = None
) -> dict:
    """
    Track a skill invocation.
    
    Returns the updated usage record for this skill.
    """
    with _usage_lock:
        usage = _load_usage()
        
        # Initialize skill entry if doesn't exist
        if skill_name not in usage["skills"]:
            usage["skills"][skill_name] = {
                "name": skill_name,
                "total_invocations": 0,
                "successful_invocations": 0,
                "failed_invocations": 0,
                "total_duration_ms": 0,
                "avg_duration_ms": 0,
                "last_used": None,
                "invocations_by_day": {},
                "invocations_by_agent": {},
                "errors": []
            }
        
        skill_stats = usage["skills"][skill_name]
        
        # Update invocation counts
        skill_stats["total_invocations"] += 1
        if success:
            skill_stats["successful_invocations"] += 1
        else:
            skill_stats["failed_invocations"] += 1
        
        # Update duration
        if duration_ms is not None:
            skill_stats["total_duration_ms"] += duration_ms
            skill_stats["avg_duration_ms"] = (
                skill_stats["total_duration_ms"] // skill_stats["total_invocations"]
            )
        
        # Update last used
        skill_stats["last_used"] = datetime.utcnow().isoformat()
        
        # Update daily counts
        today = datetime.utcnow().strftime("%Y-%m-%d")
        skill_stats["invocations_by_day"][today] = (
            skill_stats["invocations_by_day"].get(today, 0) + 1
        )
        
        # Update agent counts
        if agent_name:
            skill_stats["invocations_by_agent"][agent_name] = (
                skill_stats["invocations_by_agent"].get(agent_name, 0) + 1
            )
        
        # Track errors (keep last 10)
        if error:
            skill_stats["errors"].append({
                "timestamp": datetime.utcnow().isoformat(),
                "error": error
            })
            skill_stats["errors"] = skill_stats["errors"][-10:]
        
        _save_usage(usage)
        
        return skill_stats

def get_usage_stats() -> dict:
    """Get overall usage statistics."""
    usage = _load_usage()
    
    total_invocations = sum(s["total_invocations"] for s in usage["skills"].values())
    total_successful = sum(s["successful_invocations"] for s in usage["skills"].values())
    total_failed = sum(s["failed_invocations"] for s in usage["skills"].values())
    
    # Top 10 most used skills
    top_skills = sorted(
        usage["skills"].values(),
        key=lambda x: x["total_invocations"],
        reverse=True
    )[:10]
    
    return {
        "total_skill_invocations": total_invocations,
        "total_successful": total_successful,
        "total_failed": total_failed,
        "unique_skills_used": len(usage["skills"]),
        "last_updated": usage["last_updated"],
        "top_skills": [
            {
                "name": s["name"],
                "invocations": s["total_invocations"],
                "last_used": s["last_used"]
            }
            for s in top_skills
        ]
    }

def get_skill_usage(skill_name: str) -> Optional[dict]:
    """Get usage stats for a specific skill."""
    usage = _load_usage()
    return usage["skills"].get(skill_name)

def get_all_usage() -> dict:
    """Get all usage data."""
    return _load_usage()

def reset_usage():
    """Reset all usage data (for testing/admin)."""
    with _usage_lock:
        _save_usage({"skills": {}, "sessions": [], "last_updated": None})