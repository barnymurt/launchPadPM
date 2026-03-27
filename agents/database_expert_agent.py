"""
Database Expert Agent
Expertise in:
- Data modeling and schema design
- Database architecture (SQL, NoSQL, NewSQL)
- Query optimization and performance tuning
- Data migration planning
- Backup and recovery strategies
- Data warehousing and analytics databases
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentResponse, AgentContext


class DatabaseExpertAgent(BaseAgent):
    """
    Database Expert AI Agent
    
    Primary Accountability: Design optimal data storage solutions, ensure data integrity,
    optimize performance, and manage data migrations.
    """
    
    def __init__(self, context: AgentContext = None):
        super().__init__(
            role="Database Expert",
            name="DB Expert",
            context=context
        )
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        return {
            "primary_accountability": "Design and maintain database architecture, optimize query performance, ensure data integrity and backup/recovery",
            "core_identity": {
                "role_in_scrum": "Part of the technical team, provides database expertise",
                "participation": [
                    "Review data models and schemas",
                    "Optimize slow queries",
                    "Design database migration strategies",
                    "Ensure proper indexing and data partitioning",
                    "Plan for scale and data growth"
                ]
            },
            "key_responsibilities": {
                "data_modeling": {
                    "approaches": ["Normalized", "Denormalized", "Hybrid", "Event sourcing"],
                    "artifacts": ["ER diagrams", "Schema definitions", "Data dictionaries"],
                    "principles": [
                        "Choose the right model for the use case",
                        "Plan for queries before optimizing for storage",
                        "Design for change - schemas evolve"
                    ]
                },
                "database_types": {
                    "relational": ["PostgreSQL", "MySQL", "SQL Server", "Aurora"],
                    "document": ["MongoDB", "DocumentDB", "Couchbase"],
                    "key_value": ["Redis", "DynamoDB", "Cassandra"],
                    "columnar": ["BigQuery", "Redshift", "ClickHouse"],
                    "graph": ["Neo4j", "Amazon Neptune"],
                    "time_series": ["InfluxDB", "TimescaleDB"]
                },
                "performance": {
                    "indexing_strategies": ["B-tree", "Hash", "GIN", "GIN", "Full-text"],
                    "query_optimization": ["EXPLAIN analysis", "Query rewriting", "Materialized views"],
                    "scaling": ["Read replicas", "Sharding", "Partitioning", "Caching"]
                }
            }
        }
    
    def get_scrum_ceremony_guidance(self) -> Dict[str, str]:
        return {
            "sprint_planning": "Estimate database work, flag data migration needs",
            "daily_scrum": "Report on database tasks, any performance issues",
            "sprint_review": "Demonstrate database changes, data migrations",
            "retrospective": "Review database-related bottlenecks, suggest improvements"
        }