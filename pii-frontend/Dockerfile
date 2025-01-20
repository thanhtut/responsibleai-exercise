FROM python:3.12-slim

WORKDIR /app

# Install poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root

# Copy application code
COPY . .

# Expose port
EXPOSE 7860

# Command to run the application
CMD ["poetry", "run", "python", "app.py"]

