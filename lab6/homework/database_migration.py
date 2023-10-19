import psycopg2
import re
import sqlite3
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

sqlite_db_path = config['sqlite_db_path']
dump_file = config['dump_file']
db_name = config['db_name']
user = config['user']
password = config['password']
host = config['host']
port = config['port']


try:
    with sqlite3.connect(sqlite_db_path) as conn:
        with open(dump_file, 'w') as dump:
            for line in conn.iterdump():
                dump.write(f'{line}\n')
    print("Data dumped from SQLite")
except sqlite3.Error as e:
    print(f'SQLite error: {e}')

db_params = {
    'dbname': db_name,
    'user': user,
    'password': password,
    'host': host,
    'port': port
}

# SQL file containing data
sql_file = 'dump.sql'


# SQL commands
def execute_sql(commands):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        for command in commands:
            cursor.execute(command)
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error: {e}")


with open(dump_file, 'r') as file:
    sql_commands = file.read()

commands = [cmd.strip() for cmd in sql_commands.split(';') if cmd.strip()]

drop_table_command = "DROP TABLE IF EXISTS electro_scooter;"
execute_sql([drop_table_command])

execute_sql(commands)

print("Data inserted into PostgreSQL")
