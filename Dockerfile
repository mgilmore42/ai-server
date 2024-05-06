# Use a base image
FROM debian:latest

# Set the working directory
WORKDIR /app

# Copy the app files to the container
COPY ai_server /app/ai_server
COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock
COPY README.md /app/README.md
COPY LICENSE /app/LICENSE

# Install any dependencies
RUN apt-get update && apt-get install -y python3 poetry

# Install Configure Poetry
RUN poetry config virtualenvs.create false

# Install the dependencies
RUN poetry install

# Expose the necessary ports
EXPOSE 5000

# Define the command to run your app
CMD ai-server