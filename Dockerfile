FROM python:3.13-alpine

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . ./salary
WORKDIR /salary

CMD ["sh", "-c", "python3 main.py"]
