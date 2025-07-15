FROM python:3.11-slim

WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# copy app code
COPY app ./app

# default command (for manual runs)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
