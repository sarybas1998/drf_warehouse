FROM python:3.10-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /drf_app

# Copy project
COPY . /drf_app

RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org  --upgrade pip
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

RUN chmod +x /drf_app/entrypoint.sh
RUN chmod +x /drf_app/wait-for-it.sh
RUN mkdir -p /drf_app/logs
RUN chmod -R 777 /drf_app/logs
RUN mkdir -p /drf_app/logs/app
RUN chmod -R 777 /drf_app/logs/app
RUN mkdir -p /drf_app/warehouse_app/migrations
RUN chmod -R 777 /drf_app/warehouse_app/migrations
RUN mkdir -p /drf_app/authentication_app/migrations
RUN chmod -R 777 /drf_app/authentication_app/migrations

CMD ["sh", "/drf_app/entrypoint.sh"]
