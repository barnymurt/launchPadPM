# Scrum Team AI Agents Framework

A modular, extensible framework for building and managing specialized AI agents that function as members of a Scrum product development team.

## 🏗️ Framework Overview

This framework provides:

- **Base Agent Class**: Abstract base class for all agents
- **Agent Registry**: Centralized management of all agents
- **Configuration System**: Flexible settings management
- **Collaboration Support**: Built-in cross-functional awareness
- **Scrum Knowledge**: Shared Scrum framework knowledge
- **Continuous Discovery**: Integrated discovery habits support

## 📁 Project Structure

```
productteam/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py          # Base class for all agents
│   ├── agent_registry.py      # Agent registration and retrieval
│   └── example_agent.py       # Template for creating new agents
├── config/
│   ├── __init__.py
│   ├── settings.py            # Configuration management
│   └── config.json            # Configuration file
├── main.py                    # CLI entry point
├── requirements.txt           # Python dependencies
├── 00_README.md              # Original implementation guide
└── README_FRAMEWORK.md       # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Framework

```bash
python main.py init
```

### 3. Create Your First Agent

Create a new file `agents/product_owner_agent.py`:

```python
from agents.base_agent import BaseAgent, AgentResponse, AgentContext
from typing import Dict, Any

class ProductOwnerAgent(BaseAgent):
    def __init__(self, context: AgentContext = None):
        super().__init__(
            role="Product Owner",
            name="PO",
            context=context
        )
    
    def get_role_specific_knowledge(self) -> Dict[str, Any]:
        return {
            "primary_responsibilities": [
                "Maximize product value",
                "Manage Product Backlog",
                "Conduct continuous discovery",
                "Use Opportunity Solution Trees"
            ],
            # ... add more knowledge
        }
    
    def process_query(self, query: str, **kwargs) -> AgentResponse:
        # Implement your agent logic here
        return self.format_response(
            response_text="Your response here",
            recommendations=["Rec 1", "Rec 2"]
        )
```

### 4. Register and Use Agent

```python
from agents.product_owner_agent import ProductOwnerAgent
from agents.agent_registry import AgentRegistry

# Register the agent
agent = ProductOwnerAgent()
AgentRegistry.register_agent(agent)

# Query the agent
response = agent.process_query("Should we prioritize dark mode?")
print(response.response)
```

### 5. Use CLI

```bash
python main.py query product_owner "Should we prioritize dark mode?"
```

## 📚 Creating New Agents

### Step-by-Step Guide

1. **Create Agent File**: Create `agents/<role>_agent.py`

2. **Inherit from BaseAgent**:
   ```python
   from agents.base_agent import BaseAgent, AgentResponse
   
   class YourAgent(BaseAgent):
       def __init__(self, context=None):
           super().__init__(
               role="Your Role",
               name="ShortName",
               context=context
           )
   ```

3. **Implement Required Methods**:
   - `get_role_specific_knowledge()`: Define role-specific knowledge
   - `process_query()`: Main logic for handling queries

4. **Optional Overrides**:
   - `identify_collaboration_needs()`: Define when to collaborate
   - `get_cross_functional_awareness()`: Define collaboration patterns

5. **Register Agent**:
   ```python
   AgentRegistry.register_agent(YourAgent())
   ```

## 🔧 Configuration

Edit `config/config.json` to customize:

- Product name and sprint settings
- Agent-specific configurations
- Framework features (collaboration, continuous discovery, etc.)
- LLM provider settings (when integrated)

## 🤝 Collaboration Patterns

Agents can collaborate by:

1. **Identifying Collaboration Needs**: Override `identify_collaboration_needs()`
2. **Cross-Functional Awareness**: Define in `get_cross_functional_awareness()`
3. **Response Flags**: Set `requires_collaboration=True` in responses

Example:
```python
def process_query(self, query: str, **kwargs) -> AgentResponse:
    # Check if collaboration needed
    needs_dev = "technical" in query.lower()
    
    return self.format_response(
        response_text="...",
        requires_collaboration=needs_dev,
        collaborating_roles=["development_engineer"] if needs_dev else []
    )
```

## 📋 Agent Roles to Implement

Based on `00_README.md`, implement these 8 agents:

1. ✅ **Product Owner** (`01_Product_Owner_Agent.md`)
2. ✅ **Scrum Master** (`02_Scrum_Master_Agent.md`)
3. ✅ **Development Engineer** (`03_Development_Engineer_Agent.md`)
4. ✅ **QA Engineer** (`04_QA_Engineer_Agent.md`)
5. ✅ **Business Analyst** (`05_Business_Analyst_Agent.md`)
6. ✅ **Data/Metrics Analyst** (`06_Data_Metrics_Analyst_Agent.md`)
7. ✅ **UX/UI Designer** (`07_UX_UI_Designer_Agent.md`)
8. ✅ **Product Marketing Executive** (`08_Product_Marketing_Executive_Agent.md`)

## 🧪 Testing

```bash
# Run tests (when test files are added)
pytest

# With coverage
pytest --cov=agents
```

## 🔌 LLM Integration (Future)

To integrate with LLM providers:

1. Add provider SDK to `requirements.txt`
2. Create LLM adapter in `agents/llm_adapter.py`
3. Update `BaseAgent.process_query()` to use LLM
4. Configure API keys in `config/config.json` or environment variables

Example structure:
```python
from agents.llm_adapter import LLMAdapter

class ProductOwnerAgent(BaseAgent):
    def __init__(self, context=None):
        super().__init__(...)
        self.llm = LLMAdapter(provider="openai")
    
    def process_query(self, query: str, **kwargs) -> AgentResponse:
        prompt = self._build_prompt(query)
        response = self.llm.generate(prompt)
        return self._parse_response(response)
```

## 📝 Next Steps

1. **Add Agent Implementations**: Create the 8 agent classes based on the prompts in `00_README.md`
2. **Add Agent Prompt Files**: Store the detailed prompts from the original guide
3. **Integrate LLM**: Connect to OpenAI, Anthropic, or other providers
4. **Add Multi-Agent Orchestration**: Enable agents to query each other
5. **Add Persistence**: Store conversations and context
6. **Add Web Interface**: Create a web UI for interacting with agents

## 🐛 Troubleshooting

**Agent not found?**
- Make sure you've registered the agent: `AgentRegistry.register_agent(agent)`
- Check role name matches (case-insensitive, spaces become underscores)

**Import errors?**
- Ensure you're in the project root directory
- Check that `__init__.py` files exist in all packages

**Configuration not loading?**
- Verify `config/config.json` exists and is valid JSON
- Check file permissions

## 📄 License

See project license file.

## 🤝 Contributing

When adding new agents:
1. Follow the pattern in `example_agent.py`
2. Update this README with agent details
3. Add tests for your agent
4. Update `config.json` with agent settings

---

**Ready to build?** Start by implementing the Product Owner agent, then add the others one by one!
