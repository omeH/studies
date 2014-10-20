import sys
import argparse
import re

import psycopg2


DSN = 'dbname={0} user={1} password={2} host={3}'
TABLE = 'example'
COLUMNS = ['id', 'data', 'date', 'name']


class SQLInjection(Exception):
    pass


class WorkWithDB(object):

    sql_injection = re.compile(r'^[a-zA-Z\d]*$')

    SELECT_QUERY = 'SELECT {0} FROM {1};'
    INSERT_QUERY = 'INSERT INTO {0} ({1}) VALUES {2};'
    UPDATE_QUERY = 'UPDATE {0} SET {1} WHERE {2}'
    DELETE_QUERY = 'DELETE FROM {0} WHERE {1}'

    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def _is_execute(self, query, **params):
        try:
            self.cursor.execute(query, **params)
        except psycopg2.DatabaseError as error:
            sys.stdout.write(str(error))
            return False
        return True

    def _is_sql_injection(self, value):
        if self.sql_injection.search(value):
            return False
        return True

    def _correct_data(self, data):
        for item in data:
            if self._is_sql_injection(item):
                raise SQLInjection('{0}'.format(item))

    def select(self, table, columns):
        """
        """
        self._correct_data([table] + columns)

        query = self.SELECT_QUERY.format(','.join(columns), table)

        if self._is_execute(query):
            while True:
                line = self.cursor.fetchone()
                if not line:
                    break
                sys.stdout.write(str(line) + '\n')

    def insert(self, table, columns, data):
        self._correct_data([table] + columns)
        for item in data:
            self._correct_data(item)

        values_list = [','.join(item) for item in data]
        values = '({0})'.format(
            '),('.join(values_list)
        )

        query = self.INSERT_QUERY.format(
            table, ','.join(columns), values
        )

        if self._is_execute(query):
            self.connection.commit()
        else:
            self.connection.rollback()

    def update(self, table, data, condition):
        self._correct_data([table] + condition)
        for item in data:
            self._correct_data(item)

        for index in xrange(len(data)):
            data[index] = "{0} = '{1}'".format(*data[index])

        update_set = ','.join(data)
        update_where = ' = '.join(condition)

        query = self.UPDATE_QUERY.format(table, update_set, update_where)

        if self._is_execute(query):
            self.connection.commit()
        else:
            self.connection.rollback()

    def delete(self):
        pass


def parser_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-d', '--database', type=str, default='exampledb',
        help='Set a name database'
    )
    parser.add_argument(
        '-u', '--user', type=str, default='postgres',
        help='Set a user name'
    )
    parser.add_argument(
        '-p', '--password', type=str, default='secret',
        help='Set a password'
    )
    parser.add_argument(
        '-H', '--host', type=str, default='localhost',
        help='Set a host'
    )

    return parser.parse_args()


def main():
    options = parser_args()

    dsn = DSN.format(
        options.database, options.user, options.password, options.host
    )

    try:
        con = psycopg2.connect(dsn)
        w = WorkWithDB(con)
        w.select(TABLE, COLUMNS)
        w.insert(TABLE, ['test', 'value'], [['s', 't', 'd'], ['1', '2', '3']])
        w.select(TABLE, COLUMNS)
        w.update(TABLE, [['name', 'python']], ['id', '7'])
        w.select(TABLE, COLUMNS)
    except psycopg2.DatabaseError as error:
        print(error)
        sys.exit(1)
    finally:
        if 'con' in globals():
            con.close()


if __name__ == '__main__':
    main()
