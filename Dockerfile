FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./app /app

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
CMD ["ddtrace-run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# archive config CMD ["ddtrace-run", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--workers", "4", "app.src.main:app", "--bind", "0.0.0.0:80"]
