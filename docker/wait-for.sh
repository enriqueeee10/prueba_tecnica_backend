#!/usr/bin/env bash

set -e

HOST="$1"
PORT="$2"
shift 2
CMD="$@"

echo "Esperando a que $HOST:$PORT esté disponible..."

# Espera hasta que el puerto esté disponible
while ! nc -z "$HOST" "$PORT"; do
  sleep 1
done

echo "$HOST:$PORT está disponible."

# Ejecutar migraciones primero
echo "Ejecutando migraciones..."
alembic upgrade head

# Luego ejecutar la aplicación
echo "Iniciando la aplicación..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload