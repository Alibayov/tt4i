FROM python:3.9-slim

USER root

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY final_test_script.py .

CMD ["python", "-u", "/app/final_test_script.py"]
~                                                 
