# AIDiscuss

> AI-powered chat application with multi-provider support and embedded web UI

AIDiscuss is a modern, production-ready AI chat application that supports multiple LLM providers (Anthropic, OpenAI, Google, Groq) with advanced features like RAG, memory management, and multi-agent conversations. Built with FastAPI and React, distributed as a PyPI package.

## Features

- **Multi-Provider Support**: Anthropic Claude, OpenAI, Google Gemini, Groq
- **Advanced AI Features**: RAG (Retrieval-Augmented Generation), conversation memory, multi-agent orchestration
- **Embedded Web UI**: Beautiful React interface bundled with the Python package
- **Multi-Environment Isolation**: Automatic data separation for virtual environments vs global installs
- **Secure by Default**: Local-only storage, localhost binding, bytecode distribution
- **Production Ready**: Structured logging, version checking, graceful error handling

## Installation

```bash
pip install aidiscuss
```

Requires Python 3.11+

## Usage

```bash
aidiscuss
```

Opens the web UI at http://127.0.0.1:8000

### Configuration

On first run, AIDiscuss creates a config file:
- **Virtual env**: `{venv}/.aidiscuss_data/.env`
- **Global**: `~/.aidiscuss/.env`

API keys are configured through the web UI.

### Environment Isolation

Each installation maintains separate data:

```bash
venv1/bin/aidiscuss  # Data in venv1/.aidiscuss_data/
venv2/bin/aidiscuss  # Data in venv2/.aidiscuss_data/
aidiscuss            # Global data in ~/.aidiscuss/
```

## API

- **Web UI**: http://127.0.0.1:8000

### Key Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check |
| `POST /api/chat/stream` | Streaming chat |
| `GET /api/providers` | List LLM providers |
| `POST /api/rag/upload` | Upload documents |

## Troubleshooting

**Port in use**: AIDiscuss auto-finds ports 8000-8100, or set `PORT=8080`

**Custom data dir**: Set `AIDISCUSS_DATA_DIR=/path/to/data`

**Logs**: `~/.aidiscuss/logs/aidiscuss.log` or `{venv}/.aidiscuss_data/logs/`

## Security

Report vulnerabilities via GitHub Security Advisories. Do not open public issues.

## License

MIT License - see [LICENSE](LICENSE)