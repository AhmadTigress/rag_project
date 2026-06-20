rag_project/
├── .env                         # Local runtime environment configurations
├── .gitignore                   # Version control exclusions
├── .python-version              # Python interpreter runtime specification
├── pyproject.toml               # Modern build system & dependency configuration (uv/pip)
├── requirements.txt             # Flat dependency manifest
├── uv.lock                      # Deterministic environment lockfile
├── README.md                    # Project documentation and setup guide
│
├── config/                      # Application configurations
│   └── config.yaml              # Centralized model and parameter definitions
│
├── data/                        # Static and persistent data structures
│   ├── goldens.csv              # Ground-truth evaluation golden dataset
│   └── Agentic AI.txt           # Sample ingestion document
│   └── The Goal.pdf             # Sample ingestion document
│
├── notebooks/                   # Dynamic research, prototyping, and exploration
│   ├── data_ingestion.ipynb
│   ├── evaluations.ipynb
│   ├── experiments.ipynb
│   └── rag.ipynb
│
├── static/                      # Web serving static assets
│   └── styles.css
│
├── templates/                   # Web engine HTML layout templates
│   └── index.html
│
├── tests/                       # Complete validation framework (Pytest target)
│   ├── conftest.py              # Shared fixtures and configurations
│   ├── test_chat_route.py       # Integration tests for chat execution routing
│   ├── test_upload_route.py     # Integration tests for file ingestion routing
│   ├── unit/                    # Isolated small-scope structural tests
│   │   ├── test_data_ingestion.py
│   │   └── test_retrieval.py
│   └── runtime/                 # Operational integration testing scripts
│       ├── main.py              # Server entry point
│       └── test.py              # Temporary end-to-end trial script
│
├── storage/                     # Ephemeral application outputs (Git-ignored)
│   ├── faiss_index/             # Local vector index binary segments
│   ├── logs/                    # Standard text/JSON structural runtime logs
│   └── sessions/                # Dynamic multi-user workspace storage
│       ├── session_20260618_173417_6eefffeb/
│       ├── session_20260618_194535_434fed58/
│       │   └── a3516756.pdf
│       └── session_20260619_143413_cd1a000e/
│           └── a3c35f7f.txt
│
└── src/                         # Core source tree (Installable local package)
    └── multi_doc_chat/          # Main application package namespace
        ├── __init__.py          # Exposes core package entry points
        │
        ├── core/                # Core business logic pipelines
        │   ├── __init__.py
        │   ├── ingestion.py     # Document splitting and vector indexing pipelines
        │   └── retrieval.py     # LCEL graph composition and QA chains
        │
        ├── models/              # Pydantic schemas and interface validators
        │   ├── __init__.py
        │   └── schemas.py       # Holds ChatAnswer, ChatRequest, UploadResponse
        │
        ├── prompts/             # System instruction library management
        │   ├── __init__.py
        │   └── library.py       # Central prompt configurations
        │
        └── utils/               # Decoupled infrastructural cross-cutting helpers
            ├── __init__.py
            ├── config_loader.py # Multi-format system loader
            ├── document_ops.py  # File format chunk extraction strategies
            ├── exceptions.py    # Custom system error boundary handling
            ├── file_io.py       # OS filesystem operations
            ├── logger.py        # Centralized system logger instance
            └── model_loader.py  # LLM/Embedding runtime orchestration