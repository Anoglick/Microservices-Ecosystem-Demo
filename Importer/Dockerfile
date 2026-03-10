FROM python:3.11

WORKDIR /services/importer
COPY . /services/importer

ENV PYTHONPATH=/services

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "main.py", "run"]