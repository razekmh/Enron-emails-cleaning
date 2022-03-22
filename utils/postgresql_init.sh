#!/bin/bash
set -e
export PGPASSWORD=$POSTGRES_PASSWORD;
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	DROP USER $APP_DB_USER IF EXISTS;
	DROP DATABASE $APP_DB_NAME IF EXISTS;
	CREATE USER $APP_DB_USER WITH PASSWORD '$APP_DB_PASS';
	CREATE DATABASE $APP_DB_NAME;
	GRANT ALL PRIVILEGES ON DATABASE $APP_DB_NAME TO $APP_DB_USER;
	\connect $APP_DB_NAME $APP_DB_USER
	BEGIN;
		DROP TABLE IF EXISTS email CASCADE;

		CREATE TABLE email (
		email_message_id VARCHAR (50) PRIMARY KEY,
		email_date TIMESTAMP with time zone,
		email_subject TEXT,
		email_body TEXT
		);

		COPY email FROM '/opt/enron_processed/enron_postgresql/emails.csv' DELIMITER ',' CSV HEADER;


		DROP TABLE IF EXISTS employee CASCADE;

		CREATE TABLE employee (
		user_id VARCHAR (50) PRIMARY KEY,
		user_email VARCHAR (250),
		first_name VARCHAR (250),
		last_name VARCHAR (250),
		rank VARCHAR (250),
		role VARCHAR (250),
		company VARCHAR (250)
		);

		INSERT INTO employee (user_id, user_email, first_name, last_name, rank, role, company)
		VALUES('0','Unknown',NULL, NULL, NULL, NULL, NULL);

		COPY employee FROM '/opt/enron_processed/enron_postgresql/unique_users_with_names.csv' DELIMITER ',' CSV HEADER;


		DROP TABLE IF EXISTS eamil_transaction CASCADE;

		CREATE TABLE eamil_transaction (
		transaction_id VARCHAR (50) PRIMARY KEY,
		email_message_id VARCHAR (50),
		sender VARCHAR (250),
		receiver VARCHAR (250),
		transaction_type VARCHAR (250),
		external_or_internal VARCHAR (250),
		FOREIGN KEY (email_message_id) REFERENCES email(email_message_id),
		FOREIGN KEY (sender) REFERENCES employee(user_id),
		FOREIGN KEY (receiver) REFERENCES employee(user_id)
		);

		COPY eamil_transaction FROM '/opt/enron_processed/enron_postgresql/data/unique_email_users.csv' DELIMITER ',' CSV HEADER;
	COMMIT;
EOSQL
