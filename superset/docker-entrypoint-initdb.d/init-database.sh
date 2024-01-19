#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" <<-EOSQL
    CREATE USER superset WITH PASSWORD 'superset';
    CREATE DATABASE superset;
    GRANT ALL PRIVILEGES ON DATABASE superset TO superset;
 
EOSQL

psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" -d "superset" <<-EOSQL
   GRANT ALL ON SCHEMA public TO superset;
EOSQL