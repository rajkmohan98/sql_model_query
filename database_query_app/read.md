I have transitioned to using Django's ORM (Object-Relational Mapping), which provides an abstraction over direct SQL queries while ensuring better scalability and maintainability.
Replacing raw SQL queries with ORM has eliminated direct database connections within the view, reducing complexity.

1, 

to to connect the different database based on database name 

http://127.0.0.1:8000/database/sql_query/

{
    "query":"select * from passengers;",
    "database":"postgres"
}

{
    "query":"select * from passengers;",
    "database":"sqlite"
}

{
    "query":"select * from passengers;",
    "database":"mysql"
}



2,
to view the history that query response with is stored in database
http://127.0.0.1:8000/database/history/