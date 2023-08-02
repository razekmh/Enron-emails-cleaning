--\connect $APP_DB_USER $APP_DB_NAME

\set PG_VIEWER_USER `echo "$PG_VIEWER_USER"`
\set PG_VIEWER_PASS `echo "$PG_VIEWER_PASS"`
\set APP_DB_NAME `echo "$APP_DB_NAME"`


CREATE USER :PG_VIEWER_USER WITH ENCRYPTED PASSWORD :'PG_VIEWER_PASS';
GRANT CONNECT ON DATABASE :APP_DB_NAME TO :PG_VIEWER_USER;
GRANT USAGE ON SCHEMA public TO :PG_VIEWER_USER;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO :PG_VIEWER_USER;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO :PG_VIEWER_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO :PG_VIEWER_USER;

