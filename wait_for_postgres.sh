#!/bin/bash
set -e

echo "⏳ Attente de PostgreSQL à $POSTGRESQL_HOST:$POSTGRESQL_PORT..."
until pg_isready -h "$POSTGRESQL_HOST" -p "$POSTGRESQL_PORT" -U "$POSTGRESQL_USER"; do
  sleep 2
done
echo "✅ PostgreSQL est prêt, lancement de l'API..."
exec "$@"