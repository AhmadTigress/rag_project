# Use official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set workdir
WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y build-essential poppler-utils curl && rm -rf /var/lib/apt/lists/*

# Install uv (Python package/dependency manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"
ENV UV_LINK_MODE=copy
ENV PYTHONPATH="/app:/app/multi_doc_chat"

# --- INTEGRATION: Native uv lockfile installation ---

# 1. Copy your environment configuration files
COPY pyproject.toml uv.lock ./

# 2. Sync your production dependencies using the lockfile
RUN uv sync --frozen --no-dev --compile-bytecode

# 3. Copy the rest of your app code
COPY . .

# 4. Prepend the virtual environment's bin folder to PATH 
# This ensures runtime commands use the synchronized environment packages
ENV PATH="/app/.venv/bin:$PATH"

# Expose port
EXPOSE 8080

# Run FastAPI with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]