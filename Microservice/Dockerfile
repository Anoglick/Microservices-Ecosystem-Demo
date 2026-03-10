FROM python:3.11

WORKDIR /services/users
COPY . /services/users

ENV PYTHONPATH=/services

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8002

CMD ["uvicorn", "src.app.api:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]