FROM python:3.12-bookworm as builder

WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.8.3 \
  # App's configuration:
#  BOT_TOKEN="7360303774:AAEuj7nKEPJhUxR0J-GJACwCr6kd002aYok" \
#  DB_URL="mysql+aiomysql://root:password@localhost:9006/impression_db"\
#  DEBUG_MODE=true \
#  EMPTY_DB=true \
#  LOCALES_PATH="/app/bot/locales" \
#  MODELS_PATH="/app/models" \
#  WEBHOOK_URL="http://lemonade-bot-test.freemyip.com" \
#  WEBHOOK_PATH="/webhook" \
#  PORT=9003 \
#  TELEGRAM_SECRET_TOKEN="jhasdlha9812347123bgjklhsfg8675t123g12hjervsauDFC851673" \
#  FLOOD_AWAITING=0.69 \
#  ADMINS=[430490262]

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev --no-interaction --no-ansi --no-root

#COPY .env ./
COPY bot ./bot
COPY services ./services
COPY models ./models

CMD ["python", "-m", "bot"]

#FROM python:3.12-bookworm
#WORKDIR /app
#
#COPY --from=builder /app ./