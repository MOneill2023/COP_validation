from sqlite3 import connect
sql_conn = connect("database.db")

sql_conn.execute("CREATE TABLE if not exists validations (submission_id INT, field_name varchar(255), validation_type Varchar(50), number_failed INT)")

sql_conn.execute("CREATE TABLE if not exists job_start (submission_id INT, submitter VARCHAR(255), processing_start_time DATETIME)")

sql_conn.execute("CREATE TABLE if not exists job_finish (submission_id INT, row_count INT, processing_end_time DATETIME)")