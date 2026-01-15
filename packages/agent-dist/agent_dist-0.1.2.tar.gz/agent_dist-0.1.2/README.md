# AgentFlows

A lightweight agentic mesh for orchestrating AI agents in a hospital environment.

## ⚙️ Configuration

Copy the example configuration file:
```bash
cp .env.example .env
```
Edit `.env` to set your LLM provider.

### Supported LLM Providers
- **Ollama** (Default): Run local models via `ollama serve`.
- **Groq**: Fast inference. Set `LLM_PROVIDER=groq` and `GROQ_API_KEY`.
- **OpenAI**: Set `LLM_PROVIDER=openai` and `LLM_API_KEY`.

## Installation
```bash
pip install agentflows
```

## Running

**Registry:**
```bash
python -m agentflows.registry.app
```

**Orchestrator:**
```bash
python -m agentflows.orchestrator.app
```
