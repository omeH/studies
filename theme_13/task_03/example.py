import sys
import argparse
import re

import psycopg2


TABLE = 'example'
COLUMNS = ['id', 'data', 'date', 'name']


class SQLInjection(Exception):
    pass


class WorkWithDB(object):

    sql_injection = re.compile(r'^[a-zA-Z\d_]*$')
    dsn_format = 'dbname={0} user={1} password={2} host={3}'

    SELECT_QUERY = "SELECT {0} FROM {1};"
    INSERT_QUERY = "INSERT INTO {0} ({1}) VALUES ({2});"
    UPDATE_QUERY = "UPDATE {0} SET {1} WHERE {2};"
    DELETE_QUERY = "DELETE FROM {0} WHERE {1};"

    DBNAME_KEY = 'dbname'
    USER_KEY = 'user'
    PASSWORD_KEY = 'password'
    HOST_KEY = 'host'

    ###################
    # Default options #
    ###################
    dbname = 'postgres'
    user = 'postgres'
    pasword = 'secret'
    host = 'localhost'

    connection = None

    def __init__(self, **options):
        if self.DBNAME_KEY in options:
            self.dbname = options[self.DBNAME_KEY]
        if self.USER_KEY in options:
            self.user = options[self.USER_KEY]
        if self.PASSWORD_KEY in options:
            self.pasword = options[self.PASSWORD_KEY]
        if self.HOST_KEY in options:
            self.host = options[self.HOST_KEY]

    def connect(self):
        dsn = self.dsn_format.format(
            self.dbname, self.user, self.pasword, self.host
        )
        self.connection = psycopg2.connect(dsn)
        self.cursor = self.connection.cursor()

    def close(self):
        if self.connection:
            self.connection.close()

    def _is_execute(self, query, *params):
        try:
            self.cursor.execute(query, *params)
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

    def insert(self, table, data):
        self._correct_data([table] + data.keys())

        query = self.INSERT_QUERY.format(
            table,
            ', '.join(data.keys()),
            ', '.join(['%({0})s'.format(key) for key in data])
        )

        if self._is_execute(query, data):
            self.connection.commit()
        else:
            self.connection.rollback()

    def update(self, table, data, condition):
        self._correct_data([table] + data.keys() + condition.keys())

        query = self.UPDATE_QUERY.format(
            table,
            ', '.join(['{0} = %({0})s'.format(key) for key in data]),
            '{0} = %({0})s'.format(condition.keys()[0])
        )
        data.setdefault(*condition.items()[0])

        if self._is_execute(query, data):
            self.connection.commit()
        else:
            self.connection.rollback()

    def delete(self, table, condition):
        self._correct_data([table] + condition.keys())

        query = self.DELETE_QUERY.format(
            table,
            '{0} = %({0})s'.format(condition.keys()[0])
        )

        if self._is_execute(query, condition):
            self.connection.commit()
        else:
            self.connection.rollback()


def parser_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-d', '--dbname', type=str, default='exampledb',
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

    try:
        w = WorkWithDB(**options.__dict__)
        w.connect()
        w.select(TABLE, COLUMNS)
        print
        w.insert(TABLE, {'id': 8, 'data': 'test python',
                         'date': psycopg2.Date(2014, 10, 22),
                         'name': 'python'})
        w.select(TABLE, COLUMNS)
        print
        w.update(TABLE, {'name': 'python2.7', 'data': 'string'}, {'id': '8'})
        w.select(TABLE, COLUMNS)
        print
        w.delete(TABLE, {'id': '8'})
        w.select(TABLE, COLUMNS)
    except psycopg2.DatabaseError as error:
        print(error)
        sys.exit(1)
    finally:
        w.close()


if __name__ == '__main__':
    main()
