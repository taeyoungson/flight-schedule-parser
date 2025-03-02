FROM python:3.11

# Copy the current directory contents into the container at /app
COPY . /app

# Set the working directory
WORKDIR /app

# Install uv and sync
RUN python -m pip install uv
RUN uv sync

ENTRYPOINT [""]
