"""
notes on using psycopg2;
postgres queries;
https://www.postgresqltutorial.com/postgresql-update/
https://realpython.com/prevent-python-sql-injection/
"""


#  db connectivity


# 1. simple connectivity using script
# cursor `cur` from below can be used to execute the query
import psycopg2

try:
    connection = psycopg2.connect(
        host="localhost",
        database="db",
        user="dbuser",
        password=None
    )
    connection.set_session(autocommit=True)
except psycopg2.Error as e: 
    print("Error: Could not make connection to the Postgres database")
    print(e)

try: 
    cur = connection.cursor()
except psycopg2.Error as e: 
    print("Error: Could not get cursor to the Database")
    print(e)


# 2. connectivity using external config file
# we usually put config outside code location so abs path makes sense
# YAML  is good format to store config ; allows comment; json doesnot

import json
import yaml
import psycopg2
import atexit
import collections


class Config:
    def __init__(self):
        self._yaml_path = "/mrconfig/config.yaml"
        self._yaml_data = collections.defaultdict()
        self._json_path = "/mrconfig/config.json"
        self._json_data = collections.defaultdict()
        self._read_from_yaml()
        self._read_from_json()

    def _read_from_yaml(self):
        with open(self._yaml_path, 'r') as stream:
            self._yaml_data = yaml.safe_load(stream)

    def _read_from_json(self):
        with open(self._json_path,'r') as file:
            self._json_data = json.loads(file.read())

    def connection_string(self):
        return self._yaml_data["pg_connection_string"]


class DB:

    def __init__(self, connection_string):
        self._connection_string = connection_string
        self._cursor = None
        self._connection = None
        self._set_connection()

    def _set_connection(self):
        self._connection = psycopg2.connect(self._connection_string)
        self._connection.set_session(autocommit=True)
        self._cursor = self._connection.cursor()

    def cursor(self):
        return self._cursor

    def close_connection(self):
        self._connection.close()

    # def __exit__(self, exc_type, exc_value, traceback):
    #     print('connection closed')
    #     self.close_connection()
    #
    # def cleanup(self):
    #     print('connection closed')
    #     self.close_connection()


class Query:

    def __init__(self):
        config = Config()
        connection = DB(config.connection_string())
        self._cursor = connection.cursor()
"""

# CRUD Operation

1. CREATE

# DROP TABLE IF EXISTS courses;

# CREATE TABLE courses(
	course_id serial primary key,
	course_name VARCHAR(255) NOT NULL,
	description VARCHAR(500),
	published_date date
);

"""

from psycopg2 import sql

try:
    stmt = sql.SQL("""
            DROP TABLE IF EXISTS {table_name} 
            """).format(table_name = sql.Identifier("music_store2"))
    cur.execute(stmt)
except psycopg2.Error as E:
    print("Error: Issue Creating Table")
    print(E)

try:
    stmt = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {table_name} (
                                    transaction_id int,
                                    customer_name varchar,
                                    cashier_name varchar,
                                    year int,
                                    albums_purchased varchar)
                            """).format(table_name = sql.Identifier("music_store2"))
    cur.execute(stmt)
except psycopg2.Error as E:
    print("Error: Issue Creating Table")
    print(E)

# without sql identifier


try:
    cur.execute("DROP TABLE IF EXISTS transactions")
    cur.execute("DROP TABLE IF EXISTS albums_sold")
except psycopg2.Error as E:
    print("Error: Issue dropping Table")
    print(E)

try:
    stmt = sql.SQL("""
            CREATE TABLE IF NOT EXISTS transactions 
            (transaction_id int, 
            customer_name varchar,
            cashier_name varchar,
            year int)
    """)
    cur.execute(stmt)
except psycopg2.Error as e:
    print("Error: Issue creating table")
    print (e)

"""
2. READ

psycopgtest=# SELECT * FROM users;

"""

try:
    stmt = sql.SQL("""
            SELECT t.transaction_id,t.customer_name, t.cashier_name, t.year,a.album_name 
            FROM transactions as t
            JOIN albums_sold as a 
            ON t.transaction_id = a.transaction_id
            """)
    cur.execute(stmt)
except psycopg2.Error as e:
    print("Error: select *")
    print (e)

row = cur.fetchone()
while row:
   print(row)
   row = cur.fetchone()


"""
3. UPDATE
(INSERT , UPDATE, UPSERT)

INSERT INTO 
	courses(course_name, description, published_date)
VALUES
	('PostgreSQL for Developers','A complete PostgreSQL for Developers','2020-07-13'),
	('PostgreSQL Admininstration','A PostgreSQL Guide for DBA',NULL),
	('PostgreSQL High Performance',NULL,NULL),
	('PostgreSQL Bootcamp','Learn PostgreSQL via Bootcamp','2013-07-11'),
	('Mastering PostgreSQL','Mastering PostgreSQL in 21 Days','2012-06-30');
	

UPDATE courses
SET published_date = '2020-08-01' 
WHERE course_id = 3;

# The following statement updates course id 2. 
# It modifies published_date of the course to 2020-07-01 and returns the updated course

UPDATE courses
SET published_date = '2020-07-01'
WHERE course_id = 2
RETURNING *;

# UPSERT
INSERT INTO customer_address (customer_id, customer_street)
VALUES (432, '10 Manhattan Ave')
ON CONFLICT (customer_id)
UPDATE 
    SET customer_street = EXCLUDED.customer_street;

"""

def insert_transaction(transaction_id, customer_name, cashier_name, year):
    try:
        stmt = sql.SQL("""
                INSERT INTO transactions (transaction_id, customer_name, cashier_name, year)
                VALUES ({transaction_id}, {customer_name}, {cashier_name}, {year})
            """).format(transaction_id=sql.Literal(transaction_id),
                        customer_name=sql.Literal(customer_name),
                        cashier_name=sql.Literal(cashier_name),
                        year=sql.Literal(year))
        cur.execute(stmt)
    except psycopg2.Error as E:
        print("Error: Issue Inserting data into transactions")
        print(E)

insert_transaction(1, 'Amanda', 'sam', 2000)

"""
# upsert
--------


In RDBMS language, the term upsert refers to the idea of inserting a new row in an existing row in an 
existing table, or updating the row if it already exists in the table. the action of updating or inserting
has been described as "upsert"

The way this is handled in PostgreSQL is by using the INSERT statement in combination with the ON CONFLICT clause.


Eg.

CREATE TABLE IF NOT EXISTS customer_address (
    customer_id int PRIMARY KEY,
    customer_street varchar NOT NULL,
    customer_city text NOT NULL,
    customer_state text NOT NULL
);

# Inserting data

INSERT into customer_address (customer_id, customer_street, customer_city, customer_state)
VALUES (432, '123 Manhattan Ave','Jersey City','NJ') ;

# on conflict do noting

INSERT into customer_address( customer_id, customer_street, customer_city, customer_state)
VALUES (432 , '22 Manhattan Ave', 'Jersey City', 'NJ')
ON CONFLICT (customer_id)
DO NOTHING;

# on conflict do update
INSERT INTO customer_address (customer_id, customer_street)
VALUES (432, '10 Manhattan Ave')
ON CONFLICT (customer_id)
UPDATE 
    SET customer_street = EXCLUDED.customer_street;

"""

"""
DELETE

links = table_name
# delete table
DROP TABLE IF EXISTS links;

#delete single row
DELETE FROM links
WHERE id = 8;

# deletes and returns deleted row
DELETE FROM links
WHERE id = 7
RETURNING *;

# multiple deletes
DELETE FROM links
WHERE id IN (6,5)
RETURNING *;

# delete all rows
DELETE FROM links;
"""

try:
    stmt = sql.SQL("""
            DROP TABLE IF EXISTS {table_name} 
            """).format(table_name = sql.Identifier("music_store2"))
    cur.execute(stmt)
except psycopg2.Error as E:
    print("Error: Issue Creating Table")
    print(E)