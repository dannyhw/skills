# sqlpipe

**sqlpipe** is a command-line tool that copies Postgres tables to Amazon S3 as Parquet files. You point it at a table, choose a bucket, and it does the rest. It reads the data, writes it in a compact columnar format, and uploads it.

Most teams build their own export scripts. Each script handles naming, schemas, and retries in a different way. That makes the data hard to find, hard to trust and hard to maintain.

sqlpipe fixes this. Your organization defines one shared set of rules for paths, formats and settings. Every team then exports data the same way. Syncs are repeatable and easy to review. Analysts and engineers always know where the data lives and what it looks like.