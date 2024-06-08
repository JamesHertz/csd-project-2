#!/usr/bin/env python3

import sqlite3
import sys

from utils import DB_SCHEMA

def main( args : list[str] ):
    if len(args) < 3:
        print('Error: Missing arguments', file=sys.stderr)
        print(f'usage: {args[0]} <csv-file> <db-file>', file=sys.stderr)
        sys.exit(1)

    csv_file = args[1]
    db_file  = args[2]
    con = sqlite3.connect(db_file)

    con.execute('DROP TABLE IF EXISTS DataSet')
    con.execute(DB_SCHEMA)

    with open(csv_file) as file:
        data = []
        file.readline()
        for line in file.readlines():
            row = line.strip().split(',')
            # row_values = row[:-3] + ['1' if r == 'True' else '0' for r in row[-3:]]

            data.append(row)

        con.executemany('insert into DataSet values(?,?,?,?,?,?)', data)

    con.commit()
    con.close()

    print(f"saved {len(data)} rows in '{db_file}'")

if __name__ == '__main__':
    main(sys.argv)
