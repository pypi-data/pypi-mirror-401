# RAG Blueprint

**RAG Blueprint** is a Python CLI tool that scaffolds production-ready RAG (Retrieval-Augmented Generation) applications. It uses **LangChain** and **uv** to get you started quickly with best practices.

## Installation

You can install `rag-blueprint` via pip (once published) or `uv`:

```bash
# From PyPI (Coming soon)
pip install rag-blueprint

# From Source
git clone ...
cd rag-blueprint
py -m uv sync
```

## Quick Start

Generate a new RAG project:

```bash
# Create a simple project (interactive)
rag-blueprint create my-rag-app

# Create specific template
rag-blueprint create pro-rag-app --template advanced

# Create an agentic project
rag-blueprint create agent-rag-app --template agentic
```

## Templates

| Template | Description | Stack |
|----------|-------------|-------|
| `simple` | Basic RAG pipeline. Good for getting started. | LangChain, Chroma/FAISS, OpenAI |
| `advanced` | Production-ready pipeline with Hybrid Search & Reranking. | BM25, Chroma, FlashRank, GPT-4 |
| `agentic` | Agent-based RAG with tool use (Web Search + Vector Store). | LangGraph, Tavily, Tools |

## Development

```bash
# Windows
py -m uv run rag-blueprint --help

# Mac/Linux (if uv is in PATH)
uv run rag-blueprint --help
```
