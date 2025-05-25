FROM ubuntu

RUN apt update && apt upgrade

RUN apt install -y curl python3.12 python-is-python3

RUN curl -sSL https://install.python-poetry.org | python3.12 -
ENV POETRY_VIRTUALENVS_CREATE=false
RUN echo 'export PATH=$PATH:/root/.local/bin' >> /root/.bashrc

WORKDIR /app
COPY pyproject.toml .
RUN /root/.local/bin/poetry install

RUN /root/.local/bin/poetry run docling-tools models download

COPY . .