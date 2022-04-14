--\connect $APP_DB_USER $APP_DB_NAME

DROP TABLE IF EXISTS emails CASCADE;

CREATE TABLE emails (
		email_message_id VARCHAR (50) PRIMARY KEY,
		email_date TIMESTAMP with time zone,
		email_subject TEXT,
		email_body TEXT
		);

COPY emails FROM '/docker-entrypoint-initdb.d/emails.csv' DELIMITER ',' CSV HEADER;

DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
		user_id VARCHAR (50) PRIMARY KEY,
		user_email VARCHAR (250),
		first_name VARCHAR (250),
		last_name VARCHAR (250),
		rank VARCHAR (250),
		role VARCHAR (250),
		company VARCHAR (250)
		);

INSERT INTO users (user_id, user_email, first_name, last_name, rank, role, company)
VALUES('0','Unknown',NULL, NULL, NULL, NULL, NULL);

COPY users FROM '/docker-entrypoint-initdb.d/unique_users_with_names.csv' DELIMITER ',' CSV HEADER;


DROP TABLE IF EXISTS email_transactions CASCADE;

CREATE TABLE email_transactions (
		transaction_id VARCHAR (50) PRIMARY KEY,
		email_message_id VARCHAR (50),
		sender VARCHAR (250),
		receiver VARCHAR (250),
		transaction_type VARCHAR (250),
		external_or_internal VARCHAR (250),
		FOREIGN KEY (email_message_id) REFERENCES emails(email_message_id),
		FOREIGN KEY (sender) REFERENCES users(user_id),
		FOREIGN KEY (receiver) REFERENCES users(user_id)
		);

COPY email_transactions FROM '/docker-entrypoint-initdb.d/unique_email_users.csv' DELIMITER ',' CSV HEADER;

\set PG_VIEWER_USER `echo "$PG_VIEWER_USER"`
\set PG_VIEWER_PASS `echo "$PG_VIEWER_PASS"`
\set APP_DB_NAME `echo "$APP_DB_NAME"`


CREATE USER :PG_VIEWER_USER WITH ENCRYPTED PASSWORD :'PG_VIEWER_PASS';
GRANT CONNECT ON DATABASE :APP_DB_NAME TO :PG_VIEWER_USER;
GRANT USAGE ON SCHEMA public TO :PG_VIEWER_USER;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO :PG_VIEWER_USER;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO :PG_VIEWER_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO :PG_VIEWER_USER;
