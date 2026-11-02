# Smart Q&A Bot — Fitness & Wellness

A question-answering chatbot focused on **fitness and wellness**, built to demonstrate practical **LLM application development**, **backend engineering**, and **observability** using Python and LangChain.

The interface is intentionally lightweight: the main goal is to build reusable chatbot logic that can be integrated into a client's existing platform through a backend API.

## Project objectives

- Create a domain-focused assistant that answers fitness and wellness questions.
- Orchestrate language-model calls with LangChain chains and prompt templates.
- Return predictable, validated responses using structured output and Pydantic models.
- Improve reliability with error handling.
- Trace and inspect model executions with LangSmith.
- Expose the chatbot through a FastAPI backend while keeping the frontend simple.

> **Note:** This is a demonstration project, not a substitute for individualized medical advice.

## Key features

- **Domain-specific Q&A:** Prompts tailored to fitness and wellness topics.
- **LangChain orchestration:** Chains coordinate prompts, models, and output processing.
- **Structured responses:** Pydantic-based schemas help keep model output consistent.
- **Observability:** LangSmith tracing helps debug and analyze executions.
- **Error handling:** Application-level safeguards for failed model requests.
- **API-first approach:** Backend logic designed for integration into other applications.
- **Simple demo interface:** A minimal frontend showcases the chatbot interaction.

## Tech stack

| Technology | Purpose |
| --- | --- |
| Python 3.14+ | Backend implementation |
| LangChain / LangChain Core | Prompt templates, chains, and model orchestration |
| Pydantic | Data validation and structured output schemas |
| LangSmith | Execution tracing and observability |
| FastAPI | HTTP API |
| Uvicorn | ASGI development server |
| OpenAI / Anthropic integrations | LLM provider integrations |
| python-dotenv | Environment variable loading |
| uv | Dependency and environment management |

The project also declares **LangGraph** as a dependency, providing a foundation for future agent orchestration features.

## Getting started

### Prerequisites

- Git
- Python **3.14 or newer**
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- An API key for the language-model provider configured in your code
- A LangSmith API key (optional, for tracing)

### 1. Clone the repository

```bash
git clone https://github.com/saynarah/smart-bot-project.git
cd smart-bot-project
```

### 2. Install dependencies

```bash
uv sync
```

This creates a local virtual environment and installs dependencies defined in `pyproject.toml`.

### 3. Configure environment variables

Create a `.env` file at the project root and add the variables needed by the provider you use:

```dotenv
# Set the key for the provider configured in the application
OPENAI_API_KEY=your_openai_api_key
# ANTHROPIC_API_KEY=your_anthropic_api_key

# Optional: LangSmith tracing
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=smart-qa-bot
```

Use only the provider credentials your implementation requires. Check the code for the exact environment variable names used by the tracing configuration.

**Never commit your `.env` file or API keys.**

### 4. Start the backend

Run the FastAPI application with Uvicorn:

```bash
uv run uvicorn YOUR_API_MODULE:app --reload
```

Replace `YOUR_API_MODULE` with the import path to the Python module where your FastAPI `app` is declared (for example, `package.api` if the module is `package/api.py`).

Once running, the API is typically available at:

- API: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs

The root URL may return `404 Not Found` if no `/` endpoint is defined; use the actual chatbot endpoint or `/docs` instead.

### 5. Start the demo frontend

If your checkout includes a `frontend/` directory with static HTML, CSS, and JavaScript files, open a second terminal and run:

```bash
python3 -m http.server 5500 --directory frontend
```

Visit http://127.0.0.1:5500 and make sure the frontend's API URL points to the running backend.

## How it works

```text
User question
    |
    v
Simple frontend
    |
    v
FastAPI endpoint
    |
    v
LangChain prompt + chain
    |
    v
LLM provider
    |
    v
Pydantic structured output
    |
    v
Validated response to the user

LangSmith traces chain/model execution for debugging and monitoring.
```

## Contributing

Suggestions, bug reports, documentation improvements, and pull requests are welcome.

1. **Fork** the repository and clone your fork.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Install dependencies using `uv sync`.
4. Make your changes, keeping the backend modular and avoiding committed credentials.
5. Test the affected functionality locally and update documentation where relevant.
6. Commit with a descriptive message and push your branch:
   ```bash
   git add .
   git commit -m "feat: describe your change"
   git push origin feature/your-feature-name
   ```
7. Open a pull request describing the change, motivation, and how it was tested.

For defects or feature proposals, consider [opening an issue](https://github.com/saynarah/smart-bot-project/issues) first.

## Possible next steps

- Add automated unit and API tests.
- Introduce evaluation datasets to assess response quality.
- Strengthen input validation and error reporting.
- Containerize the backend for easier deployment.
- Expand monitoring and tracing coverage.
- Integrate the backend into a production-style client application.

## Author

Created by [Saynarah Nabuco](https://github.com/saynarah).

## Repository

[github.com/saynarah/smart-bot-project](https://github.com/saynarah/smart-bot-project)
