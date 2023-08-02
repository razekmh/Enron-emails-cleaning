--\connect $APP_DB_USER $APP_DB_NAME
COPY emails FROM '/docker-entrypoint-initdb.d/emails.csv' DELIMITER ',' CSV HEADER;
INSERT INTO users (user_id, user_email, first_name, last_name, rank, role, company)
VALUES('0','Unknown',NULL, NULL, NULL, NULL, NULL);
COPY users FROM '/docker-entrypoint-initdb.d/unique_users_with_names.csv' DELIMITER ',' CSV HEADER;
COPY email_transactions FROM '/docker-entrypoint-initdb.d/unique_email_users.csv' DELIMITER ',' CSV HEADER;
