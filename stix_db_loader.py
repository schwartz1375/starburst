#!/usr/bin/env python3

__author__ = 'Matthew Schwartz (@schwartz1375)'

import json
import sqlite3
from sqlite3 import Error

import requests


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, table_name, field_names):
    field_strings = [f"{name} text" for name in field_names]
    field_strings.append("id text PRIMARY KEY")
    fields = ', '.join(field_strings)
    table_creation_sql = f"""CREATE TABLE IF NOT EXISTS {table_name} ({fields});"""
    try:
        c = conn.cursor()
        c.execute(table_creation_sql)
    except Error as e:
        print(e)


def add_stix_object(conn, stix_object, table_name, field_names):
    cur = conn.cursor()
    while True:
        fields = ', '.join(field_names)
        placeholders = ', '.join('?' * len(field_names))
        sql = f'INSERT INTO {table_name} (id, {fields}) VALUES (?, {placeholders})'
        try:
            values = []
            for field in field_names:
                value = stix_object.get(field, "")
                if isinstance(value, list) or isinstance(value, dict):
                    value = json.dumps(value)
                values.append(value)
            cur.execute(sql, [stix_object['id']] + values)
            break
        except sqlite3.OperationalError as e:
            if 'has no column' in str(e):
                missing_column = str(e).split('has no column named ')[1]
                cur.execute(
                    f'ALTER TABLE {table_name} ADD COLUMN {missing_column} text')
                conn.commit()
                field_names.append(missing_column)
            else:
                raise
        except sqlite3.IntegrityError:
            print(
                f"Warning: ID {stix_object['id']} already exists in {table_name}.")
            break


'''
# Load data from the JSON file 
with open('./enterprise-attack-13.1.json') as f:
    data = json.load(f)
'''

# Get and load data from the JSON file
url = "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-13.1.json"
response = requests.get(url)

data = response.json()

# Connect to the SQLite database
database = "./sqlite_mitre-attack_13.1.db"
conn = create_connection(database)

# Inserting the STIX objects into the SQLite DB
for obj in data['objects']:
    table_name = obj['type'].replace('-', '_')
    field_names = [key for key in obj.keys() if key not in ['type', 'id']]
    create_table(conn, table_name, field_names)
    add_stix_object(conn, obj, table_name, field_names)

# Commit the changes and close the connection
conn.commit()
conn.close()
