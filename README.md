# 💰 Wealth Management & Tax Advisory Demo

A multi-agent AI system for automated wealth management and tax advisory, built with **LangGraph** and **Ollama** (with Kimi K2.6 fallback).

## 🎯 Demo Overview

This system demonstrates three specialized AI agents collaborating to analyze a client's portfolio and generate tax-optimized financial advice under the **Indian Income Tax Act 2025**.

### Agents

| Agent | Role | What It Does |
|-------|------|-------------|
| 📊 **Data Retrieval Agent** | Data Layer | Fetches client portfolio from SQLite DB |
| 🧮 **Tax Agent** | Analysis Layer | Analyzes tax implications, flags opportunities |
| 📋 **Advisory Agent** | Synthesis Layer | Generates comprehensive financial strategy report |

### Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  📊 Data Agent  │────▶│  🧮 Tax Agent   │────▶│  📋 Advisory    │
│                 │     │                 │     │     Agent       │
│  SQLite DB      │     │  Tax Act 2025   │     │  Report Gen     │
│  Portfolio      │     │  Ollama/Kimi    │     │  Ollama/Kimi    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                ▼
                      ┌─────────────────┐
                      │  Shared State   │
                      │  (LangGraph)    │
                      └─────────────────┘
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
cd ~/laracorp/wealth-demo
source venv/bin/activate
```

### 2. Initialize Database

```bash
python -c "from database.seed_data import create_database; create_database()"
```

### 3. Run Terminal Demo

```bash
# List available clients
python demo.py --list

# Run demo for client 1 (Rajesh Mehta)
python demo.py --client 1
```

### 4. Launch Streamlit UI

```bash
streamlit run ui/app.py
```

The UI will be available at `http://localhost:8501`

## 📊 Demo Clients

| ID | Name | Profile | Income | Portfolio |
|----|------|---------|--------|-----------|
| 1 | Rajesh Mehta | Business Owner | ₹1.2Cr | ₹2.5Cr+ multi-asset |
| 2 | Priya Sharma | IT Professional | ₹50L | ₹15L diversified |
| 3 | Amitabh Khanna | CXO - MNC | ₹2.2Cr | ₹8Cr+ HNI portfolio |

## 🏗️ Project Structure

```
wealth-demo/
├── agents/
│   ├── __init__.py
│   ├── llm_client.py          # Ollama + Kimi K2.6 fallback
│   ├── data_retrieval.py      # Data Retrieval Agent
│   ├── tax_analysis.py        # Tax Analysis Agent
│   └── advisory.py            # Advisory Agent
├── database/
│   ├── __init__.py
│   ├── schema.sql             # DB schema
│   └── seed_data.py           # 3 Indian client profiles
├── models/
│   ├── __init__.py
│   └── state.py               # LangGraph shared state
├── ui/
│   └── app.py                 # Streamlit demo UI
├── graph.py                   # LangGraph wiring
├── demo.py                    # Terminal demo script
├── requirements.txt
└── README.md
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_URL` | `http://localhost:11434` | Ollama API endpoint |
| `OPENCLAW_URL` | `http://localhost:18789` | OpenClaw gateway (Kimi fallback) |

### LLM Fallback Chain

1. **Primary:** Ollama (qwen3.5:9b) — local, fast, no API dependency
2. **Fallback:** Kimi K2.6 via OpenClaw — cloud, higher quality

## 🎭 Demo Script for Presentation

### Terminal Demo (Recommended for Reliability)

```bash
# Show the system analyzing a high-net-worth client
python demo.py --client 3
```

**Narration:**
> "Watch as three specialized agents collaborate in real-time. First, the Data Agent fetches the complete portfolio. Then the Tax Agent analyzes every holding against the 2025 Income Tax Act. Finally, the Advisory Agent synthesizes everything into actionable recommendations."

### Streamlit Demo (Visual Impact)

```bash
streamlit run ui/app.py
```

**Narration:**
> "Here's the live dashboard. I select our HNI client Amitabh Khanna, click Generate, and watch the agents execute. Each agent's reasoning is visible in real-time. The final report includes tax flags, portfolio rebalancing suggestions, and specific action items."

## 🧪 Testing

```bash
# Test database
python -c "from database.seed_data import create_database, get_client_summary; create_database(); print(get_client_summary(1))"

# Test LLM client
python -c "from agents.llm_client import get_llm_client; c = get_llm_client(); print(c.generate('Hello, what is Section 80C?'))"

# Test full workflow
python -c "from graph import run_wealth_analysis; result = run_wealth_analysis(1); print(result['status'])"
```

## 📦 Dependencies

- **LangGraph** — Agent orchestration and state management
- **LangChain-Ollama** — Local LLM integration
- **Streamlit** — Demo UI
- **SQLite** — Mock database
- **Pandas** — Data manipulation

## 🔒 Security Notes

- No real client data — all profiles are fictional
- Ollama runs locally — no data leaves the machine
- Kimi fallback uses your OpenClaw gateway (authenticated)
- GitHub PAT stored in `~/.laracorp/secrets/github-pat.sh`

## 📝 License

Private — Internal Demo

---

Built with ❤️ by Lara (your AI co-founder) for the Monday demo presentation.
