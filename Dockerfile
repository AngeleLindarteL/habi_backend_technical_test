FROM python:3.12-slim-bookworm AS builder

ARG APP_NAME
ENV APP_NAME=${APP_NAME}

WORKDIR /app

RUN pip install poetry==1.8.3

COPY ./poetry.lock /app/poetry.lock
COPY ./pyproject.toml /app/pyproject.toml

RUN poetry install

COPY ./lib /app/lib
COPY ./apps /app/apps

RUN pip cache purge && poetry cache clear --all .

COPY ./.env /app/.env

CMD ["sh", "-c", "poetry run fastapi run apps/$APP_NAME/main.py --port 8080"]
