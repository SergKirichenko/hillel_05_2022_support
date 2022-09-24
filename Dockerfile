FROM python:3.8-slim

# Receive build arguments
ARG PIPENV_EXTRA_ARGS


# Change working directory
WORKDIR /app/


# Copy project files
COPY ./ ./


# Install deps
RUN pip install pipenv \
    && pipenv install --system --deploy --ignore-pipfile $PIPENV_EXTRA_ARG

CMD sleep 3 \
    && python src/manage.py migrate \
    && python src/manage.py runserver 0.0.0.0:80