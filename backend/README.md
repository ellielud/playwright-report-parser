

### Postgres 
1. Pulled the Postgres image from docker using `docker pull postgres`
2. Run using:
```
docker run --name my_postgres \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=playwright_report_parser \
  -p 5433:5432 \
  -d postgres
```


### alembic 
1. Installed alembic
2. Ran `alembic init alembic` which generated the alembic.ini
3. Updated the SQLAlchemy URL property to point at our local postgres database
4. Created a migration script using `alembic revision -m "create test_runs table"`
5. Updated the migration script to generate tables.
6. To run the migration script, `alembic upgrade head`.
```
alembic upgrade head
```
dont need to creat another migraiton file as already done, but if someone else was to try this out, they would need to run this command.


### backend 
To run the backend, use:
```
fastapi dev main.py
```

### SQLAlchemy
1. Created the db.py which has a method for creating a database session
2. Then updated the endpoint in main.py to use db session and query the db





