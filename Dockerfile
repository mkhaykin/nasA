FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src .

CMD ["sh", "-c", "python3 run_admin.py & python3 run_user.py && wait"]
