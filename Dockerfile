FROM python:3.12

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.3


# System deps:
RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /code

COPY ./ /code/

COPY ./src/research_agent_poc /code/src/

COPY ./src/research_agent_poc /code/

# Copy only requirements to cache them in docker layer
COPY pyproject.toml /code/

# Project initialization:
# RUN poetry config virtualenvs.create false

# RUN poetry install --no-interaction --no-ansi

RUN pip install uv crewai crewai-tools redis

RUN crewai install


CMD ["crewai", "run"]