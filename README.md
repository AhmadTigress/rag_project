# Multi-Document Chat RAG System

## Overview
This repository contains a robust, production-ready Retrieval-Augmented Generation (RAG) system designed to ingest, process, and accurately query multiple documents simultaneously. The architecture leverages advanced semantic search, deterministic data parsing, and persistent memory to provide an enterprise-grade AI chatbot experience.

The system is engineered for scalability and maintainability, featuring a decoupled modular structure, comprehensive CI/CD workflows, and containerized deployment options.

## Features
*   **Multi-Document Ingestion:** Dynamically load and process varied document types (PDFs, TXT) across distinct user sessions.
*   **Optimized Retrieval Pipeline:** Utilizes FAISS for highly efficient, local vector storage and semantic similarity search.
*   **Modular Architecture:** Clean separation of concerns across core logic, prompt engineering, data models (Pydantic), and utility functions.
*   **Robust Data Validation:** Enforces strict deterministic outputs via Pydantic schemas.
*   **CI/CD Integration:** Automated testing and deployment workflows managed via GitHub Actions and Jenkins.
*   **Containerized Environments:** fully supported Docker configurations for consistent development and production environments.

## Repository Architecture

```txt
rag_project/
├── .github/
│   └── workflow/
│       ├── aws.yml
│       ├── ci.yaml
│       └── task_definition.json
├── .env                                 # Local runtime environment configurations
├── .dockerignore
├── .gitignore                           # Version control exclusions
├── .python-version                      # Python interpreter runtime specification
├── pyproject.toml                       # Modern build system & dependency configuration (uv/pip)
├── requirements.txt                     # Flat dependency manifest
├── docker-compose.jenkins.yml
├── Dockerfile
├── Dockerfile.jenkins
├── Jenkinsfile.test
├── uv.lock                              # Deterministic environment lockfile
├── README.md                            # Project documentation and setup guide
├── config/                              # Application configurations
│   └── config.yaml                      # Centralized model and parameter definitions
├── data/                                # Static and persistent data structures
│   ├── goldens.csv                      # Ground-truth evaluation golden dataset
│   ├── Agentic AI.txt                   # Sample ingestion document
│   └── The Goal.pdf                     # Sample ingestion document
├── notebooks/                           # Dynamic research, prototyping, and exploration
│   ├── data_ingestion.ipynb
│   ├── evaluations.ipynb
│   ├── experiments.ipynb
│   └── rag.ipynb
├── static/                              # Web serving static assets
│   └── styles.css
├── templates/                           # Web engine HTML layout templates
│   └── index.html
├── tests/                               # Complete validation framework (Pytest target)
│   ├── conftest.py                      # Shared fixtures and configurations
│   ├── test_chat_route.py               # Integration tests for chat execution routing
│   ├── test_upload_route.py             # Integration tests for file ingestion routing
│   ├── unit/                            # Isolated small-scope structural tests
│   │   ├── test_data_ingestion.py
│   │   └── test_retrieval.py
│   └── runtime/                         # Operational integration testing scripts
│       ├── main.py                      # Server entry point
│       └── test.py                      # Temporary end-to-end trial script
├── storage/                             # Ephemeral application outputs (Git-ignored)
│   ├── faiss_index/                     # Local vector index binary segments
│   ├── logs/                            # Standard text/JSON structural runtime logs
│   └── sessions/                        # Dynamic multi-user workspace storage
│       ├── session_20260618_173417_6eefffeb/
│       ├── session_20260618_194535_434fed58/
│       │   └── a3516756.pdf
│       └── session_20260619_143413_cd1a000e/
│           └── a3c35f7f.txt
└── src/                                 # Core source tree (Installable local package)
    └── multi_doc_chat/                  # Main application package namespace
        ├── __init__.py                  # Exposes core package entry points
        ├── core/                        # Core business logic pipelines
        │   ├── __init__.py
        │   ├── ingestion.py             # Document splitting and vector indexing pipelines
        │   └── retrieval.py             # LCEL graph composition and QA chains
        ├── models/                      # Pydantic schemas and interface validators
        │   ├── __init__.py
        │   └── schemas.py               # Holds ChatAnswer, ChatRequest, UploadResponse
        ├── prompts/                     # System instruction library management
        │   ├── __init__.py
        │   └── library.py               # Central prompt configurations
        └── utils/                       # Decoupled infrastructural cross-cutting helpers
            ├── __init__.py
            ├── config_loader.py         # Multi-format system loader
            ├── document_ops.py          # File format chunk extraction strategies
            ├── exceptions.py            # Custom system error boundary handling
            ├── file_io.py               # OS filesystem operations
            ├── logger.py                # Centralized system logger instance
            └── model_loader.py          # LLM/Embedding runtime orchestration
```

# Getting Started

## Prerequisites

- Python 3.x (Refer to .python-version for specific runtime)

- Docker & Docker Compose (for containerized execution)

- uv or pip for dependency management


## Installation

  ## Clone the repository:
```bash
git clone https://github.com/AhmadTigress/rag_project
cd rag_project
```

## Set up the environment:
Ensure you define the required environment variables in the .env file (e.g., API keys, deployment environments).

## Install dependencies:
Using uv (recommended):
```bash
uv sync
```

Or using standard pip:
```bash
pip install -r requirements.txt
```

## Usage
Running the Server

To initialize the main application server, execute the runtime script:
```bash
python tests/runtime/main.py
```

## Prototyping and Exploration

Navigate to the notebooks/ directory to utilize interactive Jupyter notebooks for:

- data_ingestion.ipynb: Testing chunking and embedding strategies.

- rag.ipynb: Experimenting with retrieval chains.

- evaluations.ipynb: Running ground-truth checks against data/goldens.csv.
  

## Testing

The project maintains a rigorous testing standard. Execute the test suite using pytest:
```bash
pytest tests/
```

The testing framework includes isolated unit tests for structural integrity and comprehensive integration tests for file ingestion and chat routing.

## Deployment

Deployment pipelines are pre-configured in the .github/workflow directory for AWS, alongside Docker and Jenkins configurations (Dockerfile.jenkins, docker-compose.jenkins.yml) to support continuous integration and continuous delivery (CI/CD) practices.

## License
MIT License
