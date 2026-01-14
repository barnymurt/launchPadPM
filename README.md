# Scrum Team AI Agents

A modular, extensible framework for building and managing specialized AI agents that function as members of a Scrum product development team.

## 🎯 Overview

This project implements specialized AI agents based on Scrum methodology, Continuous Discovery Habits, and Opportunity Solution Trees. Each agent embodies a specific role in a Scrum team with deep expertise in their domain.

## 🏗️ Framework Features

- **Base Agent System**: Abstract base class with Scrum knowledge and collaboration support
- **Agent Registry**: Centralized management of all agents
- **Configuration System**: Flexible settings management
- **Cross-Functional Collaboration**: Built-in awareness between agents
- **Scrum Knowledge Base**: Shared Scrum framework knowledge
- **Continuous Discovery**: Integrated discovery habits support

## 📋 Implemented Agents

1. ✅ **Product Owner** - Maximizing product value, backlog management, continuous discovery
2. ⏳ **Scrum Master** - Team effectiveness, servant leadership, impediment removal
3. ⏳ **Development Engineer** - Technical implementation, Sprint Backlog ownership
4. ⏳ **QA Engineer** - Quality assurance, testing, Definition of Done
5. ⏳ **Business Analyst** - Requirements analysis, acceptance criteria
6. ⏳ **Data/Metrics Analyst** - Analytics, A/B testing, metrics
7. ⏳ **UX/UI Designer** - User experience, design systems, accessibility
8. ⏳ **Product Marketing Executive** - Go-to-market, positioning, launch planning
9. ✅ **DevOps Engineer** - Infrastructure, CI/CD pipelines, environment management, monitoring, security
10. ✅ **Frontend Developer** - User interfaces, frontend architecture, design systems, performance, accessibility
11. ✅ **User Researcher** - Empirical investigation, qualitative/quantitative research, cultural intelligence, insight generation

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd productteam

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Initialize the framework
python main.py init

# List registered agents
python main.py list

# Query an agent
python main.py query product_owner "Should we prioritize dark mode?"
```

### Python API

```python
from agents.product_owner_agent import ProductOwnerAgent
from agents.agent_registry import AgentRegistry

# Create and register agent
agent = ProductOwnerAgent()
AgentRegistry.register_agent(agent)

# Query the agent
response = agent.process_query("How should I prioritize features?")
print(response.response)
```

## 📁 Project Structure

```
productteam/
├── agents/              # Agent implementations
│   ├── base_agent.py    # Base class for all agents
│   ├── agent_registry.py
│   ├── product_owner_agent.py
│   └── example_agent.py
├── config/              # Configuration files
│   ├── settings.py
│   └── config.json
├── main.py              # CLI entry point
├── test_product_owner.py
├── requirements.txt
└── README.md
```

## 📚 Documentation

- **[README_FRAMEWORK.md](README_FRAMEWORK.md)** - Framework documentation and usage guide
- **[00_README.md](00_README.md)** - Original implementation guide with agent specifications
- **[IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md)** - Current implementation status

## 🧪 Testing

```bash
# Run Product Owner agent tests
python test_product_owner.py
```

## 🔧 Configuration

Edit `config/config.json` to customize:
- Product name and sprint settings
- Agent-specific configurations
- Framework features
- LLM provider settings (when integrated)

## 🤝 Contributing

When adding new agents:
1. Follow the pattern in `agents/example_agent.py`
2. Inherit from `BaseAgent`
3. Implement `get_role_specific_knowledge()` and `process_query()`
4. Register the agent in `main.py`
5. Add tests

## 📄 License

[Add your license here]

## 🙏 Credits

**Frameworks:**
- Scrum Guide 2020 (Schwaber & Sutherland)
- Continuous Discovery Habits (Teresa Torres)
- Opportunity Solution Trees (Teresa Torres)
- AARRR Metrics (Dave McClure)

---

**Status:** Framework complete, Product Owner agent implemented. 7 agents remaining.
