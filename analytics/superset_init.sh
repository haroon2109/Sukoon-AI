#!/bin/bash
echo "Starting Superset initialization..."

# 1. Setup admin user
docker exec -it superset_app superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@superset.com \
              --password admin

# 2. Upgrade the database (run migrations)
docker exec -it superset_app superset db upgrade

# 3. Create default roles and permissions
docker exec -it superset_app superset init

echo "Superset initialization complete! You can now access the UI at http://localhost:8088 (Login: admin / admin)"
echo "To connect to Supabase, go to Settings -> Database Connections, and use the PostgreSQL driver with your Supabase DB URI."
