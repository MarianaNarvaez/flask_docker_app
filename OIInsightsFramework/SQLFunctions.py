# Load libraries
import pyodbc
import pandas as pd
import contextlib
import logging


class SQLFunctions:
    def __init__(self, connectionString: str):
        self.connection: str = connectionString

    @contextlib.contextmanager
    def dbconnect(self, log=False):
        dbConnection: pyodbc.Connection = pyodbc.connect(self.connection)
        try:
            if log:
                logging.info("Opening Connection: {}".format(self.connection))
            yield dbConnection
        finally:
            dbConnection.close()
            if log:
                logging.info("Closing Connection: {}".format(self.connection))

    def execute_query_SQL(self, query: str, args=None):
        with self.dbconnect() as dbConnection:
            result = pd.read_sql_query(query, dbConnection, params=args)
            logging.info("Executed query: {}, args:{}".format(query,args))
        return result

    def execute_statement_SQL(self, statement: str, args=None):
        with self.dbconnect() as dbConnection:
            cursor = dbConnection.cursor()
            cursor.execute(statement, args)
            affected_records = cursor.rowcount
            dbConnection.commit()
            logging.info("Executed statement: {}, args:{}".format(statement,args))
        return affected_records

    def execute_manystatement_SQL(self, statement: str, args=None):
        with self.dbconnect() as dbConnection:
            cursor = dbConnection.cursor()
            cursor.executemany(statement, args)
            affected_records = cursor.rowcount
            dbConnection.commit()
            logging.info("Executed statement: {}, args:{}".format(statement,args))
        return affected_records