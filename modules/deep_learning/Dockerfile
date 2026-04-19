ARG MODEL_PATH="./infotrustai_model"

FROM python:3.12-slim

ARG MODEL_PATH

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .
RUN mkdir -p /app/model
COPY ${MODEL_PATH} /app/model

# Expose port
EXPOSE 5000

# Run the application with Gunicorn
CMD ["gunicorn", "--timeout", "1850", "--bind", "0.0.0.0:5000", "setup.wsgi:application"]
