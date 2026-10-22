sqlpipe is a command-line tool that copies Postgres tables to S3 as Parquet files. Parquet is a compact file format that analytics tools such as Athena, Spark and DuckDB read quickly.

You run one command to sync a table. sqlpipe reads the rows, converts them to Parquet and uploads the files to your bucket. It sends only the rows that changed since the last run, so repeat syncs are fast and cheap.

sqlpipe also helps your organisation export data in one consistent way. A shared configuration file sets the bucket layout, file naming, compression and schema rules. Every team that uses the file produces the same output, so you do not need to maintain separate export scripts for each team.