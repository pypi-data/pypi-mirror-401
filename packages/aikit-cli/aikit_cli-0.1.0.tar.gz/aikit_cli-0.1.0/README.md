# aikit-cli

**aikit-cli** is a lightweight command-line tool for scaffolding minimal AI projects.  
It provides opinionated, ready-to-use boilerplate for common AI patterns.

---

## Installation

```bash
pip install aikit-cli
```

## Usage

Create a new project:

```bash
# Interactive mode
aikit-cli new my-bot

# One-liner
aikit-cli new my-bot --type chatbot --provider openai
```

### Options

| Option | Shorthand | Description | Default |
|--------|-----------|-------------|---------|
| `--type` | `-t` | Project type (`chatbot` or `rag`) | `chatbot` |
| `--provider` | `-p` | AI provider (`openai` or `ollama`) | `openai` |
| `--create-venv`| | Create a virtual environment | `False` |
| `--non-interactive` | | Fail if required options are missing instead of prompting | `False` |

### Examples

**Interactive Mode (Recommended)**:
```bash
aikit-cli new my-bot
```

**Quick Create (Chatbot with OpenAI)**:
```bash
aikit-cli new my-bot --type chatbot --provider openai
```

**Local RAG Project (with Ollama)**:
```bash
aikit-cli new local-rag --type rag --provider ollama
```

## Generated Structure

After creating a project, you'll get a clean structure similar to this:

```
my-bot/
├── .env                # Environment variables (API keys, etc.)
├── app/
│   ├── __init__.py
│   ├── main.py         # Entry point
│   ├── config.py       # Configuration settings
│   └── provider.py     # LLM provider wrapper
├── pyproject.toml      # Project dependencies
└── README.md
```

##  Running Your Project

1. Navigate to the created directory:
   ```bash
   cd my-bot
   ```
# TODO: Add poetry/uv support + dependencies
2. Install dependencies:
   ```bash
   pip install .  # or use poetry/uv
   ```

3. Configure environment:
   - For OpenAI: Add `OPENAI_API_KEY=sk-...` to `.env`.
   - For Ollama: Ensure Ollama is running (`ollama serve`).

4. Run the app:
   ```bash
   python app/main.py
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

MIT
