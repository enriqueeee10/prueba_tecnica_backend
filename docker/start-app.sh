#!/bin/sh

echo "Esperando a que la base de datos esté disponible..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Base de datos lista."

# Ejecutar migraciones de Alembic
alembic upgrade head

# Luego iniciar la app
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
