FROM python:3.12-slim

WORKDIR /app

RUN mkdir -p /app/uploads /app/db

VOLUME /app/uploads
VOLUME /app/db

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src .

CMD ["sh", "-c", "python3 run_admin.py & python3 run_user.py && wait"]
