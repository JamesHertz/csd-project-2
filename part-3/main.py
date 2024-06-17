#!/usr/bin/env python3

import sqlite3
import numpy as np
import os
import sys

from utils import DB_SCHEMA

DB_FILE = 'dataset.db'

def load_data_base() -> sqlite3.Connection:
    print(f"Loading database from '{DB_FILE}' (please be sure you are on the right folder)")
    return sqlite3.connect(DB_FILE)

def choose_select() -> tuple[int, str] | None:
    line = input('select-option: ')

    while line.strip() == '':
        line = input('select-option: ')

    try:
        option = int(line.strip())
        if option < 0 or option > 2:
            raise ValueError("Option should be between 0 and 2.")
    except Exception as e:
        print('Error parsing option:', e)
        return None

    if option == 0:
        return (0, '')

    where_clause = input("where clause (without 'where' keyword): ")
    if where_clause.find(';') != -1:
        print("Invalid where clause it cannot contain the ';' character")
        return None

    return (option, where_clause)

# it seems reasolable c:
privacy_budget = 10
params = {
    1 : {
        'query'  : 'select count(*)',
        'epsilon' : 0.5,
        'sensitivity': 1
    },
    2 : {
        'query'  : 'select avg(education)',
        'epsilon' : 0.5,
        # assuming 16 assuming that the maximum education level is 16 
        # (but still we are gonna have devide by the query output nr which will be calculated later)
        'sensitivity': 16 
    }
}

def execute_query( db : sqlite3.Connection, query : tuple[int, str]):
    global privacy_budget

    (option, query_str) = query
    entry = params[option]

    epsilon = entry['epsilon']
    if epsilon > privacy_budget:
        print('Sorry you rand out of privacy buget (deleting db)')
        os.remove(DB_FILE)
        sys.exit(1)

    try:
        sql_query = entry['query'] + ' from DataSet'
        if query_str != '':
            sql_query += ' where ' + query_str

        print(f' * Executing: "{sql_query}"')
        cursor = db.execute(sql_query)
    except Exception as e:
        print('Error executing query:', e)
        return

    sensitivity = entry['sensitivity']
    if option == 2:
        cursor = db.execute('select count(*) from ' + sql_query.split('from', maxsplit=1)[1])
        sensitivity += 1 #/= len(cursor.fetchall())

    rows = cursor.fetchall()
    resp = 0 if rows == [] else rows[0][0]
    resp += np.random.laplace(loc=0, scale=sensitivity/epsilon)
    privacy_budget -= epsilon
    print('result:', round(resp, 2))


def main():
    db = load_data_base()

    print(f"""
Welcome to my little program
You will be prompted to select a `select clause` and to type in one line a `where clause`
The database schema you will be querying is:
{DB_SCHEMA}

You will be promted to select a  `select optoin` that an be:

1. count(*)
2. avg(education)

Or you can pres '0' to exit. 

Then you will be prompt to write the where clause of your sql query.""")


    # query = read_query()
    query = choose_select()

    while query != (0, ''):
        if query == None:
            print('Invalid option lets try again..')
        else:
            execute_query(db, query)
        query = choose_select()



    print('Bye bye!!')

if __name__ == '__main__':
    main()
