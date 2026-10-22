## Introduction

**sqlpipe** is a command-line tool that syncs Postgres tables to Amazon S3 as Parquet files. Point it at a database, choose the tables you want, and sqlpipe handles extraction, type mapping, compression, and upload. It writes columnar files that work with Athena, Spark, DuckDB, and most other analytics tools.

sqlpipe is also built to help an organization standardize how its teams export data. Shared configuration defines naming conventions, bucket layout, partitioning, and schema handling in one place. Every team then produces consistent, predictable datasets without writing and maintaining its own one-off export scripts.

Use sqlpipe for a single ad hoc export or run it on a schedule in CI. It gives you reliable, repeatable data movement with minimal setup.