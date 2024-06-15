FROM python:3.11.9-slim-bookworm as builder
ENV PATH="${PATH}:/etc/poetry/bin"
RUN apt update -y
RUN apt upgrade -y
RUN apt install curl -y
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
RUN poetry config virtualenvs.in-project true
COPY mailer/pyproject.toml pyproject.toml
CMD poerty lock
RUN poetry install

FROM python:3.11.9-slim-bookworm
COPY --from=builder .venv/ .venv/
COPY mailer .