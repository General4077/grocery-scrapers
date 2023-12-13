
FROM python:3.11-slim 
# 3.12 will require removing or fixing pyRdfa from extruct (import imp)
# 3.13 will require removing or fixing htmlmin (import cgi)
WORKDIR /app
COPY config/client/requirements.txt .
RUN pip install -r requirements.txt
COPY ../.. .
CMD ["python", "client_start.py"]
