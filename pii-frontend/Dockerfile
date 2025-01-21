FROM python:3.12-slim

WORKDIR /app

# Install poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root

COPY . .

EXPOSE 7860

CMD ["poetry", "run", "python", "app.py"]

