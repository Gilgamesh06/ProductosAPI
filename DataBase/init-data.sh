#!/bin/bash
set -e

echo "Esperando a que el backend esté listo..."
sleep 15

echo "Verificando si las tablas existen..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -c '\dt' | grep -q 'categoria'; do
  echo "Esperando a que FastAPI cree las tablas..."
  sleep 3
done

echo "Tablas detectadas. Poblando base de datos..."
PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -f /initdb.sql

echo "✓ Base de datos poblada exitosamente!"
