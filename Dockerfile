FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN echo '#!/bin/bash' > docker-entrypoint.sh
RUN echo 'set -e' >> docker-entrypoint.sh
RUN echo '' >> docker-entrypoint.sh
RUN echo 'echo "Creating database tables..."' >> docker-entrypoint.sh
RUN echo 'python -c "from app import create_app, db; app = create_app('"'"'production'"'"'); app.app_context().push(); db.create_all()"' >> docker-entrypoint.sh
RUN echo '' >> docker-entrypoint.sh
RUN echo 'echo "Starting gunicorn..."' >> docker-entrypoint.sh
RUN echo 'exec gunicorn --bind 0.0.0.0:5000 --workers 2 wsgi:app' >> docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh
EXPOSE 5000
ENTRYPOINT ["./docker-entrypoint.sh"]