version: '3.8'

services:
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_DB: your_db_name
      POSTGRES_USER: your_db_user
      POSTGRES_PASSWORD: your_db_password

  web:
    build: .
    command: gunicorn --bind 0.0.0.0:8000 studentManagement.wsgi:application
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DEBUG: 'true'
      DATABASE_URL: postgres://your_db_user:your_db_password@db/your_db_name

volumes:
  postgres_data:
