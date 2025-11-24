FROM python:3
# Working directory in the container
WORKDIR /app
# Requirements first! for cache performance
COPY requirements.txt .
RUN pip install -r requirements.txt
# Then the source code
COPY src .
# For initial data
COPY docker/freeradius-mysql/initial_data.py .
