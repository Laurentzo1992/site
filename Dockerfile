FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /var/www/site

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /var/www/site

RUN chmod +x /var/www/site/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/var/www/site/entrypoint.sh"]
CMD ["gunicorn", "website.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
