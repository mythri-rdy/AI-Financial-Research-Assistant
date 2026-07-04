-- This file runs automatically the FIRST time the Postgres container
-- starts with an empty data volume (Docker's postgres image looks for
-- .sql files in /docker-entrypoint-initdb.d/ and runs them in order).
--
-- pgvector ships as a Postgres extension. Installing the Python
-- "pgvector" package is not enough — the database itself also needs
-- this extension turned on before it understands the VECTOR type.

CREATE EXTENSION IF NOT EXISTS vector;
