FROM docker.io/python:3.12-bookworm

ENV PYTHONUNBUFFERED=1

RUN pip install poetry

COPY cer2cen ./cer2cen
COPY poetry.lock .
COPY pyproject.toml .
COPY tables.json .

RUN poetry install

ENTRYPOINT ["poetry", "run", "migrate"]