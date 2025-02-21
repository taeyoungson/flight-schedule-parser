FROM python:3.11

# Copy the current directory contents into the container at /app
COPY . /app

# Set the working directory
WORKDIR /app

# Install uv
RUN python -m pip install uv

RUN uv export --no-hashes --format requirements-txt > requirements.txt

RUN python -m pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "-m", "cron"]
