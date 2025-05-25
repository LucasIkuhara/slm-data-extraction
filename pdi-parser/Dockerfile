FROM ubuntu

RUN apt update && apt upgrade

RUN apt install -y curl python3.12

RUN curl -sSL https://install.python-poetry.org | python3.12 -

WORKDIR /app

COPY pyproject.toml .

RUN /root/.local/bin/poetry install --no-root

COPY . .